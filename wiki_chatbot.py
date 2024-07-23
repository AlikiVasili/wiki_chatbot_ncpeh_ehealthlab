import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
import re

os.environ["HF_TOKEN"] = "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"

# Initialize the model and tokenizer
model_id_llama2 = "meta-llama/Llama-2-7b-hf"
model_llama2 = AutoModelForCausalLM.from_pretrained(model_id_llama2)
tokenizer_llama2 = AutoTokenizer.from_pretrained(model_id_llama2)

# Set up generation config
generation_config = {
    "do_sample": True,  # Use greedy decoding for speed
    "temperature": 0.01,
    "max_new_tokens": 512,  # Limit the number of tokens generated
    "eos_token_id": tokenizer_llama2.pad_token_id,
    "return_full_text": False,
}

# Set up the pipeline (defined after the function definition to avoid issues with tokenizer sharing)
pipeline_llama2 = pipeline(
    "text-generation",
    model=model_llama2,
    tokenizer=tokenizer_llama2,
    framework="pt",
    device=-1,  # Use CPU
    **generation_config
)

# Load the keywords from the file
with open("article_keywords.json", "r", encoding="utf-8") as f:
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
    print(article_names[highest_similarity_index])
    return article_names[highest_similarity_index]

# Define your template
template = """You are an expert in answering questions related to the Deployment of Generic Cross Border eHealth in Cyprus. Given a question and relevant information from the article '{article}', can you answer the question?
Question: {question}
Answer:
"""

# Function to generate response
def generate_response(question, relevant_article):
    # Load the relevant article
    with open(os.path.join("articles", relevant_article), "r", encoding="utf-8") as f:
        article_text = f.read()

    context = template.format(question=question, article=article_text)  # Corrected to use {article}
    response = pipeline_llama2(context)[0]['generated_text']
    response = response.strip()
    return response

def extract_before_first_question(response):
    question_index = response.find("Question:")
    if question_index != -1:
        response = response[:question_index]
    hashtag_index = response.find("### ")
    if hashtag_index != -1:
        response = response[:hashtag_index]
    return response.strip()

def cut_before_first_question(text):
    # Regular expression to find the first question mark
    question_pattern = re.compile(r'\?')
    match = question_pattern.search(text)
    
    if match:
        # Cut the text before the first question mark
        cut_off_index = match.start()
        # Find the start of the sentence that contains the question mark
        sentence_start_index = text.rfind('.', 0, cut_off_index) + 1
        # Return the text up to this sentence
        return text[:sentence_start_index].strip()
    
    # If no question mark is found, return the original text
    return text

def remove_repetitions(text):
    # Normalize the text by replacing newlines with spaces
    text = text.replace('\n', ' ')
    
    # Split the text into sentences
    sentences = text.split('. ')
    seen = set()
    result = []

    for sentence in sentences:
        # Normalize sentence by stripping whitespace
        normalized_sentence = sentence.strip()
        
        # Check for repetition
        if normalized_sentence in seen:
            break
        seen.add(normalized_sentence)
        result.append(normalized_sentence)
    
    # Join the result back into a single string with proper sentence endings
    cleaned_text = '. '.join(result)
    if text.endswith('.'):
        cleaned_text += '.'

    return cleaned_text

# Example usage with interactive question-answer session
while True:
    user_question = input("Ask me a question (type 'quit' to exit): ")
    if user_question.lower() == 'quit':
        break

    most_relevant_article = find_relevant_article(user_question, keywords_dict)
    response = generate_response(user_question, most_relevant_article)

    response = extract_before_first_question(response)
    response = remove_repetitions(response)
    response = cut_before_first_question(response)

    print(response)
