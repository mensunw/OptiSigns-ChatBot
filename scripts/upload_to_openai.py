# scripts/upload_to_openai.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# init OpenAI client for easier API access
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ARTICLES_DIR = "../articles"

def upload_file(filepath):
    """
    Upload a single file content to OpenAI (API upload)
    """
    with open(filepath, "rb") as f:
        file = client.files.create(
            file=f,
            purpose="assistants"
        )
    return file.id  

def create_vector_store(file_ids):
    """
    Create a vector store with uploaded file IDs
    """
    vector_store = client.vector_stores.create(
        name="Optisigns Vector Store",
        file_ids=file_ids
    )
    return vector_store.id

def upload_and_store(filenames):
    ''''''
    file_ids = []
    for filename in filenames:
        filepath = os.path.join("articles", filename)
        file_id = upload_file(filepath)
        print(f"Uploaded {filename} as file_id {file_id}")
        file_ids.append(file_id)
    vector_store_id = create_vector_store(file_ids)
    print(f"Vector Store ID: {vector_store_id}")
    print(f"Uploaded {len(file_ids)} files into Vector Store.")

def main():
    try:
        file_ids = []
        # upload the files
        for filename in os.listdir(ARTICLES_DIR):
            filepath = os.path.join(ARTICLES_DIR, filename)
            file_id = upload_file(filepath)
            print(f"Uploaded {filename} - File ID: {file_id}")
            file_ids.append(file_id)
        # create vector store based on the file ids uploaded
        vector_store_id = create_vector_store(file_ids)
        print(f"Vector Store ID: {vector_store_id}")
        print(f"Uploaded {len(file_ids)} files into Vector Store.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()