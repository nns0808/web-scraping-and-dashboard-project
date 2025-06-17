# web-scraping-and-dashboard-project
This project demonstrates:
- Web Scraping with Selenium  
- Data Cleaning with Pandas  
- Database Storage using SQLite  
- Interactive Dashboard using Dash & Plotly
web_scraping_and_dashboard_project/
│
├── web_scraping/
│ ├── web_scraping.py # Web scraper using Selenium
│ ├── import_csv_to_sqlite.py # CSV import into SQLite database
│ ├── mlb_dashboard.py # Interactive dashboard using Dash
│ ├── mlb_history_1902.csv # Scraped data (sample)
│ ├── mlb_history.db # SQLite database
│
├── requirements.txt # All required packages
└── README.md # This documentation
1. Web Scraping
Used Selenium to scrape MLB historical data from baseball-almanac.com.
Handled:
Missing HTML elements (with try/except blocks for missing tags).
Pagination by iterating through multiple year links.
Added user-agent header to simulate real browser access.
Collected raw data for different years.
Saved data into a CSV file (mlb_history_1902.csv) for further processing.
2. Data Cleaning & Transformation
Loaded CSV data into Pandas DataFrames.
Cleaned:
Missing fields.
Duplicate rows.
Malformed text or HTML tags.
Applied transformations:
Extracted year values from URLs.
Formatted columns for future analysis.
Ensured consistent data types (strings, integers, etc.).
Exported cleaned data for database import.
3. Database Storage
Created a SQLite database (mlb_history.db) to store cleaned data.
Wrote Python scripts to:
Automatically import CSV data into SQLite tables.
Create appropriate schema with column types.
Handle errors during import (e.g., duplicates or invalid entries).
4. Data Visualization Dashboard
Built an interactive dashboard using Dash (Plotly Dash).
Features:
Multiple visualizations (bar charts, pie charts, scatter plots).
Interactive dropdown menus for year selection.
Sliders to filter data by year range.
Dynamic visual updates when user changes filters.
Provided clean layout, titles, labels, and instructions for usability.
Runs locally on http://127.0.0.1:8050/.
5. Deployment 
Project deployed to Render.
screenshot: (https://github.com/user-attachments/assets/a2ffd669-31c0-4cc4-b05b-3689a80db4c1)



