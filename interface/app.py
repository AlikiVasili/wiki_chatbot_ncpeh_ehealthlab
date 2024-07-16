from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

# Set up the environment variable for the Hugging Face token
os.environ["HF_TOKEN"] = "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"

# Load model and tokenizer globally to avoid reloading
model_id_llama2 = "meta-llama/Llama-2-7b-hf"
model_llama2 = AutoModelForCausalLM.from_pretrained(model_id_llama2)
tokenizer_llama2 = AutoTokenizer.from_pretrained(model_id_llama2)

# Set up generation config
generation_config = {
    "do_sample": True,
    "temperature": 0.01,
    "max_new_tokens": 128,
    "eos_token_id": tokenizer_llama2.pad_token_id,
    "return_full_text": False,
}

# Initialize the text generation pipeline
pipeline_llama2 = pipeline(
    "text-generation",
    model=model_llama2,
    tokenizer=tokenizer_llama2,
    framework="pt",
    device=-1,
)

print("Model loaded!")

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS


# Load keywords from file
with open("article_keywords.json", "r", encoding="utf-8") as f:
    keywords_dict = json.load(f)

# Function to find the most relevant article
def find_relevant_article(question, keywords_dict):
    all_keywords = [" ".join(keywords) for keywords in keywords_dict.values()]
    article_names = list(keywords_dict.keys())
    documents = [question] + all_keywords
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    highest_similarity_index = cosine_similarities.argmax()
    return article_names[highest_similarity_index]

# Function to generate response
def generate_response(question, relevant_article):
    
    # Template for response generation
    template = """You are an expert in answering questions related to the Deployment of Generic Cross Border eHealth in Cyprus. Given a question and relevant information from the article '{article}', can you answer the question?
    Question: {question}
    Answer:
    """
    print("Template: " + template)

    with open(os.path.join("articles", relevant_article), "r", encoding="utf-8") as f:
        article_text = f.read()

    context = template.format(question=question, article=article_text)
    print("Generating response...")
    response = pipeline_llama2(context)[0]['generated_text']
    return response.strip()

# Route for answering questions
@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')
    print("Question: " + user_question)
    if not user_question:
        return jsonify({"error": "No question provided."}), 400

    most_relevant_article = find_relevant_article(user_question, keywords_dict)
    print("Most Relevant article: " + most_relevant_article)
    
    response = generate_response(user_question, most_relevant_article)
    print("Response: " + response)

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=False)
