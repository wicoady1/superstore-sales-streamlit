# SuperSales Data Analysis

A Streamlit dashboard application for analyzing SuperSales data with interactive visualizations and filters.

## Project Structure

```
├── main.py              # Main application entry point
├── utils.py             # Shared utility functions
├── tabs/                # Directory for tab modules
│   ├── __init__.py      # Makes tabs a proper Python package
│   ├── dashboard.py     # Dashboard tab implementation
│   └── raw_data.py      # Raw data tab implementation
├── datasource/          # Data directory
│   └── supersales_data.csv  # Sample data file
├── Makefile             # Automation commands
└── requirements.txt     # Project dependencies
```

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```
   make install
   ```
   or
   ```
   pip install -r requirements.txt
   ```

## Running the Application

Use the Makefile to run the application:

```
make run
```

This will start the Streamlit server on port 8503 (default). You can access the dashboard at http://localhost:8503.

To run on a different port:

```
make run PORT=8000
```

## Available Makefile Commands

- `make run` - Run the Streamlit application (default port: 8503)
- `make run PORT=8000` - Run the Streamlit application on a specific port
- `make install` - Install required dependencies
- `make clean` - Clean up cache files
- `make help` - Display help information

## Features

- Interactive dashboard with KPIs and visualizations
- Raw data view with search functionality
- Filters for date range, region, and category
- Data export capability
- Responsive design

## Dashboard Components

- Monthly sales trend
- Sales by category
- Top 10 products
- Top 10 customers
- Key performance indicators