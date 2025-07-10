# Firestore Data to CSV Export Script

This Python script provides a straightforward way to extract data from your Google Cloud Firestore database and save it into a CSV (Comma Separated Values) format. It supports fetching data from all top-level collections and flattens nested document structures for easier CSV representation.

## Features

* Connects to Google Cloud Firestore using a service account key.

* Automatically detects and fetches data from all top-level collections in your database.

* Includes the Firestore document ID (`id`) as a column in the output CSV.

* Flattens nested dictionaries (e.g., `user: { name: 'Alice' }` becomes `user.name: 'Alice'`).

* Converts list fields to their string representation within the CSV.

* Outputs all fetched data into a single CSV file.

## Prerequisites

Before running this script, ensure you have the following:

1.  **Python 3.6+**: The script is written in Python.

2.  **Google Cloud Project with Firestore Enabled**: Your project must have a Firestore database set up and populated with data.

3.  **Firebase Admin SDK**: This Python library is used to interact with Firestore.

4.  **Pandas**: This Python library is used for data manipulation and CSV export.

5.  **Service Account Key**: A JSON key file for authentication.

## Setup

1.  **Download your Service Account Key**:

    * Go to your Google Cloud Console for your Firebase Project.

    * Navigate to **Project settings** (gear icon) > **Service accounts**.

    * Click on **"Generate new private key"** and download the JSON file.

    * **Crucially, store this file securely and do NOT share it publicly or commit it to version control.**

2.  **Install Python Libraries**:
    Open your terminal or command prompt and run the following command to install the required libraries:

    ```
    pip install firebase-admin pandas
    ```

3.  **Configure the Script**:

    * Open the `main.py` file (or whatever you've named the script).

    * Locate the `SERVICE_ACCOUNT_KEY_PATH` variable:

        ```
        SERVICE_ACCOUNT_KEY_PATH = 'path/to/your/serviceAccountKey.json'
        ```

    * **Replace `'path/to/your/serviceAccountKey.json'`** with the actual path to the JSON service account key file you downloaded. If the key file is in the same directory as your Python script, you can just use its filename (e.g., `'your-project-name-firebase-adminsdk-xxxxx-xxxxxx.json'`).

    * Occasionally, you can change the `OUTPUT_CSV_FILENAME` if you prefer a different name for your CSV file.

## How to Run

After setting up the prerequisites and configuration, execute the script from your terminal:

```
python main.py
```

The script will print status messages to the console, indicating which collections it's fetching and when the CSV file has been successfully created. The output CSV file will be saved in the same directory where you run the script.

## Code Overview

* **`initialize_firestore()`**: Handles the connection to your Firestore database using the provided service account credentials.

* **`get_all_collections(db_client)`**: Discovers and returns a list of all top-level collection names present in your Firestore.

* **`get_collection_data(db_client, collection_name)`**: Fetches all documents from a specified collection. It uses `stream()` for efficient retrieval and adds the document's native `id` to its data.

* **`flatten_dict(d, parent_key='', sep='.')`**: A utility function to transform nested dictionaries into a flat structure, making them compatible with CSV format. Nested keys are joined by a `.` (e.g., `address.city`). Lists are converted to strings.

* **`save_to_csv(data, filename)`**: Takes the flattened document data, converts it into a Pandas DataFrame, and then exports it to a CSV file.

* **`main()`**: The primary execution function that orchestrates the entire process, calling the other functions sequentially. It combines data from all collections into a single output CSV, adding a `firestore_collection` field to each document to identify its original collection.

## Security Considerations

The `SERVICE_ACCOUNT_KEY_PATH` refers to a highly sensitive file. **This file grants administrative access to your Firebase project.**

* **Never share this file.**

* **Never commit this file to public version control (e.g., GitHub, GitLab).** Add it to your `.gitignore` file.

* For production deployments, consider more secure ways of handling credentials, such as environment variables, Google Cloud Secret Manager, or other secure credential management systems.