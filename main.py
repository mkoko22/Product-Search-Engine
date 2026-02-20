import json
import re
from difflib import get_close_matches

# load product data
def load_data(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

# preprocess a single product
def preprocess_product(product):
    name = product.get("name", "")
    description = product.get("description", "")
    brand = product.get("brand", "")
    country = product.get("country", "")
    text = f"{name} {description} {brand} {country}"
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# preprocess all products
def preprocess_data(data):
    processed_data = []
    for product in data:
        processed_data.append(preprocess_product(product))
    return processed_data

# function to handle typos in the search query
def fix_typos(query, vocabulary, n=1, cutoff=0.6):
    words = query.split()
    corrected = []
    for w in words:
        match = get_close_matches(w, vocabulary, n=n, cutoff=cutoff)
        if match:
            corrected.append(match[0])
        else:
            corrected.append(w)
    return " ".join(corrected)

# load and preprocess
data = load_data("products.json")
processed_data = preprocess_data(data)

# sanity check the processed dat
print(processed_data[:3]) 

# test fix_typos function
vocabulary = set()
for text in processed_data:
    for word in text.split():
        vocabulary.add(word)
print(fix_typos("cotten", vocabulary))
print(fix_typos("proffesional", vocabulary))