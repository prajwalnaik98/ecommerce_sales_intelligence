# analyze_sales.py
#
# E-commerce Sales Intelligence
#
# This script answers seven business questions for an online store, using three
# raw, messy CSV files (orders, products, customers) as input:
#   1. How is our monthly revenue trending?
#   2. What are our best-selling products?
#   3. Which city + category combinations bring in the most revenue?
#   4. Who are our most valuable customers?
#   5. What is the average value of a typical order?
#   6. Which products are sitting unsold in stock?
#   7. How is our customer base growing over time?
#
# The script reads the raw data, cleans it up (fixing date formats, removing
# duplicates, filling in missing values, etc.), combines everything into one
# master dataset, and then runs the analysis above. Results are printed to
# the screen and saved into the outputs/ folder as a CSV file and a JSON report.

import json
from pathlib import Path

import pandas as pd


def setup_folders():
    """
    Make sure the outputs/ folder exists, so we have somewhere to save
    our results. pathlib's mkdir() with exist_ok=True will not raise an
    error if the folder is already there.
    """
    outputs_folder = Path("outputs")
    outputs_folder.mkdir(exist_ok=True)
    print("outputs/ folder is ready.")


def load_data():
    """
    Read orders.csv, products.csv, and customers.csv from the data/ folder.
    If any file is missing or empty, print a clear error message and stop
    the program instead of continuing with bad data.
    Returns three DataFrames: orders_df, products_df, customers_df.
    """
    data_folder = Path("data")

    try:
        orders_df = pd.read_csv(data_folder / "orders.csv")
        products_df = pd.read_csv(data_folder / "products.csv")
        customers_df = pd.read_csv(data_folder / "customers.csv")
    except FileNotFoundError as error:
        print(f"Error: could not find one of the data files. Details: {error}")
        raise
    except pd.errors.EmptyDataError as error:
        print(f"Error: one of the data files is empty. Details: {error}")
        raise

    print(
        f"Loaded {len(orders_df)} order rows, {len(products_df)} product rows, "
        f"{len(customers_df)} customer rows."
    )
    return orders_df, products_df, customers_df


def clean_orders(df):
    """
    Clean the raw orders DataFrame:
    - Parse order_date, handling both the YYYY-MM-DD and DD-MM-YYYY formats.
    - Remove exact duplicate rows.
    - Drop rows where customer_id is missing (we cannot link these orders
      to a customer, so they are not useful for analysis).
    - Clean up the order_status text (extra spaces and inconsistent casing).
    - Fix the data type of the quantity column.
    Returns the cleaned DataFrame.
    """
    cleaned_df = df.copy()

    # Step 1: try to parse order_date assuming the YYYY-MM-DD format first.
    parsed_main_format = pd.to_datetime(
        cleaned_df["order_date"], format="%Y-%m-%d", errors="coerce"
    )

    # Step 2: for any dates that failed to parse above, try the DD-MM-YYYY format.
    parsed_alt_format = pd.to_datetime(
        cleaned_df["order_date"], format="%d-%m-%Y", errors="coerce"
    )

    # Step 3: combine the two results. Where the main format worked, keep it.
    # Where it did not (it is still empty/NaT), fill it in with the alt format result.
    cleaned_df["order_date"] = parsed_main_format.fillna(parsed_alt_format)

    # Step 4: count and remove exact duplicate rows (every column matches).
    number_of_duplicates = cleaned_df.duplicated().sum()
    cleaned_df = cleaned_df.drop_duplicates()
    print(f"clean_orders: removed {number_of_duplicates} duplicate rows.")

    # Step 5: count and drop rows where customer_id is missing.
    number_missing_customer = cleaned_df["customer_id"].isna().sum()
    cleaned_df = cleaned_df.dropna(subset=["customer_id"])
    print(f"clean_orders: removed {number_missing_customer} rows with missing customer_id.")

    # Step 6: clean up order_status text - remove extra spaces and make casing consistent.
    cleaned_df["order_status"] = cleaned_df["order_status"].str.strip().str.title()

    # Step 7: fix data types now that the messy rows are gone.
    cleaned_df["quantity"] = cleaned_df["quantity"].astype(int)
    cleaned_df["customer_id"] = cleaned_df["customer_id"].astype(str)

    return cleaned_df


def clean_products(df):
    """
    Clean the raw products DataFrame:
    - Clean up the category text (extra spaces and inconsistent casing).
    - Fill missing price values with the average price for that product's category.
    Returns the cleaned DataFrame.
    """
    cleaned_df = df.copy()

    # Clean up category text first. We do this before filling in missing prices,
    # so that messy text (like " electronics " and "ELECTRONICS") does not
    # accidentally create extra, fake categories when we group by category below.
    cleaned_df["category"] = cleaned_df["category"].str.strip().str.title()

    # Calculate the average price for each category using groupby() and agg().
    # Missing prices (NaN) are automatically ignored by mean().
    category_average_price = cleaned_df.groupby("category")["price"].agg("mean")

    # Look up the matching category average price for every row.
    average_price_for_each_row = cleaned_df["category"].map(category_average_price)

    # Count and fill in missing prices using the category average we just looked up.
    number_missing_price = cleaned_df["price"].isna().sum()
    cleaned_df["price"] = cleaned_df["price"].fillna(average_price_for_each_row)
    print(f"clean_products: filled {number_missing_price} missing price values using category averages.")

    # Fix data type and round to 2 decimal places, since this is a money column.
    cleaned_df["price"] = cleaned_df["price"].astype(float).round(2)

    return cleaned_df


def clean_customers(df):
    """
    Clean the raw customers DataFrame:
    - Clean up the city text (extra spaces and inconsistent casing).
    - Parse signup_date, handling both the YYYY-MM-DD and DD-MM-YYYY formats.
    - Fill missing email addresses with the placeholder text "not provided".
    Returns the cleaned DataFrame.
    """
    cleaned_df = df.copy()

    # Clean up city text - remove extra spaces and make casing consistent.
    cleaned_df["city"] = cleaned_df["city"].str.strip().str.title()

    # Parse signup_date the same way we parsed order_date: try the main format
    # first, then fall back to the alternate format for anything that failed.
    parsed_main_format = pd.to_datetime(
        cleaned_df["signup_date"], format="%Y-%m-%d", errors="coerce"
    )
    parsed_alt_format = pd.to_datetime(
        cleaned_df["signup_date"], format="%d-%m-%Y", errors="coerce"
    )
    cleaned_df["signup_date"] = parsed_main_format.fillna(parsed_alt_format)

    # Count and fill in missing email addresses with a clear placeholder.
    number_missing_email = cleaned_df["email"].isna().sum()
    cleaned_df["email"] = cleaned_df["email"].fillna("not provided")
    print(f"clean_customers: filled {number_missing_email} missing email values with 'not provided'.")

    return cleaned_df


def build_master_dataset(orders_df, products_df, customers_df):
    """
    Merge the cleaned orders, products, and customers DataFrames into one
    master DataFrame, and add a revenue column (quantity x price).
    Returns the merged master DataFrame.
    """
    # We use a LEFT join here, with orders as the base (left) table.
    # This keeps every cleaned order, even in the unlikely case a customer_id
    # does not have a matching row in customers.csv. An inner join could
    # silently drop valid orders if that ever happened.
    master_df = orders_df.merge(customers_df, on="customer_id", how="left")

    # We use an INNER join here because every product_id remaining in our
    # cleaned orders should match a real row in products.csv. Using an inner
    # join also acts as a safety check: if a product_id did not match anything,
    # that order row would be dropped instead of silently keeping incomplete data.
    master_df = master_df.merge(products_df, on="product_id", how="inner")

    # Add a revenue column: how much money this order line is worth.
    master_df["revenue"] = master_df["quantity"] * master_df["price"]

    return master_df


def monthly_revenue(master_df):
    """
    Calculate total revenue per month using resampling. Only "Delivered"
    orders count as real revenue, since Cancelled, Returned, and Pending
    orders did not result in a completed sale.
    Adds a month-over-month growth percentage column.
    Returns a DataFrame with one row per month.
    """
    delivered_df = master_df[master_df["order_status"] == "Delivered"].copy()

    # Resampling needs a DatetimeIndex, so we set order_date as the index.
    delivered_df = delivered_df.set_index("order_date")

    # Resample by month start ("MS") and add up the revenue for each month.
    monthly_series = delivered_df["revenue"].resample("MS").sum()
    monthly_df = monthly_series.to_frame()

    # Calculate month-over-month growth percentage.
    monthly_df["growth_percent"] = monthly_df["revenue"].pct_change() * 100
    monthly_df["growth_percent"] = monthly_df["growth_percent"].round(2)

    # Reset the index so "order_date" becomes a normal column, and rename it to "month".
    monthly_df = monthly_df.reset_index()
    monthly_df = monthly_df.rename(columns={"order_date": "month"})

    return monthly_df


def top_products(master_df, n=10):
    """
    Find the top n products by total revenue, counting only Delivered orders.
    Returns a DataFrame sorted from highest to lowest revenue.
    """
    delivered_df = master_df[master_df["order_status"] == "Delivered"]

    # Group by product and add up the revenue and quantity sold for each one.
    product_summary = delivered_df.groupby(["product_id", "product_name", "category"]).agg(
        total_revenue=("revenue", "sum"),
        total_quantity_sold=("quantity", "sum"),
    )
    product_summary = product_summary.reset_index()

    # Sort so the highest revenue products come first, and keep only the top n.
    product_summary = product_summary.sort_values(by="total_revenue", ascending=False)
    top_n_products = product_summary.head(n)
    top_n_products = top_n_products.reset_index(drop=True)

    return top_n_products


def city_category_breakdown(master_df):
    """
    Build a pivot table showing total revenue by city (rows) and category
    (columns), counting only Delivered orders.
    Returns the pivot table as a DataFrame.
    """
    delivered_df = master_df[master_df["order_status"] == "Delivered"]

    pivot_df = pd.pivot_table(
        delivered_df,
        values="revenue",
        index="city",
        columns="category",
        aggfunc="sum",
        fill_value=0,
    )

    return pivot_df


def top_customers(master_df, n=20):
    """
    Find the top n customers by total amount spent, counting only Delivered
    orders. Also calculates the overall average order value.
    Returns a tuple: (top_customers_df, average_order_value).
    """
    delivered_df = master_df[master_df["order_status"] == "Delivered"]

    customer_summary = delivered_df.groupby(["customer_id", "customer_name", "city"]).agg(
        total_spent=("revenue", "sum"),
        number_of_orders=("order_id", "count"),
    )
    customer_summary = customer_summary.reset_index()
    customer_summary = customer_summary.sort_values(by="total_spent", ascending=False)
    top_n_customers = customer_summary.head(n)
    top_n_customers = top_n_customers.reset_index(drop=True)

    # Average order value = total delivered revenue divided by number of delivered orders.
    total_delivered_revenue = delivered_df["revenue"].sum()
    total_delivered_orders = delivered_df["order_id"].count()
    average_order_value = total_delivered_revenue / total_delivered_orders
    average_order_value = float(round(average_order_value, 2))

    return top_n_customers, average_order_value


def unsold_products(products_df, orders_df):
    """
    Find products that are marked in_stock but never appear in any order.
    Uses a left join with an indicator column to spot products that have
    no matching rows in orders.csv at all.
    Returns a DataFrame of those unsold, in-stock products.
    """
    merged_df = products_df.merge(
        orders_df[["product_id", "order_id"]],
        on="product_id",
        how="left",
        indicator=True,
    )

    # "_merge" tells us whether each row matched an order or not.
    # "left_only" means this product never appeared in orders.csv.
    never_ordered = merged_df[merged_df["_merge"] == "left_only"]
    never_ordered_in_stock = never_ordered[never_ordered["in_stock"] == True]

    # Keep only the useful columns, and drop duplicate product rows.
    result_df = never_ordered_in_stock[["product_id", "product_name", "category", "price"]]
    result_df = result_df.drop_duplicates()
    result_df = result_df.reset_index(drop=True)

    return result_df


def customer_signup_trend(customers_df):
    """
    Count how many new customers signed up each month.
    Returns a DataFrame with one row per month, showing the year, month,
    and number of new signups, sorted in time order.
    """
    trend_df = customers_df.copy()

    # Extract just the year and month from signup_date using the .dt accessor.
    trend_df["signup_year"] = trend_df["signup_date"].dt.year
    trend_df["signup_month"] = trend_df["signup_date"].dt.month

    # Group by year and month, and count how many customers signed up in each one.
    monthly_counts = trend_df.groupby(["signup_year", "signup_month"]).agg(
        new_signups=("customer_id", "count")
    )
    monthly_counts = monthly_counts.reset_index()

    # Sort the results in time order (earliest month first).
    monthly_counts = monthly_counts.sort_values(by=["signup_year", "signup_month"])
    monthly_counts = monthly_counts.reset_index(drop=True)

    return monthly_counts


def save_master_dataset(master_df):
    """Save the cleaned, merged master dataset to outputs/master_data.csv."""
    output_path = Path("outputs") / "master_data.csv"
    master_df.to_csv(output_path, index=False)
    print(f"Saved master dataset to {output_path}")


def save_business_report(monthly_rev, top_prod, city_cat, top_cust, avg_order_value, unsold, signup_trend):
    """
    Save all of the business analysis results into one structured JSON
    file at outputs/business_report.json.
    """
    # Turn the "month" column (a date) into plain text, since JSON cannot
    # store pandas Timestamp objects directly.
    monthly_rev_copy = monthly_rev.copy()
    monthly_rev_copy["month"] = monthly_rev_copy["month"].dt.strftime("%Y-%m")

    # Turn the monthly revenue table into a list of plain dictionaries.
    monthly_revenue_records = monthly_rev_copy.to_dict(orient="records")

    # The first month has no previous month to compare to, so its growth
    # percentage is missing (NaN). Replace that with None so it is saved
    # as a valid "null" value in the JSON file instead of an invalid number.
    for record in monthly_revenue_records:
        if pd.isna(record["growth_percent"]):
            record["growth_percent"] = None

    # Build a readable "YYYY-MM" month label for the signup trend table.
    signup_trend_copy = signup_trend.copy()
    month_labels = []
    for row_index, row in signup_trend_copy.iterrows():
        year = int(row["signup_year"])
        month = int(row["signup_month"])
        month_labels.append(f"{year}-{month:02d}")
    signup_trend_copy["month"] = month_labels

    # Put every result into one dictionary. Each DataFrame is turned into a
    # JSON-friendly list of records (or a dict, for the city x category table).
    report = {
        "monthly_revenue": monthly_revenue_records,
        "top_products": top_prod.to_dict(orient="records"),
        "city_category_revenue": city_cat.to_dict(orient="index"),
        "top_customers": top_cust.to_dict(orient="records"),
        "average_order_value": avg_order_value,
        "unsold_products": unsold.to_dict(orient="records"),
        "customer_signup_trend": signup_trend_copy[["month", "new_signups"]].to_dict(orient="records"),
    }

    # allow_nan=False makes json.dump raise an error instead of silently writing
    # an invalid "NaN" value, in case any other missing values slipped through.
    output_path = Path("outputs") / "business_report.json"
    with open(output_path, "w") as json_file:
        json.dump(report, json_file, indent=4, allow_nan=False)

    print(f"Saved business report to {output_path}")


def print_summary_report(monthly_rev, top_prod, city_cat, top_cust, avg_order_value, unsold, signup_trend):
    """
    Print a clean, readable summary in the terminal that answers all seven
    business questions in plain sentences.
    """
    print("\n" + "=" * 60)
    print("E-COMMERCE SALES INTELLIGENCE - SUMMARY REPORT")
    print("=" * 60)

    # Question 1: How is our monthly revenue trending?
    total_revenue = monthly_rev["revenue"].sum()
    best_month_row = monthly_rev.loc[monthly_rev["revenue"].idxmax()]
    latest_month_row = monthly_rev.iloc[-1]
    print("\n1. MONTHLY REVENUE TREND")
    print(f"   Total delivered revenue across all months: Rs {total_revenue:,.2f}")
    best_month_text = best_month_row["month"].strftime("%B %Y")
    print(f"   Best month: {best_month_text} with Rs {best_month_row['revenue']:,.2f} in revenue.")
    latest_month_text = latest_month_row["month"].strftime("%B %Y")
    if pd.isna(latest_month_row["growth_percent"]):
        print(f"   Latest month ({latest_month_text}) has no prior month to compare growth to.")
    else:
        print(f"   Latest month ({latest_month_text}) revenue changed by {latest_month_row['growth_percent']}% versus the previous month.")

    # Question 2: What are our best-selling products?
    print("\n2. TOP-SELLING PRODUCTS")
    print(f"   Our top {len(top_prod)} products by revenue are:")
    for row_index, row in top_prod.head(5).iterrows():
        print(f"     - {row['product_name']} ({row['category']}): Rs {row['total_revenue']:,.2f}")

    # Question 3: Which city + category combinations bring in the most revenue?
    best_city = None
    best_category = None
    best_combo_revenue = -1
    for city in city_cat.index:
        for category in city_cat.columns:
            revenue_value = city_cat.loc[city, category]
            if revenue_value > best_combo_revenue:
                best_combo_revenue = revenue_value
                best_city = city
                best_category = category
    print("\n3. CITY + CATEGORY REVENUE BREAKDOWN")
    print(f"   The strongest combination is {best_category} sales in {best_city}, worth Rs {best_combo_revenue:,.2f}.")

    # Question 4: Who are our most valuable customers?
    print("\n4. TOP CUSTOMERS")
    print(f"   Our top {len(top_cust)} customers by total spend include:")
    for row_index, row in top_cust.head(5).iterrows():
        print(f"     - {row['customer_name']} ({row['city']}): Rs {row['total_spent']:,.2f} across {row['number_of_orders']} orders.")

    # Question 5: What is the average value of a typical order?
    print("\n5. AVERAGE ORDER VALUE")
    print(f"   The average delivered order is worth Rs {avg_order_value:,.2f}.")

    # Question 6: Which products are sitting unsold in stock?
    print("\n6. UNSOLD PRODUCTS (in stock but never ordered)")
    print(f"   There are {len(unsold)} in-stock products that have never been ordered:")
    for row_index, row in unsold.head(5).iterrows():
        print(f"     - {row['product_name']} ({row['category']}), priced at Rs {row['price']:,.2f}")

    # Question 7: How is our customer base growing over time?
    total_signups = signup_trend["new_signups"].sum()
    latest_signup_row = signup_trend.iloc[-1]
    print("\n7. CUSTOMER SIGNUP TREND")
    print(f"   {total_signups} customers have signed up in total.")
    print(f"   In {int(latest_signup_row['signup_year'])}-{int(latest_signup_row['signup_month']):02d}, {latest_signup_row['new_signups']} new customers signed up.")

    print("\n" + "=" * 60)


def main():
    """Run the full e-commerce sales intelligence analysis, step by step."""
    print("E-commerce Sales Intelligence - starting analysis")
    print("=" * 60)

    print("\nStep 1: Setting up the outputs folder...")
    setup_folders()

    print("\nStep 2: Loading data files...")
    orders_df, products_df, customers_df = load_data()

    print("\nStep 3: Cleaning orders data...")
    orders_df = clean_orders(orders_df)

    print("\nStep 4: Cleaning products data...")
    products_df = clean_products(products_df)

    print("\nStep 5: Cleaning customers data...")
    customers_df = clean_customers(customers_df)

    print("\nStep 6: Building the master dataset...")
    master_df = build_master_dataset(orders_df, products_df, customers_df)
    print(f"   Master dataset has {len(master_df)} rows.")

    print("\nStep 7: Calculating monthly revenue trend...")
    monthly_rev = monthly_revenue(master_df)

    print("\nStep 8: Finding top products...")
    top_prod = top_products(master_df, n=10)

    print("\nStep 9: Building city x category revenue breakdown...")
    city_cat = city_category_breakdown(master_df)

    print("\nStep 10: Finding top customers and average order value...")
    top_cust, avg_order_value = top_customers(master_df, n=20)

    print("\nStep 11: Finding unsold products...")
    unsold = unsold_products(products_df, orders_df)

    print("\nStep 12: Calculating customer signup trend...")
    signup_trend = customer_signup_trend(customers_df)

    print("\nStep 13: Saving the master dataset...")
    save_master_dataset(master_df)

    print("\nStep 14: Saving the business report...")
    save_business_report(monthly_rev, top_prod, city_cat, top_cust, avg_order_value, unsold, signup_trend)

    print("\nStep 15: Printing summary report...")
    print_summary_report(monthly_rev, top_prod, city_cat, top_cust, avg_order_value, unsold, signup_trend)

    print("\nAnalysis complete! Check the outputs/ folder for saved files.")


if __name__ == "__main__":
    main()
