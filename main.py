import json
import re
import os
import numpy as np
from collections import Counter
from difflib import get_close_matches
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# synonym dictionary for query expansion
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

# build TF-IDF
def build_tfidf(processed_data):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_data)
    return vectorizer, tfidf_matrix

# expand synonyms
def expand_synonyms(query, synonyms_dict):
    words = query.split()
    expanded = []
    for w in words:
        expanded.append(w)
        if w in synonyms_dict:
            expanded.extend(synonyms_dict[w])
    return " ".join(expanded)

# search function
def search(query, vectorizer, tfidf_matrix, data, synonyms_dict, vocabulary, top_k=10):
    query = query.lower()
    query = re.sub(r"[^a-z0-9\s]", " ", query)
    query = re.sub(r"\s+", " ", query).strip()

    query = fix_typos(query, vocabulary)
    query = expand_synonyms(query, synonyms_dict)

    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append((data[idx], float(scores[idx])))
    return results

# interactive CLI loop
def run_cli(vectorizer, tfidf_matrix, data, synonyms_dict, vocabulary):
    print("\n" + "="*60)
    print("Product Search Engine Ready! Type 'exit' to quit.")
    print("="*60 + "\n")
    
    while True:
        query = input("Search: ").strip()
        if not query:
            continue
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        results = search(query, vectorizer, tfidf_matrix, data, synonyms_dict, vocabulary)

        valid_results = [(p, s) for p, s in results if s > 0]

        if not valid_results:
            print("\nNo matching products found. Try different keywords!\n")
            continue

        print(f"\nTop {len(valid_results)} results:")
        for i, (product, score) in enumerate(valid_results, 1):
            name = product.get('name', 'Unknown')
            price = product.get('price', 'N/A')
            brand = product.get('brand', 'N/A')
            print(f"{i}. {name} | Brand: {brand} | Price: {price} (Score: {score:.4f})")
        print("\n")

# main execution
if __name__ == "__main__":
    print("Loading data and building search index. Please wait...")
    
    if not os.path.exists("products.json"):
        print("Error: 'products.json' not found in the current directory.")
        exit(1)

    data = load_data("products.json") 
    processed_data = preprocess_data(data)

    vectorizer, tfidf_matrix = build_tfidf(processed_data)
    vocabulary = vectorizer.get_feature_names_out()
    run_cli(vectorizer, tfidf_matrix, data, SYNONYMS, vocabulary)





