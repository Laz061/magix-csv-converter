# Customer Data Extractor

A simple Streamlit web application to extract and clean customer contact information (Registration, Email, Mobile) from a specifically formatted CSV file.

## Features

- Upload a CSV file directly through the web interface.
- Extracts key-value data spread across multiple columns.
- Automatically filters out records that are missing an email address.
- Allows for the addition of optional 'Location' and 'Brand' columns to the output data.
- Provides a data preview within the app.
- Enables downloading the cleaned data as a new CSV file named `extracted_records.csv`.

## Setup and Installation

To run this application locally, you'll need Python installed.

1.  **Clone the repository or download the files.**

2.  **Install the required packages:**
    A `requirements.txt` file is included. Install the dependencies using pip:
    ```sh
    pip install -r requirements.txt
    ```

## How to Use

1.  **Run the Streamlit app:**
    Open your terminal, navigate to the project directory, and run the following command:

    ```sh
    streamlit run extract.py
    ```

2.  **Use the Web Interface:**
    - Your browser should open with the application running.
    - Use the "Choose a CSV file" button to upload your source file.
    - Use the checkboxes and input fields to configure the optional 'Location' and 'Brand' columns.
    - Click the "Process Data" button to start the extraction.
    - Once processing is complete, a preview of the data will be shown.
    - Click the "Download Extracted Data as CSV" button to save the results to your computer.

## Input CSV Format

The script is designed to work with a CSV that has no header row. It expects to find specific key-value pairs in the following columns (1-indexed):

- **Column 3 (C) & 4 (D):** Looks for `'Registration'` and its value.
- **Column 5 (E) & 6 (F):** Looks for `'Driver Email'` and its value.
- **Column 7 (G) & 8 (H):** Looks for `'Mobile'` and its value.

A new customer record is identified by the presence of `'Registration'` in Column 3.
