# BrowserBank

A microservices-based banking application with Flask, gRPC, PostgreSQL, and Redis.

## Features

- Account management (register, login, delete account)
- Basic banking (deposit, withdraw, transfer money)
- Investment platform (stocks, bonds, futures trading)

## Requirements

- Python 3.7+
- PostgreSQL
- Redis
- Bun (for package management)

## Database Setup

The application requires PostgreSQL database with the following tables:

- customers_table
- stocks_table
- bonds_table
- futures_table
- customer_investments
- customer_futures

### Database Schema SQL

```sql
-- Create stocks table
CREATE TABLE stocks_table (
  symbol VARCHAR(10) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  price DECIMAL(10, 2) NOT NULL
);

-- Create bonds table
CREATE TABLE bonds_table (
  bond_id VARCHAR(10) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  yield DECIMAL(5, 2) NOT NULL,
  maturity DATE NOT NULL
);

-- Create futures table
CREATE TABLE futures_table (
  symbol VARCHAR(10) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  margin_req DECIMAL(4, 2) NOT NULL,
  expiry DATE NOT NULL
);

-- Create customer investments table
CREATE TABLE customer_investments (
  id SERIAL PRIMARY KEY,
  customer_name VARCHAR(50) NOT NULL,
  symbol VARCHAR(10) NOT NULL,
  type VARCHAR(10) NOT NULL,
  amount INTEGER NOT NULL
);

-- Create customer futures table
CREATE TABLE customer_futures (
  id SERIAL PRIMARY KEY,
  customer_name VARCHAR(50) NOT NULL,
  symbol VARCHAR(10) NOT NULL,
  amount INTEGER NOT NULL,
  position_type VARCHAR(5) NOT NULL,
  margin DECIMAL(10, 2) NOT NULL,
  open_price DECIMAL(10, 2) NOT NULL
);

-- Insert sample stocks
INSERT INTO stocks_table (symbol, name, price) VALUES
  ('AAPL', 'Apple Inc', 169.93),
  ('MSFT', 'Microsoft Corporation', 410.34),
  ('GOOGL', 'Alphabet Inc', 159.13),
  ('AMZN', 'Amazon.com Inc', 182.41),
  ('TSLA', 'Tesla Inc', 173.66);

-- Insert sample bonds
INSERT INTO bonds_table (bond_id, name, price, yield, maturity) VALUES
  ('T10Y', 'US 10 Year Treasury', 100.00, 4.50, '2034-04-01'),
  ('T5Y', 'US 5 Year Treasury', 100.00, 4.20, '2029-04-01'),
  ('T2Y', 'US 2 Year Treasury', 100.00, 3.90, '2026-04-01'),
  ('CORP1', 'Corporate Bond AA', 98.50, 5.10, '2030-06-01'),
  ('CORP2', 'Corporate Bond BBB', 97.00, 6.25, '2028-09-01');

-- Insert sample futures
INSERT INTO futures_table (symbol, name, price, margin_req, expiry) VALUES
  ('CL', 'Crude Oil', 83.17, 0.10, '2024-12-15'),
  ('GC', 'Gold', 2291.10, 0.10, '2024-12-15'),
  ('SI', 'Silver', 26.77, 0.10, '2024-12-15'),
  ('ES', 'S&P 500 E-mini', 5231.50, 0.05, '2024-06-15'),
  ('NQ', 'Nasdaq 100 E-mini', 18239.75, 0.05, '2024-06-15');
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd bankgrpcweb

# Install dependencies using bun
bun install

# Or if using pip
pip install flask flask-login psycopg2-binary redis grpc grpcio-tools
```

## Running the Application

The application consists of multiple microservices that need to be started separately:

### 1. Start the gRPC Authentication Service

```bash
bun run python startGrpcAuth.py
```

### 2. Start the gRPC Banking Service

```bash
bun run python startGrpcBank.py
```

### 3. Start the Flask Web Application

```bash
bun run python Startapp.py
```

## Accessing the Application

After starting all services, the application will be available at:

- http://localhost:5000

## Application Structure

- `main.py` - Core business logic for banking and investments
- `Startapp.py` - Flask web application entry point
- `startGrpcAuth.py` - Authentication service starter
- `startGrpcBank.py` - Banking service starter
- `bank/` - Banking microservice
- `reg_login/` - Authentication microservice
- `templates/` - HTML templates for the web interface
