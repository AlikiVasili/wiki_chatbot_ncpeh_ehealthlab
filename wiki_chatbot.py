import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import os

# Function to generate response
def generate_response(question, articles):
    context = template.format(question=question, articles=articles)
    response = pipeline_llama2(context)[0]['generated_text']
    # Extract the answer part without unnecessary tokens
    start_token = "\begin{blockquote}"
    end_token = "\end{blockquote}"
    start_index = response.find(start_token)
    end_index = response.find(end_token)
    if start_index != -1 and end_index != -1:
        response = response[start_index + len(start_token):end_index].strip()
    return response

# Initialize the model and tokenizer
model_id_llama2 = "meta-llama/Llama-2-7b-hf"
model_llama2 = AutoModelForCausalLM.from_pretrained(model_id_llama2)
tokenizer_llama2 = AutoTokenizer.from_pretrained(model_id_llama2)

# Set up generation config
generation_config = {
    "do_sample": False,  # Use greedy decoding for speed
    "temperature": 0.01,
    "max_new_tokens": 128,  # Limit the number of tokens generated
    "eos_token_id": tokenizer_llama2.pad_token_id,
    "return_full_text": False,
}

# Set up the pipeline
pipeline_llama2 = pipeline(
    "text-generation",
    model=model_llama2,
    tokenizer=tokenizer_llama2,
    framework="pt",
    device=-1,  # Use CPU
    **generation_config
)

# Define your template
template = """You are an expert in answering questions related to the Deployment of Generic Cross Border eHealth in Cyprus. Given a question and relevant information from the articles inside the website of Deployment of Generic Cross Border eHealth in Cyprus, can you answer the question?
Question: {question}
Articles: {articles}
Answer:
"""

# Load the articles into memory
articles = []
article_dir = "articles_sum"  # Assuming articles are stored in this directory
for filename in os.listdir(article_dir):
    with open(os.path.join(article_dir, filename), "r", encoding="utf-8") as f:
        articles.append(f.read())

# Combine articles into a single context
articles_combined = " ".join(articles)

# Loop for interactive question-answer session
while True:
    user_question = input("Ask me a question (type 'quit' to exit): ")
    if user_question.lower() == 'quit':
        break
    response = generate_response(user_question, articles_combined)
    print(response)
