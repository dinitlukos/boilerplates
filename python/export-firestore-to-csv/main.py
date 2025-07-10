import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import os

# --- Configuration ---
# IMPORTANT: Replace 'path/to/your/serviceAccountKey.json' with the actual path
# to your Firebase service account key file.
# You can download this file from your Firebase Project settings > Service accounts.
# For security, consider storing this path in an environment variable in a real application.
SERVICE_ACCOUNT_KEY_PATH = 'serviceAccountKey.json'

# Name of the CSV file where the data will be saved
OUTPUT_CSV_FILENAME = 'data.csv'

def initialize_firestore():
    """
    Initializes the Firebase Admin SDK using the provided service account key.
    Prints an error message if the key file is not found or initialization fails.
    """
    if not os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
        print(f"Error: Service account key file not found at '{SERVICE_ACCOUNT_KEY_PATH}'")
        print("Please download your service account key from the Firebase Console (Project settings > Service accounts) and update SERVICE_ACCOUNT_KEY_PATH.")
        return None

    try:
        # Initialize Firebase Admin SDK with the service account credentials
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully.")
        # Return the Firestore client instance
        return firestore.client()
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return None

def get_all_collections(db_client):
    """
    Fetches the names (IDs) of all top-level collections in the Firestore database.
    Args:
        db_client: An initialized Firestore client instance.
    Returns:
        A list of string names of the top-level collections.
    """
    try:
        # Get all top-level collection references
        collections = db_client.collections()
        # Extract the ID (name) of each collection
        collection_names = [col.id for col in collections]
        print(f"Found top-level collections: {collection_names}")
        return collection_names
    except Exception as e:
        print(f"Error getting collection names: {e}")
        return []

def get_collection_data(db_client, collection_name):
    """
    Fetches all documents from a specific Firestore collection.
    Args:
        db_client: An initialized Firestore client instance.
        collection_name (str): The name of the collection to fetch data from.
    Returns:
        A list of dictionaries, where each dictionary represents a document
        and includes its 'id' field.
    """
    print(f"Fetching data from collection: '{collection_name}'...")
    data = []
    try:
        # Stream documents from the collection (efficient for large collections)
        docs = db_client.collection(collection_name).stream()
        for doc in docs:
            doc_data = doc.to_dict()
            # Add the document ID as a field in the dictionary
            doc_data['id'] = doc.id
            data.append(doc_data)
        print(f"Fetched {len(data)} documents from '{collection_name}'.")
    except Exception as e:
        print(f"Error fetching data from collection '{collection_name}': {e}")
    return data

def flatten_dict(d, parent_key='', sep='.'):
    """
    Recursively flattens a nested dictionary.
    Keys are joined by the separator (default is '.').
    Lists are converted to their string representation.
    Example: {'user': {'name': 'Alice', 'address': {'city': 'NY'}}}
             becomes {'user.name': 'Alice', 'user.address.city': 'NY'}
    Args:
        d (dict): The dictionary to flatten.
        parent_key (str): The base key for current recursion level.
        sep (str): The separator to use for joining keys.
    Returns:
        A new flattened dictionary.
    """
    items = []
    for k, v in d.items():
        # Construct the new key, handling the first level
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            # Recursively flatten nested dictionaries
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # For lists, convert to string.
            # For lists of dictionaries, more complex flattening logic might be needed.
            items.append((new_key, str(v)))
        else:
            # For non-dict, non-list values, just add them
            items.append((new_key, v))
    return dict(items)

def save_to_csv(data, filename):
    """
    Saves a list of dictionaries (representing Firestore documents) to a CSV file.
    Each dictionary is flattened before being added to the DataFrame.
    Args:
        data (list): A list of dictionaries to save.
        filename (str): The name of the CSV file to create/overwrite.
    """
    if not data:
        print(f"No data to save to '{filename}'. Skipping CSV creation.")
        return

    # Flatten each document dictionary to handle nested fields
    flattened_data = [flatten_dict(doc) for doc in data]

    try:
        # Create a Pandas DataFrame from the flattened data
        df = pd.DataFrame(flattened_data)
        # Save the DataFrame to a CSV file
        # index=False prevents writing the DataFrame index as a column
        # encoding='utf-8' handles various characters correctly
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"All Firestore data successfully saved to '{filename}'.")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

def main():
    """
    Main function to orchestrate fetching data from Firestore and saving it to CSV.
    It fetches data from all top-level collections.
    """
    # Initialize Firestore client
    db = initialize_firestore()
    if not db:
        print("Firestore initialization failed. Exiting.")
        return

    # Get names of all top-level collections
    all_collection_names = get_all_collections(db)

    # List to hold data from all collections
    all_data_combined = []

    # Iterate through each collection and fetch its data
    for col_name in all_collection_names:
        collection_data = get_collection_data(db, col_name)
        # Add a 'firestore_collection' field to each document to indicate its origin
        for doc in collection_data:
            doc['firestore_collection'] = col_name
        all_data_combined.extend(collection_data)

    # Save all combined data to a single CSV file
    save_to_csv(all_data_combined, OUTPUT_CSV_FILENAME)

    # --- Optional: Example to fetch data from a specific collection ---
    # Uncomment and modify the lines below if you only need data from one collection.
    # specific_collection_to_fetch = 'your_specific_collection_name_here' # e.g., 'users'
    # if specific_collection_to_fetch in all_collection_names:
    #     specific_data = get_collection_data(db, specific_collection_to_fetch)
    #     save_to_csv(specific_data, f'{specific_collection_to_fetch}.csv')
    # else:
    #     print(f"Collection '{specific_collection_to_fetch}' not found.")


if __name__ == "__main__":
    main()
