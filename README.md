# E-commerce Sales Intelligence

**Author:** Prajwal Naik

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

---

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
GitHub: https://github.com/your-github-username
