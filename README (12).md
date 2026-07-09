# E-commerce Sales Intelligence

## The Business Problem

Imagine you run a small online store. Every month you collect data about your
orders, your products, and your customers — but that data is exported from
different systems, on different days, by different people. The result is
messy: some dates are written as `2024-05-21` and others as `21-05-2024`,
some rows are accidentally duplicated, some customer IDs or product prices
are missing, and text fields like city or category have inconsistent spacing
and capitalization (`" mumbai"`, `"MUMBAI "`, `"Mumbai"`).

Before you can answer simple but important questions like "what are our
best-selling products?" or "which customers should we focus on retaining?",
you first need to clean this data up and bring it all together into one
reliable dataset.

This project does exactly that. It takes three raw, messy CSV exports and
turns them into a single, clean dataset plus a business report that answers
seven real questions a store owner would care about:

1. How is our monthly revenue trending?
2. What are our best-selling products?
3. Which city + category combinations bring in the most revenue?
4. Who are our most valuable customers?
5. What is the average value of a typical order?
6. Which products are sitting unsold in stock?
7. How is our customer base growing over time?

## What the Script Does

`analyze_sales.py` runs through the analysis in clear, well-commented steps:

1. **Set up folders** — makes sure an `outputs/` folder exists.
2. **Load the data** — reads `orders.csv`, `products.csv`, and `customers.csv`,
   with error handling in case a file is missing.
3. **Clean the orders** — fixes the two different date formats, removes
   duplicate rows, drops orders with a missing customer ID, and tidies up
   the order status text.
4. **Clean the products** — tidies up the category text and fills in any
   missing prices using the average price for that product's category.
5. **Clean the customers** — fixes the date formats again, tidies up city
   text, and fills in missing emails with `"not provided"`.
6. **Build a master dataset** — merges orders, products, and customers
   together into one table, adding a `revenue` column.
7. **Run the analysis** — calculates monthly revenue trends, top products,
   a city-by-category revenue breakdown, top customers, average order
   value, unsold products, and customer signup trends.
8. **Save the results** — writes the cleaned master dataset to a CSV file
   and all of the analysis results to a single JSON report.
9. **Print a summary** — prints a plain-English summary in the terminal
   that answers all seven business questions.

A separate script, `generate_data.py`, was used to create the sample
"messy" CSV files in the `data/` folder. You do not need to run it again
unless you want to regenerate fresh sample data.

## Folder Structure

```
ecommerce_sales_intelligence/
├── data/
│   ├── orders.csv          # raw, messy order records
│   ├── products.csv        # raw product catalog
│   └── customers.csv       # raw customer records
├── outputs/                 # created automatically when you run the script
│   ├── master_data.csv      # cleaned, merged dataset
│   └── business_report.json # all analysis results in one file
├── analyze_sales.py          # the main analysis script
├── generate_data.py          # creates the sample messy CSV files
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Run It

1. Make sure your virtual environment is activated and the packages in
   `requirements.txt` are installed (pandas and numpy).
2. From the project folder, run:

   ```
   python analyze_sales.py
   ```

3. Watch the terminal — it prints a short progress message before each
   step, then a full summary report at the end.

If you ever want fresh sample data, you can run `python generate_data.py`
first to recreate the CSV files in `data/` before running the analysis.

## What to Expect in the Outputs

After running `analyze_sales.py`, check the `outputs/` folder for:

- **`master_data.csv`** — the cleaned dataset of all orders, joined with
  their product and customer details, ready for further analysis in Excel,
  Power BI, or any other tool.
- **`business_report.json`** — a structured file containing the monthly
  revenue trend, top products, city/category revenue breakdown, top
  customers, average order value, unsold products, and customer signup
  trend — all in one place.

The terminal output also gives you a plain-English summary, so you do not
need to open the JSON file just to understand the headline numbers.
