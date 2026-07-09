# E-commerce Sales Intelligence



## Project Overview

This project demonstrates a complete data cleaning and business analysis workflow using Python and Pandas. It simulates a real-world e-commerce scenario where order, product, and customer data is exported from different systems in inconsistent formats. The project cleans the data, merges it into a reliable master dataset, and generates business insights that can support data-driven decision-making.

---

## The Business Problem

Imagine you run a small online store. Every month you collect data about your
orders, your products, and your customers — but that data is exported from
different systems, on different days, by different people. The result is
messy: some dates are written as `2024-05-21` and others as `21-05-2024`,
some rows are accidentally duplicated, some customer IDs or product prices
are missing, and text fields like city or category have inconsistent spacing
and capitalization (`" mumbai"`, `"MUMBAI "`, `"Mumbai"`).

Before you can answer simple but important questions like:

- How are our sales performing?
- Which products generate the highest revenue?
- Which customers are most valuable?

You first need to clean the data and combine everything into one reliable,
analysis-ready dataset.

This project does exactly that. It takes three raw, messy CSV exports and
turns them into a single, clean dataset along with a business report that
answers seven real business questions.

---

## Business Questions Answered

1. How is our monthly revenue trending?
2. What are our best-selling products?
3. Which city + category combinations generate the most revenue?
4. Who are our most valuable customers?
5. What is the average value of a typical order?
6. Which products are currently unsold?
7. How is our customer base growing over time?

---

## What the Script Does

`analyze_sales.py` runs through the analysis in clear, well-commented steps:

1. **Set up folders** — ensures an `outputs/` directory exists.
2. **Load the data** — reads `orders.csv`, `products.csv`, and `customers.csv` with proper error handling.
3. **Clean the orders**
   - Standardizes multiple date formats.
   - Removes duplicate records.
   - Drops rows with missing customer IDs.
   - Cleans inconsistent order status values.
4. **Clean the products**
   - Standardizes category names.
   - Fills missing prices using the average price of the corresponding category.
5. **Clean the customers**
   - Standardizes signup dates.
   - Cleans city names.
   - Replaces missing email addresses with `"not provided"`.
6. **Build a master dataset**
   - Merges orders, products, and customers.
   - Creates a calculated `revenue` column.
7. **Run business analysis**
   - Monthly revenue trend
   - Best-selling products
   - Revenue by city and category
   - Top customers
   - Average order value
   - Unsold products
   - Customer signup trend
8. **Save outputs**
   - Writes the cleaned master dataset to CSV.
   - Saves all business insights to a JSON report.
9. **Print a summary**
   - Displays a plain-English summary answering all seven business questions.

A separate script, `generate_data.py`, was used to generate the sample messy
CSV files in the `data/` folder. You only need to run it if you want to
regenerate fresh sample data.

---

## Folder Structure

```text
ecommerce_sales_intelligence/
├── data/
│   ├── orders.csv          # Raw, messy order records
│   ├── products.csv        # Raw product catalog
│   └── customers.csv       # Raw customer records
├── outputs/                # Created automatically after running the analysis
│   ├── master_data.csv     # Cleaned and merged dataset
│   └── business_report.json# Business insights in JSON format
├── analyze_sales.py        # Main analysis script
├── generate_data.py        # Generates sample messy datasets
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Technologies Used

- Python 3
- Pandas
- NumPy
- JSON
- CSV

---

## How to Run the Project

1. Activate your virtual environment.
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the analysis:

```bash
python analyze_sales.py
```

4. The script will:

- Clean all datasets
- Merge them into a master dataset
- Perform business analysis
- Save the outputs
- Print a summary report in the terminal

If you want fresh sample data, simply run:

```bash
python generate_data.py
```

before running the analysis again.

---

## Output Files

After running `analyze_sales.py`, the `outputs/` folder will contain:

### `master_data.csv`

A cleaned and merged dataset containing order, product, and customer
information, ready for further analysis in Excel, Power BI, SQL, or Python.

### `business_report.json`

A structured report containing:

- Monthly revenue trend
- Best-selling products
- Revenue by city and category
- Top customers
- Average order value
- Unsold products
- Customer signup trend

The terminal also prints a clear, plain-English summary, allowing you to
understand the key business insights without opening the JSON report.
E-commerce Sales Intelligence - starting analysis
============================================================

Step 1: Setting up the outputs folder...
outputs/ folder is ready.

Step 2: Loading data files...
Loaded 1500 order rows, 79 product rows, 300 customer rows.

Step 3: Cleaning orders data...
clean_orders: removed 20 duplicate rows.
clean_orders: removed 15 rows with missing customer_id.

Step 4: Cleaning products data...
clean_products: filled 5 missing price values using category averages.

Step 5: Cleaning customers data...
clean_customers: filled 10 missing email values with 'not provided'.

Step 6: Building the master dataset...
   Master dataset has 1465 rows.

Step 7: Calculating monthly revenue trend...

Step 8: Finding top products...

Step 9: Building city x category revenue breakdown...

Step 10: Finding top customers and average order value...

Step 11: Finding unsold products...

Step 12: Calculating customer signup trend...

Step 13: Saving the master dataset...
Saved master dataset to outputs/master_data.csv

Step 14: Saving the business report...
Saved business report to outputs/business_report.json

Step 15: Printing summary report...

============================================================
E-COMMERCE SALES INTELLIGENCE - SUMMARY REPORT
============================================================

1. MONTHLY REVENUE TREND
   Total delivered revenue across all months: Rs 5,760,237.24
   Best month: February 2024 with Rs 539,630.57 in revenue.
   Latest month (March 2025) revenue changed by 56.74% versus the previous month.

2. TOP-SELLING PRODUCTS
   Our top 10 products by revenue are:
     - Phone Case (Electronics): Rs 343,297.94
     - Smartphone Stand (Electronics): Rs 308,593.04
     - Cricket Bat (Sports): Rs 279,014.50
     - Webcam (Electronics): Rs 268,468.90
     - Wireless Mouse (Electronics): Rs 266,403.09

3. CITY + CATEGORY REVENUE BREAKDOWN
   The strongest combination is Electronics sales in Ahmedabad, worth Rs 479,758.10.

4. TOP CUSTOMERS
   Our top 20 customers by total spend include:
     - Aman Nair (Kolkata): Rs 81,120.89 across 8 orders.
     - Rahul Nair (Ahmedabad): Rs 78,507.59 across 4 orders.
     - Kavya Patel (Ahmedabad): Rs 71,510.33 across 5 orders.
     - Reyansh Malhotra (Delhi): Rs 69,635.34 across 5 orders.
     - Myra Verma (Bangalore): Rs 67,375.24 across 6 orders.

5. AVERAGE ORDER VALUE
   The average delivered order is worth Rs 6,598.21.

6. UNSOLD PRODUCTS (in stock but never ordered)
   There are 10 in-stock products that have never been ordered:
     - Football (Sports), priced at Rs 3,117.38
     - Badminton Racket (Sports), priced at Rs 5,228.51
     - Skipping Rope (Sports), priced at Rs 2,460.15
     - Resistance Bands (Sports), priced at Rs 5,581.15
     - Running Shoes (Sports), priced at Rs 2,711.14

7. CUSTOMER SIGNUP TREND
   300 customers have signed up in total.
   In 2025-03, 11 new customers signed up.

============================================================

Analysis complete! Check the outputs/ folder for saved files.


## Project Highlights

- Data Cleaning
- Data Transformation
- Data Merging
- Missing Value Handling
- Duplicate Removal
- Business KPI Analysis
- Revenue Analysis
- Customer Analytics
- Product Performance Analysis
- JSON Report Generation
- CSV Processing
- Python Automation

---

## Author

**Prajwal Naik**
GitHub: https://github.com/prajwalnaik98
<br>
LinkedIn: www.linkedin.com/in/prajwal-naik-9362b0327
