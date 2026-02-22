## Search Engine Documentation

### How My Search Works at a High Level:

When a user types a query, the text goes through a step-by-step journey before the results appear on the screen:

1. Cleaning: First, I strip out punctuation and make everything lowercase so the query matches the clean format of the product database.

2. Typo Fixing: I check the user's words against the actual vocabulary in our dataset. If there is a slight misspelling, the engine finds the closest valid word. However, I added a safety check: if the word is already a known synonym, it skips the spellchecker so it doesn't accidentally change a valid concept into a different word.

3. Synonym Expansion: Next, it checks a custom dictionary I built. I made sure this works in both directions. If someone searches "studio", the engine quietly adds "workshop" to the search. And if they search "workshop", it knows to look backwards and add "studio".

4. Scoring (The Math): Instead of just writing a loop to count matching words, I used a concept called TF-IDF. This turns the text into a mathematical vector, giving more weight to unique, meaningful words and ignoring filler words like "the". Then, I use Cosine Similarity to calculate the "angle" between the user's search vector and every product's vector. The smaller the angle, the better the match.

5. Filtering: Finally, it sorts everything by the math score. If the user asked for a max price or a specific brand, the engine walks down the sorted list, skipping over items that don't fit the filters, until it gathers exactly the top 10 best matches.

### What I Built Myself vs. What I Reused

What I reused:
* I realized that trying to write complex matrix math from scratch for a weekend assignment wasn't practical or efficient.
For the core math, I used TfidfVectorizer and cosine_similarity from the scikit-learn library. These are heavily optimized, making them fast for comparing 10,000 products instantly.
* For handling typos, I used Python's built-in difflib. It handles fuzzy string matching nicely without needing to install heavy external dependencies.
* To analyze my dataset, I relied on Python's built-in Counter and scikit-learn's ENGLISH_STOP_WORDS. I needed to know the most frequent words in the dataset, but a raw count would be flooded with useless words like "the", "and", or "with". Reusing a pre-built stop-word list let me instantly filter out the noise and isolate the meaningful product terms.

What I built myself:
* The Pipeline Logic: I designed the step-by-step order of operations. A decision here was applying the price and brand filters after calculating the math, during the final loop. If I had filtered the dataset first, the array indexes would have misaligned with the TF-IDF matrix and broken the search.
* A Targeted Synonym Engine: Instead of pulling in a massive, slow English dictionary library, I wrote a temporary script to find the most common meaningful words in this specific dataset. From that, I hand-crafted a small, bidirectional synonym dictionary tailored exactly to these products.
* The CLI & Edge Case Handling: I built the terminal interface to be resilient. It catches errors safely, like if a user types letters into the price filter, or if the JSON file is missing.

### What Works Well and What is Still Weak / Unfinished

What works well:

* Performance: Because the search relies on matrix math instead of looping through strings, it feels instant.
* Search Accuracy & Relevance: The combination of fuzzy typo-correction and bidirectional synonym expansion works well together. The engine successfully understands that a user searching for workshop with a typo (e.g., wrkshop) is actually looking for studio products, and it returns highly relevant results without failing.
* Robustness: The application handles edge cases cleanly. I tuned the algorithms (like adjusting the Levenshtein distance cutoff to 0.7 and prioritizing known synonyms) to ensure the search engine doesn't return false positives or crash on weird inputs.

What is still weak / unfinished:

* Lexical vs. Semantic Search: While TF-IDF paired with my custom synonym dictionary works well for keyword matching, it fundamentally relies on exact-term frequencies. It doesn't truly "understand" the context or intent behind a user's sentence. If I were building the next iteration of this for a modern AI, I would replace this classical NLP approach with dense vector embeddings.

Production Scalability: Currently, the TfidfVectorizer processes the JSON file and builds the mathematical matrix in memory every single time the CLI is executed. While this initializes in under a second for 10,000 records, it is a major bottleneck for scalability. In a real-world production environment, I would pre-compute and save the matrix so the engine doesn't repeat the heavy math on every launch. This would allow the system to handle millions of products and concurrent user requests efficiently. I am also motivated to learn how to wrap this backend logic into a lightweight web framework, which would allow the system to handle concurrent user requests efficiently.



