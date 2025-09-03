# Financial Data Generator

This Python script generates realistic financial data with intentional data quality issues to simulate real-world scenarios for data strategy and quality analysis.

## Overview

The script generates **20,000+ unique records** across four relational tables:

1. **customers.csv** - Customer demographic and financial information
2. **accounts.csv** - Bank account details linked to customers  
3. **transactions.csv** - Transaction history linked to accounts
4. **credit_history.csv** - Credit score history linked to customers

## Features

### Relational Structure
- **Customers** → **Accounts** (One-to-Many)
- **Accounts** → **Transactions** (One-to-Many)  
- **Customers** → **Credit History** (One-to-Many)

### Data Quality Issues Introduced
- **Missing Values**: 2-6% of records have missing data in various fields
- **Invalid Formats**: Invalid email addresses, phone numbers, dates
- **Duplicate Records**: 1-2% of records are intentionally duplicated
- **Orphaned References**: Some accounts reference non-existent customers
- **Future Dates**: Some records have dates in the future
- **Negative Values**: Inappropriate negative values in certain fields
- **Invalid Data Types**: Non-numeric values in numeric fields

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the data generation script:

```bash
python generate_financial_data.py
```

This will create four CSV files in the current directory:
- `customers.csv` (~5,100 records)
- `accounts.csv` (~8,080 records)  
- `transactions.csv` (~20,200 records)
- `credit_history.csv` (~12,000 records)

## Data Schema

### Customers Table
| Field | Type | Description | Quality Issues |
|-------|------|-------------|----------------|
| customer_id | UUID | Unique customer identifier | None |
| first_name | String | Customer first name | 5% missing |
| last_name | String | Customer last name | 3% missing |
| email | String | Email address | 4% invalid format |
| phone | String | Phone number | 6% missing |
| ssn | String | Social Security Number | 2% invalid format |
| date_of_birth | Date | Date of birth | None |
| address | String | Street address | 3% missing |
| city | String | City | 4% missing |
| state | String | State/Province | 2% missing |
| zip_code | String | Postal code | 5% missing |
| country | String | Country | None |
| annual_income | Float | Annual income | 3% negative values |
| employment_status | String | Employment status | None |
| credit_score | Integer | Credit score (300-850) | 2% invalid range |
| credit_range | String | Credit score category | None |
| created_date | DateTime | Account creation date | None |

### Accounts Table
| Field | Type | Description | Quality Issues |
|-------|------|-------------|----------------|
| account_id | UUID | Unique account identifier | None |
| customer_id | UUID | Foreign key to customers | 1% orphaned |
| account_type | String | Type of account | 2% invalid values |
| account_number | String | Account number | 4% missing |
| routing_number | String | Bank routing number | 3% missing |
| balance | Float | Current balance | 5% missing |
| credit_limit | Float | Credit limit (if applicable) | None |
| interest_rate | Float | Interest rate (if applicable) | None |
| status | String | Account status | 3% missing |
| opened_date | DateTime | Account opening date | 4% future dates |

### Transactions Table
| Field | Type | Description | Quality Issues |
|-------|------|-------------|----------------|
| transaction_id | UUID | Unique transaction identifier | None |
| account_id | UUID | Foreign key to accounts | None |
| transaction_type | String | Type of transaction | 3% missing |
| amount | Float | Transaction amount | 6% missing, 4% negative |
| description | String | Transaction description | 5% missing |
| merchant_name | String | Merchant name (if applicable) | None |
| merchant_category | String | Merchant category | None |
| transaction_date | DateTime | Transaction date | 2% future dates |
| status | String | Transaction status | 4% missing |
| reference_number | String | Reference number | None |
| authorization_code | String | Authorization code | None |
| location | String | Transaction location | 3% missing |

### Credit History Table
| Field | Type | Description | Quality Issues |
|-------|------|-------------|----------------|
| credit_history_id | UUID | Unique identifier | None |
| customer_id | UUID | Foreign key to customers | None |
| credit_score | Integer | Credit score | 3% missing, 2% invalid |
| credit_bureau | String | Credit bureau | 4% missing |
| score_date | DateTime | Date of credit score | None |

## Data Quality Analysis

The script includes a built-in data quality report that shows:
- Total records and columns per table
- Missing value counts and percentages
- Duplicate record counts
- Column-wise missing value analysis

## Use Cases

This dataset is ideal for:
- **Data Quality Assessment**: Practice identifying and fixing data quality issues
- **Data Strategy Development**: Test data governance and management approaches
- **Analytics Training**: Learn data cleaning and preprocessing techniques
- **Compliance Testing**: Practice handling financial data regulations
- **Machine Learning**: Train models on realistic financial data with quality issues

## Customization

You can modify the script to:
- Change the number of records generated
- Adjust the percentage of data quality issues
- Add new fields or tables
- Modify the types of quality issues introduced
- Change the date ranges and value distributions

## Notes

- All data is synthetic and generated using the Faker library
- Customer IDs, account IDs, and transaction IDs are UUIDs for uniqueness
- The script uses random seeds for reproducible results
- Data quality issues are intentionally introduced to simulate real-world scenarios
- The relational structure mimics typical financial institution databases

## License

This script is provided for educational and research purposes. Please ensure compliance with data privacy regulations when using or modifying the generated data.
