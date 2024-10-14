# Google-Cloud-ETL-Pipeline
This project demonstrates how to build an ETL (Extract, Transform, Load) pipeline on Google Cloud using Cloud Functions, BigQuery, and Cloud Scheduler.
## Project Overview
- Extract: Retrieve data from external APIs (e.g., weather data from OpenWeather and flight information from AeroDataBox).
- Transform: Clean, process, and format the data using Pandas.
    - Load: Store the transformed data in:
        - A MySQL database (for local storage).
        - BigQuery (for cloud-based storage).
## Technologies Used
   - Google Cloud: BigQuery, Cloud Functions, Cloud Scheduler.
   - Python: Core language used for data extraction, transformation, and loading.
           - Libraries: pandas, requests, sqlalchemy, pytz.
   - APIs: OpenWeather, AeroDataBox.
   - Databases: MySQL (local), BigQuery (cloud).
## Prerequisites
   - Python 3.9+ installed on your local machine.
   - MySQL database set up for local data storage.
   - A Google Cloud project with BigQuery and Cloud Functions enabled.
   - API keys for OpenWeather and AeroDataBox.
## How to Run Locally
  1. Clone the repository and navigate to the project directory:
     ```bash
     git clone https://github.com/your-repository.git
     cd your-repository
     ```
  2.  Install the required dependencies:
           ```bash
      
     cd your-repository
     pip install -r requirements.txt
     ```
 3. **Set up the MySQL database to store data locally.**
 4. Run the main Python script to initiate the ETL process:
    ```python
    python3 main.py
## Running in the Cloud

### For running the ETL pipeline on Google Cloud, the function-service folder contains the necessary code for Google Cloud Functions.
### Steps:
   - Deploy the Cloud Functions from the function-service folder to your Google Cloud project.
   - Use Cloud Scheduler to automate the pipeline execution based on your preferred schedule.

## Folder Structure
   - function-service/: Contains the code for deploying to Google Cloud Functions.
   - main.py: Main script for running the pipeline locally.
