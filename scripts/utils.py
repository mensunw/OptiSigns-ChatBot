# scripts/utils.py

import hashlib
import os
import json
import datetime

# note: i designed these helper functions with "main.py" mainly in mind, but easily configurable by entering directory/filepath

def compute_article_hashes(directory="articles"):
    """
    Compute SHA256 hashes of all Markdown files in the given articles directory
    Returns a dict: { filename: hash }
    """
    hashes = {}
    for filename in os.listdir(directory):
      filepath = os.path.join(directory, filename)
      with open(filepath, "rb") as f: # hash the raw bytes for precision
        file_content = f.read()
        file_hash = hashlib.sha256(file_content).hexdigest()
        hashes[filename] = file_hash

    return hashes

def load_json(filepath="article_hashes.json"):
    """
    Load dictionary from a JSON file
    """
    with open(filepath, "r", encoding="utf-8") as f:
      return json.load(f)
    
def detect_changes(old_hashes, new_hashes):
    """
    Compare old and new hashes to find added, updated, and skipped articles
    Returns three lists: [filenames], [filenames], [filenames]
    """
    added = []
    updated = []
    skipped = []

    for filename, new_hash in new_hashes.items():
      if filename not in old_hashes:
        # filename doesn't exist in old hash
        added.append(filename)
      elif old_hashes[filename] != new_hash:
        # file name is the same, but content has changed
        updated.append(filename)
      else:
        # filename exists and content didn't change
        skipped.append(filename)

    return added, updated, skipped

def log_results(added, updated, skipped, output_path="run_logs.txt"):
    """
    Print log summary of the scraping run's added, updated, and skipped articles
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    summary = (
        "=== Job Summary ===\n"
        f"Added: {len(added)} files\n"
        f"Updated: {len(updated)} files\n"
        f"Skipped: {len(skipped)} files\n"
        f"Completed on: {now}\n"
        "===================\n\n"
    )
    print(summary)

    # appends to output log, creates one if it does not exist
    with open(output_path, "a", encoding="utf-8") as f:
      f.write(summary)

def save_json(data, filepath="article_hashes.json", ):
    """
    Save dictionary as a JSON file
    """
    with open(filepath, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=2)