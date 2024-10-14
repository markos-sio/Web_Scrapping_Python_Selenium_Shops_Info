Overview
This project automates the extraction of delivery service information from a website using Selenium for web scraping and Pandas for data manipulation.
It is designed to fetch data for multiple cities, gathering details such as:

Shop Names: The name of each delivery shop.

Service Type: Information about the type of service offered (e.g., delivery, takeout).

Delivery Times: Available delivery time windows for each shop.

Minimum Consumption: The minimum order amount required for placing a delivery.

Ratings: User ratings of the shop.

Number of Reviews: Total reviews received by the shop.

Delivery Costs: The cost of delivery for each shop.

The data is scraped from specific pages corresponding to delivery areas (e.g., Athens, Thessaloniki, Patra), and the extracted information is organized into Pandas DataFrames. These DataFrames are then saved to an Excel file, with each city having its own sheet.

Key Features:
Automated Web Scraping: Uses Selenium to load and parse web pages for multiple cities.

Detailed Data Extraction: Gathers relevant data about each delivery service, including shop details, delivery information, ratings, and costs.

Structured Data Output: Stores the data in an Excel file, organizing it into separate sheets for each city, providing clear and structured results for easy analysis.

Requirements

Python 3.10.9

Required libraries: pandas, selenium, xlsxwriter

ChromeDriver (matching your Chrome version)


