import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import os


# Check if the directory exists and create if it doesn't
desktop_path = "E:/Project 234/Project_cinema_retail_operation1"
if not os.path.exists(desktop_path):
    os.makedirs(desktop_path)
    print(f"Directory created at: {desktop_path}")
else:
    print(f"Directory already exists at: {desktop_path}")

# Define file paths
customers_file_path = os.path.join(desktop_path, "cinema_customers_india_updated.csv")
transactions_file_path = os.path.join(desktop_path, "cinema_transactions_updated.csv")
merged_file_path = os.path.join(desktop_path, "cinema_merged_data_updated.csv")



# Return file paths for confirmation
customers_file_path, transactions_file_path, merged_file_path

# Initialize Faker with localization for India
fake = Faker('en_IN')

# Function to generate customer data
def generate_cinema_customers_india(n_customers):
    customer_ids = [f"CUST{i:05d}" for i in range(1, n_customers + 1)]
    names = [fake.name() for _ in range(n_customers)]
    ages = [random.randint(18, 65) for _ in range(n_customers)]
    genders = [random.choice(["Male", "Female"]) for _ in range(n_customers)]
    occupations = np.random.choice(["Student", "Employee", "Self-Employed", "Retired"], size=n_customers)
    locations = np.random.choice(["Tier_1", "Tier_2", "Tier_3"], size=n_customers)
    preferred_snacks = [random.choice(["Popcorn", "Samosa", "Cold Drink", "Nachos", "Ice Cream"]) for _ in range(n_customers)]
    visitation_frequency = [random.choice(["Weekly", "Monthly", "Quarterly", "Yearly"]) for _ in range(n_customers)]
    membership_types = np.random.choice(["Basic", "Premium", "Gold"], size=n_customers)
    membership_status = [random.choice(["Member", "Non-Member"]) for _ in range(n_customers)]
    incomes = np.random.choice([300000, 500000, 700000, 1000000], size=n_customers)  # In INR
    loyalty_points = [random.randint(0, 1000) for _ in range(n_customers)]

    return pd.DataFrame({
        "Customer_ID": customer_ids,
        "Customer_Name": names,
        "Age": ages,
        "Gender": genders,
        "Occupation": occupations,
        "Location": locations,
        "Income": incomes,
        "Preferred_Snacks": preferred_snacks,
        "Visitation_Frequency": visitation_frequency,
        "Membership_Type": membership_types,
        "Membership_Status": membership_status,
        "Loyalty_Points": loyalty_points
    })

# Function to generate transaction data
def generate_cinema_transactions_india(customers, n_transactions):
    transaction_data = []
    for _ in range(n_transactions):
        customer_id = random.choice(customers)
        transaction_id = f"TXN{random.randint(1000000, 9999999)}"
        transaction_date = datetime.now() - timedelta(days=random.randint(1, 365))
        ticket_price = random.choice([150, 250, 350, 450])
        category = random.choice(["Ticket", "Snacks", "Merchandise"])
        amount = round(random.uniform(100, 5000), 2)
        quantity = random.randint(1, 10)
        discount_applied = round(random.uniform(0, 0.3) * amount, 2)  # Discount up to 30%
        snacks_purchased = random.choice([0, 1])  # Whether they bought snacks or not
        snack_amount = random.choice([0, 50, 100, 150]) * snacks_purchased

        transaction_data.append({
            "Transaction_ID": transaction_id,
            "Customer_ID": customer_id,
            "Transaction_Date": transaction_date,
            "Ticket_Price": ticket_price,
            "Amount": amount,
            "Category": category,
            "Quantity": quantity,
            "Discount_Applied": discount_applied,
            "Snacks_Purchased": snacks_purchased,
            "Snack_Amount": snack_amount
        })

    return pd.DataFrame(transaction_data)

# RFM Calculation function
def calculate_rfm(transactions_df):
    today = datetime.today()

    # Recency: Days since last transaction
    recency = transactions_df.groupby('Customer_ID')['Transaction_Date'].max().reset_index()
    recency['Recency'] = (today - pd.to_datetime(recency['Transaction_Date'])).dt.days

    # Frequency: Number of transactions
    frequency = transactions_df.groupby('Customer_ID').size().reset_index(name='Frequency')

    # Monetary: Total amount spent
    monetary = transactions_df.groupby('Customer_ID')['Amount'].sum().reset_index(name='Monetary')

    # Merge RFM Data
    rfm_df = pd.merge(recency, frequency, on='Customer_ID')
    rfm_df = pd.merge(rfm_df, monetary, on='Customer_ID')

    return rfm_df

# Generate customers and transactions
n_customers = 2000  # Number of customers
n_transactions = 10000  # Number of transactions

cinema_customers_df = generate_cinema_customers_india(n_customers)
cinema_transactions_df = generate_cinema_transactions_india(cinema_customers_df["Customer_ID"].tolist(), n_transactions)

# Calculate RFM metrics
rfm_df = calculate_rfm(cinema_transactions_df)

# Merge customer and transaction data with RFM
cinema_merged_df = pd.merge(cinema_transactions_df, cinema_customers_df, on="Customer_ID", how="left")
cinema_merged_df = pd.merge(cinema_merged_df, rfm_df, on="Customer_ID", how="left")

# Directory paths to be created
directory_path = "E:/Project 234/Project_cinema_retail_operation"

# Create the directory if it doesn't exist
try:
    os.makedirs(directory_path, exist_ok=True)
    print(f"Directory created or already exists at: {directory_path}")
except Exception as e:
    print(f"An error occurred while creating the directory: {e}")

# Save datasets
cinema_customers_df.to_csv(customers_file_path, index=False)
cinema_transactions_df.to_csv(transactions_file_path, index=False)
cinema_merged_df.to_csv(merged_file_path, index=False)

cinema_customers_df.to_csv(customers_file_path, index=False)
cinema_transactions_df.to_csv(transactions_file_path, index=False)
cinema_merged_df.to_csv(merged_file_path, index=False)

# Return file paths for confirmation
customers_file_path, transactions_file_path, merged_file_path

