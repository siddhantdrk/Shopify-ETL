# Shopify ETL Project

This project implements an ETL pipeline to process Shopify order data and store it in ClickHouse for analytics.

## Project Structure
```
shopify_etl/
├── data/                   # Input data directory
├── src/                    # Source code
│   ├── models/            # Data models
│   ├── etl/               # ETL pipeline code
│   ├── database/          # Database related code
│   └── analytics/         # Analytics and metrics code
├── tests/                 # Test files
├── config/                # Configuration files
```

## Setup
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
CLICKHOUSE_HOST=127.0.0.1
CLICKHOUSE_PORT=9000
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=
CLICKHOUSE_DATABASE=default
```

## Running the Project
1. Start ClickHouse server
2. Run the ETL pipeline:
```bash
python src/main.py
```

## Development
- Use `black` for code formatting
- Use `isort` for import sorting
- Use `mypy` for type checking
- Write tests using `pytest` 
