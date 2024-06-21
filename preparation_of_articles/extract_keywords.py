import nltk
from rake_nltk import Rake
import os

nltk.download('stopwords')
nltk.download('punkt')

# Initialize Rake
r = Rake()

# Directory where your articles are stored
article_dir = "articles"
keywords_dict = {}

# Extract keywords from each article
for filename in os.listdir(article_dir):
    with open(os.path.join(article_dir, filename), "r", encoding="utf-8") as f:
        text = f.read()
        r.extract_keywords_from_text(text)
        keywords = r.get_ranked_phrases()
        keywords_dict[filename] = keywords

# Save keywords to a file
import json
with open("article_keywords.json", "w", encoding="utf-8") as f:
    json.dump(keywords_dict, f, ensure_ascii=False, indent=4)
