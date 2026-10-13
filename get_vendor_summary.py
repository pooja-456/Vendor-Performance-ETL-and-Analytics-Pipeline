
import sqlite3
import pandas as pd
import logging
import os

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)


def create_vendor_summary(conn):
    """Merge purchase, sales, and freight data into a vendor summary."""

    query = """
    WITH FreightSummary AS (
        SELECT
            VendorNumber,
            SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),

    PurchaseSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp
            ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price,
            pp.Volume
    ),

    SalesSummary AS (
        SELECT
            VendorNo,
            Brand,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand
    )

    SELECT
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchaseSummary ps

    LEFT JOIN SalesSummary ss
        ON ps.VendorNumber = ss.VendorNo
        AND ps.Brand = ss.Brand

    LEFT JOIN FreightSummary fs
        ON ps.VendorNumber = fs.VendorNumber

    ORDER BY ps.TotalPurchaseDollars DESC
    """

    return pd.read_sql_query(query, conn)


def clean_data(df):
    """Clean the summary and calculate vendor performance metrics."""

    # Convert numeric columns safely
    numeric_columns = [
        "PurchasePrice",
        "ActualPrice",
        "Volume",
        "TotalPurchaseQuantity",
        "TotalPurchaseDollars",
        "TotalSalesQuantity",
        "TotalSalesDollars",
        "TotalSalesPrice",
        "TotalExciseTax",
        "FreightCost"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Replace missing numeric values with zero
    df[numeric_columns] = df[numeric_columns].fillna(0)

    # Clean categorical columns
    for column in ["VendorName", "Description"]:
        df[column] = df[column].fillna("").astype(str).str.strip()

    # Calculate metrics safely when denominators are zero
    df["GrossProfit"] = (
        df["TotalSalesDollars"] - df["TotalPurchaseDollars"]
    )

    df["ProfitMargin"] = (
        df["GrossProfit"]
        .div(df["TotalSalesDollars"].where(df["TotalSalesDollars"] != 0))
        .mul(100)
    )

    df["StockTurnover"] = (
        df["TotalSalesQuantity"]
        .div(
            df["TotalPurchaseQuantity"].where(
                df["TotalPurchaseQuantity"] != 0
            )
        )
    )

    df["SalesToPurchaseRatio"] = (
        df["TotalSalesDollars"]
        .div(
            df["TotalPurchaseDollars"].where(
                df["TotalPurchaseDollars"] != 0
            )
        )
    )

    # Avoid infinite values in the output
    metric_columns = [
        "ProfitMargin",
        "StockTurnover",
        "SalesToPurchaseRatio"
    ]

    df[metric_columns] = df[metric_columns].replace(
        [float("inf"), float("-inf")], float("nan")
    )

    return df


def main():
    """Generate, clean, and store the vendor sales summary."""

    db_path = "vendorinventory.db"

    if not os.path.exists(db_path):
        raise FileNotFoundError(
            f"Database not found: {db_path}. "
            "Run ingestion_db.py first."
        )

    conn = sqlite3.connect(db_path)

    try:
        logging.info("Creating Vendor Summary Table.......")
        summary_df = create_vendor_summary(conn)
        logging.info("Raw summary rows: %s", len(summary_df))

        logging.info("Cleaning Data.......")
        clean_df = clean_data(summary_df)

        logging.info("Ingesting data into vendor_sales_summary.......")

        clean_df.to_sql(
            "vendor_sales_summary",
            conn,
            if_exists="replace",
            index=False,
            chunksize=1000
        )

        logging.info("Vendor summary table created successfully.")
        logging.info("Total rows: %s", len(clean_df))

        print("Vendor summary created successfully.")
        print(f"Total rows: {len(clean_df):,}")
        print("Table: vendor_sales_summary")
        print("Database: vendorinventory.db")
        print("Log: logs/get_vendor_summary.log")

    except Exception:
        logging.exception("Vendor summary creation failed.")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
