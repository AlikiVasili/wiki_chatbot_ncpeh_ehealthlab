from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Load the keywords from the file
with open("c:/Users/aliki/Desktop/work/version 2/preparation_of_articles/article_keywords.json", "r", encoding="utf-8") as f:
    keywords_dict = json.load(f)

# Function to find the most relevant article
def find_relevant_article(question, keywords_dict):
    all_keywords = [" ".join(keywords) for keywords in keywords_dict.values()]
    article_names = list(keywords_dict.keys())

    # Create a list with the question and all keywords
    documents = [question] + all_keywords

    # Vectorize the documents
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()

    # Compute cosine similarity
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    highest_similarity_index = cosine_similarities.argmax()
    return article_names[highest_similarity_index]

# Example usage
user_question = "What is ePrescription?"
most_relevant_article = find_relevant_article(user_question, keywords_dict)
print("Most relevant article:", most_relevant_article)
