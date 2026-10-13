## Vendor Performance \& Inventory Analytics

An end-to-end data analytics project focused on analyzing vendor performance, inventory efficiency, purchasing behavior, sales, costs, and profitability to support data-driven business decisions.

## Business Problem

Effective inventory and sales management are critical for optimizing profitability in the retail and wholesale industry. Companies need to ensure that they are not incurring losses due to inefficient pricing, poor inventory turnover, or vendor dependency. The goal of this analysis is to:

* Identify underperforming brands that require promotional or pricing adjustments.
* Determine top vendors contributing to sales and gross profit.
* Analyze the impact of bulk purchasing on unit costs.
* Assess inventory turnover to reduce holding costs and improve efficiency.
* Investigate the profitability variance between high-performing and low-performing vendors.

\## Tech Stack



\- \*\*Python:\*\* Pandas, SQLAlchemy

\- \*\*Database:\*\* SQLite

\- \*\*Analytics:\*\* SQL, Jupyter Notebook

\- \*\*Visualization:\*\* Power BI



\## Project Structure



```text

Vendor-Performance-ETL-and-Analytics-Pipeline/

├── data/                           # Input CSV datasets (not tracked by Git)

├── EDA.ipynb                       # Exploratory Data Analysis

├── Vendor Performance Analysis.ipynb

├── ingestion\_db.py                 # Data ingestion pipeline

├── get\_vendor\_summary.py            # Vendor summary generation

├── README.md

└── .gitignore

```



\## Workflow



1\. Load source CSV files.

2\. Ingest the data into an SQLite database.

3\. Generate vendor performance summaries.

4\. Perform exploratory data analysis using Jupyter Notebook.

5\. Analyze sales, purchasing costs, gross profit, inventory turnover, and vendor performance.



\## Setup and Usage



1\. Clone this repository.

2\. Create and activate a Python virtual environment.

3\. Install the required Python dependencies.

4\. Place the required source CSV files in the `data/` directory.

5\. Run the ingestion and vendor summary scripts in the correct order.

6\. Open the notebooks in Jupyter to explore the analysis.



Install the main dependencies with:



```bash

pip install pandas sqlalchemy jupyter matplotlib seaborn

```



Additional dependencies may be required depending on the imports used in the scripts and notebooks.



\## Dataset Note



The source CSV datasets and generated SQLite database are excluded from Git because of their large size. Obtain the datasets from an authorized source and place them in the `data/` directory before running the pipeline.



\## Key Analysis Areas



\- Vendor and brand sales performance

\- Purchasing costs and bulk-purchasing impact

\- Gross profit and profitability

\- Inventory turnover and unsold inventory

\- Vendor contribution and performance comparisons

