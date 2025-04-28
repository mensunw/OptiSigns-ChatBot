# scripts/utils.py

import hashlib
import os
import json

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