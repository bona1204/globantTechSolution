# DB Migration API with FastAPI & MySQL

This project implements a local REST API using FastAPI and SQLAlchemy to handle the migration of data for three related tables: `departments`, `jobs`, and `hired_employees`.

## Features

- Receives historical data from CSV files.
- Uploads this data to a SQL database (MySQL).
- Supports batch inserts (up to 1000 rows per request).
- Automatically splits large files into multiple transactions if necessary.
- Uses Docker containers for easy local setup.

## Technologies Used

- FastAPI  
- SQLAlchemy  
- MySQL 8  
- Docker & Docker Compose  
- Python 3.10  
- Pandas

## Requirements

- Docker  
- Docker Compose

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/bona1204/globantTechSolution.git
    cd globantTechSolution
    ```

2. Start the containers:

    ```bash
    docker-compose up --build
    ```

This will launch:

- A MySQL container with a database named `globant_db`.
- The FastAPI backend available at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Usage

To upload a CSV file, send a POST request to:

http://localhost:8000/upload/{table_name}

Valid values for `{table_name}`:

- `departments`
- `jobs`
- `hired_employees`

Example using `curl`:

```bash
curl -X POST http://localhost:8000/upload/departments

Notes
CSV files must be placed in the data/ folder.

CSV files should not have a header row.

The database schema is auto-generated on startup.

hired_employees data is inserted in batches of up to 1000 records per insert. If a file has more than 1000 rows, it is split and processed in multiple chunks during the same request.

## API Endpoints

### Upload Historical Data

**POST** `/upload/{table_name}`  
Uploads historical data from a CSV file located in the `data/` folder.

### Accepted values for `{table_name}`

- `departments`
- `jobs`
- `hired_employees`


### Report: Hires by Department and Job (per quarter)

**GET** `/report/hired_employees_by_quarter`  
Returns a summary of how many people were hired per department and job in each quarter of 2021.

### Report: Top 10 Departments by Hires in 2021

**GET** `/report/top_10_departments`  
Returns the top 10 departments with the most hires in 2021.