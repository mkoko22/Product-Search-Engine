## Product Search Engine (CLI)
# What I Built:
I built a lightweight, terminal-based search engine designed to quickly and accurately search through a dataset of 10,000 products. Rather than building a web interface, I chose to build a Command Line Interface (CLI). This allowed me to focus on the actual backend logic: text preprocessing, handling user typos, synonym expansion, mathematical ranking (TF-IDF), and post-search filtering.

# How to Run It Step-by-Step:
1. Prerequisites:
Ensure you have Python 3 installed.
You will also need to install the required libraries for matrix math and vectorization.
- pip install scikit-learn numpy

2. Setup:
Ensure both main.py and products.json are in the same directory.

4. Run the application:
Execute the script from your terminal:
- python main.py

# Example Queries to Try:
Once the CLI says "Ready", try these examples to see the engine's features in action:

* Test Typo Correction: Type proffessnal cotten
(Watch the engine automatically fix it to "professional cotton" and return relevant results).
* Test Synonym Expansion: Search for `tour`, note the top results, and then search for `travel`. You will see the exact same products with identical mathematical relevance scores.
  Search for `workshop`. Even though the products are named "Studio", the reverse-lookup engine successfully maps the concept and returns the correct items.
* Test Filtering: Type `headphones`, then when prompted, set a Max Price of `300` and a Brand of `Nova`.




