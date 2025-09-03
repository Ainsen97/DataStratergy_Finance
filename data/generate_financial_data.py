#!/usr/bin/env python3
"""
Financial Data Generator with Data Quality Issues

This script generates 20,000 unique financial records across multiple relational tables
with intentional data quality issues to simulate real-world scenarios.

Author: Data Strategy Finance Project (Ai Assisted) 
Date: 2025
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid
import os

# Initialize Faker with multiple locales for diverse data
fake = Faker(['en_US', 'en_GB', 'en_CA', 'en_AU'])

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)
Faker.seed(42)

class FinancialDataGenerator:
    """Generate financial data with various data quality issues"""
    
    def __init__(self, num_customers=5000, num_accounts=8000, num_transactions=20000):
        self.num_customers = num_customers
        self.num_accounts = num_accounts
        self.num_transactions = num_transactions
        
        # Financial product types
        self.account_types = ['Checking', 'Savings', 'Credit Card', 'Investment', 'Loan', 'Mortgage']
        self.transaction_types = ['Deposit', 'Withdrawal', 'Transfer', 'Payment', 'Interest', 'Fee', 'Purchase']
        self.merchant_categories = ['Retail', 'Restaurant', 'Gas Station', 'Online', 'Healthcare', 'Entertainment', 'Travel', 'Utilities']
        
        # Credit score ranges
        self.credit_ranges = [(300, 579, 'Poor'), (580, 669, 'Fair'), (670, 739, 'Good'), (740, 799, 'Very Good'), (800, 850, 'Excellent')]
        
    def generate_customers(self):
        """Generate customer data with various data quality issues"""
        print("Generating customer data...")
        
        customers = []
        customer_ids = set()
        
        for i in range(self.num_customers):
            # Generate unique customer ID
            customer_id = str(uuid.uuid4())
            while customer_id in customer_ids:
                customer_id = str(uuid.uuid4())
            customer_ids.add(customer_id)
            
            # Basic customer information
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            phone = fake.phone_number()
            ssn = fake.ssn()
            date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
            address = fake.address().replace('\n', ', ')
            city = fake.city()
            state = fake.state()
            zip_code = fake.zipcode()
            country = fake.country()
            
            # Financial information
            annual_income = round(random.uniform(25000, 200000), 2)
            employment_status = random.choice(['Employed', 'Self-employed', 'Unemployed', 'Retired', 'Student'])
            
            # Credit information
            credit_score = random.randint(300, 850)
            credit_range = next((r[2] for r in self.credit_ranges if r[0] <= credit_score <= r[1]), 'Unknown')
            
            # Introduce data quality issues (approximately 5-10% of records)
            if random.random() < 0.05:  # 5% missing first name
                first_name = None
            if random.random() < 0.03:  # 3% missing last name
                last_name = None
            if random.random() < 0.04:  # 4% invalid email format
                email = fake.word() + '@invalid'
            if random.random() < 0.06:  # 6% missing phone
                phone = None
            if random.random() < 0.02:  # 2% invalid SSN format
                ssn = '000-00-0000'
            if random.random() < 0.03:  # 3% missing address
                address = None
            if random.random() < 0.04:  # 4% missing city
                city = None
            if random.random() < 0.02:  # 2% missing state
                state = None
            if random.random() < 0.05:  # 5% missing zip code
                zip_code = None
            if random.random() < 0.03:  # 3% negative income
                annual_income = -abs(annual_income)
            if random.random() < 0.02:  # 2% invalid credit score
                credit_score = random.randint(0, 299)  # Below valid range
            
            customer = {
                'customer_id': customer_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'ssn': ssn,
                'date_of_birth': date_of_birth,
                'address': address,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'country': country,
                'annual_income': annual_income,
                'employment_status': employment_status,
                'credit_score': credit_score,
                'credit_range': credit_range,
                'created_date': fake.date_time_between(start_date='-5y', end_date='now')
            }
            
            customers.append(customer)
        
        # Create DataFrame and add some duplicates (2% of records)
        df_customers = pd.DataFrame(customers)
        duplicates = df_customers.sample(frac=0.02, random_state=42)
        df_customers = pd.concat([df_customers, duplicates], ignore_index=True)
        
        return df_customers
    
    def generate_accounts(self, customers_df):
        """Generate account data linked to customers"""
        print("Generating account data...")
        
        accounts = []
        account_ids = set()
        customer_ids = customers_df['customer_id'].tolist()
        
        for i in range(self.num_accounts):
            # Generate unique account ID
            account_id = str(uuid.uuid4())
            while account_id in account_ids:
                account_id = str(uuid.uuid4())
            account_ids.add(account_id)
            
            # Link to customer
            customer_id = random.choice(customer_ids)
            
            # Account information
            account_type = random.choice(self.account_types)
            account_number = fake.credit_card_number()
            routing_number = fake.aba()
            balance = round(random.uniform(-50000, 100000), 2)  # Allow negative balances
            credit_limit = round(random.uniform(1000, 50000), 2) if account_type == 'Credit Card' else None
            interest_rate = round(random.uniform(0.5, 25.0), 2) if account_type in ['Savings', 'Credit Card', 'Loan', 'Mortgage'] else None
            status = random.choice(['Active', 'Inactive', 'Suspended', 'Closed'])
            opened_date = fake.date_time_between(start_date='-10y', end_date='now')
            
            # Introduce data quality issues
            if random.random() < 0.04:  # 4% missing account number
                account_number = None
            if random.random() < 0.03:  # 3% missing routing number
                routing_number = None
            if random.random() < 0.05:  # 5% missing balance
                balance = None
            if random.random() < 0.02:  # 2% invalid account type
                account_type = 'Invalid_Type'
            if random.random() < 0.03:  # 3% missing status
                status = None
            if random.random() < 0.04:  # 4% future opened date
                opened_date = fake.date_time_between(start_date='now', end_date='+1y')
            
            account = {
                'account_id': account_id,
                'customer_id': customer_id,
                'account_type': account_type,
                'account_number': account_number,
                'routing_number': routing_number,
                'balance': balance,
                'credit_limit': credit_limit,
                'interest_rate': interest_rate,
                'status': status,
                'opened_date': opened_date
            }
            
            accounts.append(account)
        
        df_accounts = pd.DataFrame(accounts)
        
        # Add some orphaned accounts (accounts without valid customer_id)
        orphaned_accounts = []
        for _ in range(int(self.num_accounts * 0.01)):  # 1% orphaned accounts
            orphaned_account = {
                'account_id': str(uuid.uuid4()),
                'customer_id': 'INVALID_CUSTOMER_ID',
                'account_type': random.choice(self.account_types),
                'account_number': fake.credit_card_number(),
                'routing_number': fake.aba(),
                'balance': round(random.uniform(0, 50000), 2),
                'credit_limit': None,
                'interest_rate': None,
                'status': 'Active',
                'opened_date': fake.date_time_between(start_date='-5y', end_date='now')
            }
            orphaned_accounts.append(orphaned_account)
        
        df_accounts = pd.concat([df_accounts, pd.DataFrame(orphaned_accounts)], ignore_index=True)
        
        return df_accounts
    
    def generate_transactions(self, accounts_df):
        """Generate transaction data linked to accounts"""
        print("Generating transaction data...")
        
        transactions = []
        transaction_ids = set()
        account_ids = accounts_df['account_id'].tolist()
        
        for i in range(self.num_transactions):
            # Generate unique transaction ID
            transaction_id = str(uuid.uuid4())
            while transaction_id in transaction_ids:
                transaction_id = str(uuid.uuid4())
            transaction_ids.add(transaction_id)
            
            # Link to account
            account_id = random.choice(account_ids)
            
            # Transaction information
            transaction_type = random.choice(self.transaction_types)
            amount = round(random.uniform(1, 10000), 2)
            description = fake.sentence(nb_words=6)
            merchant_name = fake.company() if transaction_type in ['Purchase', 'Payment'] else None
            merchant_category = random.choice(self.merchant_categories) if merchant_name else None
            transaction_date = fake.date_time_between(start_date='-2y', end_date='now')
            status = random.choice(['Completed', 'Pending', 'Failed', 'Cancelled'])
            
            # Reference numbers
            reference_number = fake.bothify(text='REF-####-????')
            authorization_code = fake.bothify(text='AUTH-######') if transaction_type in ['Purchase', 'Payment'] else None
            
            # Location information
            location = fake.city() + ', ' + fake.state()
            
            # Introduce data quality issues
            if random.random() < 0.06:  # 6% missing amount
                amount = None
            if random.random() < 0.04:  # 4% negative amount for non-withdrawal transactions
                if transaction_type not in ['Withdrawal', 'Payment', 'Fee'] and amount is not None:
                    amount = -abs(amount)
            if random.random() < 0.05:  # 5% missing description
                description = None
            if random.random() < 0.03:  # 3% missing transaction type
                transaction_type = None
            if random.random() < 0.04:  # 4% missing status
                status = None
            if random.random() < 0.02:  # 2% future transaction date
                transaction_date = fake.date_time_between(start_date='now', end_date='+1y')
            if random.random() < 0.03:  # 3% missing location
                location = None
            
            transaction = {
                'transaction_id': transaction_id,
                'account_id': account_id,
                'transaction_type': transaction_type,
                'amount': amount,
                'description': description,
                'merchant_name': merchant_name,
                'merchant_category': merchant_category,
                'transaction_date': transaction_date,
                'status': status,
                'reference_number': reference_number,
                'authorization_code': authorization_code,
                'location': location
            }
            
            transactions.append(transaction)
        
        df_transactions = pd.DataFrame(transactions)
        
        # Add some duplicate transactions (1% of records)
        duplicates = df_transactions.sample(frac=0.01, random_state=42)
        df_transactions = pd.concat([df_transactions, duplicates], ignore_index=True)
        
        return df_transactions
    
    def generate_credit_scores(self, customers_df):
        """Generate separate credit score history table"""
        print("Generating credit score history...")
        
        credit_history = []
        customer_ids = customers_df['customer_id'].tolist()
        
        for customer_id in customer_ids:
            # Generate 1-5 credit score records per customer
            num_records = random.randint(1, 5)
            
            for i in range(num_records):
                score_date = fake.date_time_between(start_date='-3y', end_date='now')
                credit_score = random.randint(300, 850)
                credit_bureau = random.choice(['Equifax', 'Experian', 'TransUnion'])
                
                # Introduce data quality issues
                if random.random() < 0.03:  # 3% missing credit score
                    credit_score = None
                if random.random() < 0.02:  # 2% invalid credit score
                    credit_score = random.randint(0, 299)
                if random.random() < 0.04:  # 4% missing bureau
                    credit_bureau = None
                
                credit_record = {
                    'credit_history_id': str(uuid.uuid4()),
                    'customer_id': customer_id,
                    'credit_score': credit_score,
                    'credit_bureau': credit_bureau,
                    'score_date': score_date
                }
                
                credit_history.append(credit_record)
        
        return pd.DataFrame(credit_history)
    
    def save_to_csv(self, dataframes, output_dir='data'):
        """Save all DataFrames to CSV files"""
        print("Saving data to CSV files...")
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Save each DataFrame
        for name, df in dataframes.items():
            filename = os.path.join(output_dir, f'{name}.csv')
            df.to_csv(filename, index=False)
            print(f"Saved {len(df)} records to {filename}")
    
    def generate_data_quality_report(self, dataframes):
        """Generate a data quality report for all datasets"""
        print("\n" + "="*60)
        print("DATA QUALITY REPORT")
        print("="*60)
        
        for name, df in dataframes.items():
            print(f"\n{name.upper()} Dataset:")
            print(f"Total Records: {len(df)}")
            print(f"Total Columns: {len(df.columns)}")
            print(f"Missing Values: {df.isnull().sum().sum()}")
            print(f"Duplicate Rows: {df.duplicated().sum()}")
            
            # Column-wise missing values
            missing_cols = df.isnull().sum()
            if missing_cols.sum() > 0:
                print("Missing Values by Column:")
                for col, missing in missing_cols[missing_cols > 0].items():
                    print(f"  {col}: {missing} ({missing/len(df)*100:.1f}%)")
            
            print("-" * 40)
    
    def run(self):
        """Generate all datasets and save to CSV"""
        print("Starting Financial Data Generation...")
        print(f"Target: {self.num_transactions} total records across multiple tables")
        print("="*60)
        
        # Generate all datasets
        customers_df = self.generate_customers()
        accounts_df = self.generate_accounts(customers_df)
        transactions_df = self.generate_transactions(accounts_df)
        credit_history_df = self.generate_credit_scores(customers_df)
        
        # Prepare dataframes dictionary
        dataframes = {
            'customers': customers_df,
            'accounts': accounts_df,
            'transactions': transactions_df,
            'credit_history': credit_history_df
        }
        
        # Save to CSV
        self.save_to_csv(dataframes)
        
        # Generate data quality report
        self.generate_data_quality_report(dataframes)
        
        print("\n" + "="*60)
        print("DATA GENERATION COMPLETE!")
        print("="*60)
        print(f"Total unique records generated: {len(customers_df) + len(accounts_df) + len(transactions_df) + len(credit_history_df)}")
        print("Files created in 'data' directory:")
        print("- customers.csv")
        print("- accounts.csv") 
        print("- transactions.csv")
        print("- credit_history.csv")
        print("\nData quality issues intentionally introduced:")
        print("- Missing values (2-6% per field)")
        print("- Invalid data formats")
        print("- Duplicate records")
        print("- Orphaned references")
        print("- Future dates")
        print("- Negative values where inappropriate")

if __name__ == "__main__":
    # Create generator instance
    generator = FinancialDataGenerator(
        num_customers=5000,
        num_accounts=8000, 
        num_transactions=20000
    )
    
    # Generate and save data
    generator.run()
