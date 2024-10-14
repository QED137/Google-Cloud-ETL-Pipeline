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
# Scheduling in ETL
One of the highlight of this project that retiving ewather data or flight data from api and writing to the cloud database has been aiutmated on the goodle cloud. There is .yml function  for scheduling the tak. One can shcedule the taks as per direction on google cloud documents of one can follow the follwoing instructions 
Uploading the Scheduler Configuration (.yaml)

Upload the .yaml Configuration: If you need to create or update your Cloud Scheduler job using the .yaml file, you can do so as follows:

bash

    gcloud scheduler jobs update http <job-name> \
      --location=<your-location> \
      --schedule="0 */6 * * *" \
      --uri="https://<your-region>-<your-project-id>.cloudfunctions.net/your-function" \
      --time-zone="Europe/Berlin" \
      --format=yaml < job_config.yaml

    This command ensures that the scheduler job will trigger the specified Cloud Function at regular intervals (every 6 hours in this case).

    Benefits of Using YAML for Scheduler Configuration:
        Version Control: You can track changes in the scheduler configuration by storing the .yaml file in version control (e.g., GitHub).
        Reusability: The same configuration can be reused across multiple projects by simply uploading the .yaml file.
        Consistency: Ensure that the scheduling setup remains consistent across environments (development, production, etc.).

Scheduling Example for the Project

In this project, we use the Cloud Scheduler to automatically trigger Cloud Functions that extract flight and weather data from external APIs at regular intervals (every 6 hours). This ensures that the data in both MySQL and BigQuery remains up-to-date.

For example, you can create a flight data scheduler that triggers the flight fetching Cloud Function every 6 hours:
```bash

gcloud scheduler jobs create http flight_schedular \
  --schedule="0 */6 * * *" \
  --uri="https://<your-region>-<your-project-id>.cloudfunctions.net/flight_function" \
  --time-zone="Europe/Berlin" \
  --location=<your-location>
``
With this setup, the flight_function Cloud Function will automatically execute every 6 hours, ensuring that the data pipeline runs seamlessly without manual intervention.
