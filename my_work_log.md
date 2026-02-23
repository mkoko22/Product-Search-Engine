## Feb 20
### 19:30–21:30

Did: read the assignment carefully and worked on understanding the requirements. Reviewed TF-IDF and feature weighting examples to see how to identify which words are most meaningful in a search context. Explored different interface options (CLI vs website) and considered how much impact the interface has versus the search logic.

Confused about: how to clearly distinguish common versus informative words when ranking relevance, whether a CLI might be viewed as less impressive than a website, and how detailed the work log should be to reflect genuine progress.

Changed after learning: decided to maintain the work log in real time rather than writing it all at the end. Also concluded that a simple CLI can still be very effective if the search and ranking logic is solid, so I’ll prioritize correctness and clarity over interface design.

## Feb 21
### 00:30-02:30

Did: started implementing data preprocessing. Wrote functions to load JSON, combine product fields into a single text string, lowercase everything, and remove punctuation/extra spaces. Tested preprocessing on sample products to confirm it worked.

Confused about: how to handle typos in user queries efficiently and whether to build it from scratch or use existing libraries.

Changed after learning: discovered difflib.get_close_matches and rapidfuzz.process.extractOne could help with fuzzy matching. Tested difflib for single-word typos and decided it works more reliably for short words than rapidfuzz. Decided to integrate it into query preprocessing.

## Feb 22
### 16:00 - 18:00

Did: worked on ways to improve search recall by handling vocabulary mismatches. Wrote a script to count and extract the most frequent words across all products (save_top_words) to understand the dataset better. Based on those common terms, I manually created a SYNONYMS dictionary to map variations.

Confused about: at first, my top words list was completely flooded with generic words like "the", "and", or "with", which wasn't helpful for finding actual product attributes. I was also unsure whether to use a massive external library like WordNet for synonyms or just hardcode them.

Changed after learning: I realized I needed to filter out common English words (like "the" or "and"), so I used ENGLISH_STOP_WORDS from sklearn to clean up my frequency counter. For synonyms, I originally thought about using a big dictionary library to find matching words. But I realized that would be too slow and complicated for a simple CLI app. Instead, I decided to just "hardcode" a small dictionary of synonyms myself using only the most common words I found in my product dataset.


### 19:00-21:00

Did: implemented the core search and ranking engine. I brought in TfidfVectorizer from sklearn to convert all product texts into a matrix, which automatically weights unique/informative words higher than generic ones. I also wrote an expand_synonyms function to catch related terms, and built the final search function that ties the whole pipeline together.

Confused about: initially, I wasn't sure how to efficiently score and rank 10,000 products against a user's query without writing a massive, slow for loop to count matching words. I was also re-calculating the vocabulary for my typo-fixer manually, which felt redundant and slow.

Changed after learning:  I learned about cosine_similarity, which compares the "angle" of the query vector against the entire product matrix instantly, providing a much more accurate relevance score than basic word counting. I also realized TfidfVectorizer automatically extracts all unique words during its fit_transform step. I deleted my manual vocabulary loop and replaced it with vectorizer.get_feature_names_out(), which made the script significantly faster and cleaner.


### 21:00-23:00

Did: added post-search filtering for Price and Brand and polished the CLI. I updated the search function to accept optional filter arguments and process them efficiently.

Confused about: initially, I wasn't sure when to apply the filters. If I filtered the data list before running the search, the index numbers of the products would no longer match the index numbers in my tfidf_matrix, which would cause the program to return the wrong products or crash.

Changed after learning: I realized the best way to do this is to calculate the cosine similarity scores for everything, sort the array from highest to lowest score, and then apply the filters as I loop through the sorted list. I set it to break the loop as soon as it successfully finds 10 products that match the filter criteria.

## Feb 23
### 00:00-02:00 

Did: conducted final end-to-end testing of the CLI. Tested edge-case queries to verify that both the typo-corrector and the custom bidirectional synonym dictionary were working together seamlessly.

Confused about: during testing, I noticed a logic conflict. When I searched for the valid word "workshop" (which my synonym engine is supposed to map to "studio"), I got bizarre results for products containing the word "works" (like "Rustavi Works"). I couldn't figure out why the synonym engine was completely ignoring the word "workshop".

Changed after learning: I realized my typo-corrector was running before the synonym expander and was being way too aggressive. Because my `difflib` cutoff was set to 0.6, the script assumed "workshop" was a misspelling of "works" and overwrote it before the synonym dictionary ever saw it. To fix this, I increased the distance cutoff threshold to 0.7 to make the spellchecker stricter. Also, I added a safety check to the pipeline: if a word is already in my synonym dictionary, the engine explicitly bypasses the typo-corrector.

### 16:00-18:00 
Did: finalized the project by writing the README.md and DOCUMENTATION.md files. I created step-by-step setup instructions, example queries to prove the synonym/typo engine works and an explanation of the system architecture (what I built vs. what I reused).

Confused about: initially, I wasn't sure how to write about the weaknesses of my application.

Changed after learning: I realized that being completely transparent about the system's limitations is actually a strength. Instead of hiding the fact that TF-IDF doesn't understand context, I documented it as "Lexical vs. Semantic Search" and explained that my next learning goal is to implement dense vector embeddings and API wrappers. Framing these as future optimizations made the documentation feel much more honest.
