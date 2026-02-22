import json
import re
import os
from collections import Counter
from difflib import get_close_matches
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

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

# save top words to a file
def save_top_words(processed_data, file_name="top_words.txt", top_n=30):
    words = []
    for product_text in processed_data:
        for w in product_text.split():
            if w not in ENGLISH_STOP_WORDS:
                words.append(w)
    
    counter = Counter(words)
    top_words = counter.most_common(top_n)
    
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    
    with open(file_path, "w") as f:
        for word, freq in top_words:
            f.write(f"{word} {freq}\n")
    
    print(f"Top {top_n} words saved to {file_path}")

# run simple checks only when executing directly
if __name__ == "__main__":
    data = load_data("products.json")
    processed_data = preprocess_data(data)

    print(processed_data[:3])

    vocabulary = {w for text in processed_data for w in text.split()}

    print(fix_typos("cotten", vocabulary))
    print(fix_typos("proffesional", vocabulary))

    # synonyms dictionary for common product-related terms
    SYNONYMS = {
        "use": ["utilize", "apply", "employ"],
        "quality": ["standard", "grade", "caliber"],
        "classic": ["traditional", "timeless", "iconic"],
        "travel": ["journey", "trip", "tour"],
        "materials": ["fabrics", "components", "substances"],
        "design": ["style", "pattern", "layout"],
        "max": ["maximum", "ultimate", "highest"],
        "pro": ["professional", "advanced", "expert"],
        "elite": ["premium", "exclusive", "top-tier"],
        "lite": ["lightweight", "basic", "slim"],
        "sport": ["athletic", "fitness", "training"],
        "plus": ["additional", "extra", "extended"],
        "studio": ["workshop", "lab", "creative-space"],
        "designed": ["crafted", "built", "constructed"],
        "worldwide": ["global", "international", "universal"],
        "essentials": ["basics", "necessities", "fundamentals"],
        "performs": ["operates", "functions", "works"],
        "ensure": ["guarantee", "secure", "confirm"],
        "excellent": ["outstanding", "superb", "exceptional"],
        "performance": ["efficiency", "output", "capabilities"],
        "functionality": ["features", "capabilities", "utility"],
        "home": ["house", "domestic", "residential"],
        "ideal": ["perfect", "optimal", "suitable"],
        "modern": ["contemporary", "current", "updated"],
        "premium": ["luxury", "high-end", "top-quality"],
        "collection": ["set", "series", "assortment"],
        "setup": ["configuration", "installation", "arrangement"],
        "users": ["customers", "clients", "consumers"],
        "craftsmanship": ["artistry", "skill", "expertise"],
        "friendly": ["easy", "accessible", "user-friendly"],
    }




