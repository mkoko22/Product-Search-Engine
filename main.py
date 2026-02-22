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
def fix_typos(query, vocabulary, synonyms_dict, n=1, cutoff=0.7):
    words = query.split()
    corrected = []
    all_synonyms = set(synonyms_dict.keys())
    for vals in synonyms_dict.values():
        all_synonyms.update(vals)

    for w in words:
        if w in all_synonyms:
            corrected.append(w)
        else:
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
    expanded = set()
    for w in words:
        expanded.add(w)
        
        if w in synonyms_dict:
            for syn in synonyms_dict[w]:
                expanded.add(syn)
                
        for key, values in synonyms_dict.items():
            if w in values:
                expanded.add(key)
                for syn in values:
                    expanded.add(syn)

    return " ".join(expanded)

# search function with filtering
def search(query, vectorizer, tfidf_matrix, data, synonyms_dict, vocabulary, max_price=None, target_brand=None, top_k=10):
    query = query.lower()
    query = re.sub(r"[^a-z0-9\s]", " ", query)
    query = re.sub(r"\s+", " ", query).strip()
    query = fix_typos(query, vocabulary, synonyms_dict)
    query = expand_synonyms(query, synonyms_dict)
    query_vec = vectorizer.transform([query])

    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    sorted_indices = np.argsort(scores)[::-1]

    results = []
    for idx in sorted_indices:
        score = float(scores[idx])
        
        if score == 0:
            break

        product = data[idx]

        if max_price is not None: # price filtering
            try:
                price = float(product.get('price', 0))
                if price > max_price:
                    continue
            except ValueError:
                continue

        if target_brand is not None: # brand filtering
            brand = product.get('brand', '').lower()
            if brand != target_brand.lower():
                continue

        results.append((product, score))
        if len(results) == top_k:
            break
            
    return results

# interactive CLI loop
def run_cli(vectorizer, tfidf_matrix, data, synonyms_dict, vocabulary):
    print("\n" + "="*60)
    print("Product Search Engine Ready")
    print("="*60 + "\n")
    
    while True:
        print("-"*60 + "\n")
        query = input("Search keywords (or 'exit' to quit): ").strip()
        
        if not query:
            continue
            
        if query.lower() in ["exit", "quit"]:
            print("\nGoodbye!\n")
            break

        price_input = input("Max price (optional, press Enter to skip): ").strip()
        max_price = None
        if price_input:
            try:
                max_price = float(price_input)
            except ValueError:
                print("  [!] Invalid price format. Ignoring price filter.")

        brand_input = input("Brand (optional, press Enter to skip): ").strip()
        target_brand = brand_input if brand_input else None

        print("\nSearching...")
        results = search(query, vectorizer, tfidf_matrix, data, synonyms_dict, vocabulary, max_price, target_brand)

        if not results:
            print("\nNo matching products found for your criteria. Try looser filters.\n")
            continue

        print(f"\nTop {len(results)} results:")
        for i, (product, score) in enumerate(results, 1):
            name = product.get('name', 'Unknown')
            price = product.get('price', 'N/A')
            brand = product.get('brand', 'N/A')
            print(f"  {i}. {name}")
            print(f"     Brand: {brand} | Price: ${price} | (Score: {score:.4f})")
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





