import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Load the Excel file
file_path = r"C:\Users\aliki\Desktop\wiki_chatbot_ncpeh_ehealthlab\evaluation\testing_results.xlsx"
df = pd.read_excel(file_path)

# Check the first few rows of the DataFrame to ensure it is loaded correctly
print("First few rows of the DataFrame:")
print(df.head(10))

def evaluate_responses(df, evaluation_column):
    # Treat NotFull as Incorrect
    df[evaluation_column] = df[evaluation_column].apply(lambda x: 'Incorrect' if x == 'NotFull' else x)

    # Encode the evaluations: Correct = 1, Incorrect = 0
    y_pred = df[evaluation_column].apply(lambda x: 1 if x == 'Correct' else 0)

    # y_true is 1 for all responses since all must be Correct
    y_true = [1] * len(y_pred)

    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    conf_matrix = confusion_matrix(y_true, y_pred)

    # Response completeness
    total_responses = len(df)
    not_full_responses = len(df[df[evaluation_column] == 'NotFull'])
    response_completeness = 1 - (not_full_responses / total_responses)

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': conf_matrix,
        'response_completeness': response_completeness
    }

# Evaluate for 128 tokens
results_128 = evaluate_responses(df, 'Evaluation_128')

# Evaluate for 256 tokens
results_256 = evaluate_responses(df, 'Evaluation_256')

# Evaluate for 512 tokens
results_512 = evaluate_responses(df, 'Evaluation_512')

# Print results
print("\nResults for 128 tokens:")
print(f"Accuracy: {results_128['accuracy']}")
print(f"Precision: {results_128['precision']}")
print(f"Recall: {results_128['recall']}")
print(f"F1 Score: {results_128['f1']}")
print(f"Confusion Matrix: \n{results_128['confusion_matrix']}")
print(f"Response Completeness: {results_128['response_completeness']}")

print("\nResults for 256 tokens:")
print(f"Accuracy: {results_256['accuracy']}")
print(f"Precision: {results_256['precision']}")
print(f"Recall: {results_256['recall']}")
print(f"F1 Score: {results_256['f1']}")
print(f"Confusion Matrix: \n{results_256['confusion_matrix']}")
print(f"Response Completeness: {results_256['response_completeness']}")

print("\nResults for 512 tokens:")
print(f"Accuracy: {results_512['accuracy']}")
print(f"Precision: {results_512['precision']}")
print(f"Recall: {results_512['recall']}")
print(f"F1 Score: {results_256['f1']}")
print(f"Confusion Matrix: \n{results_512['confusion_matrix']}")
print(f"Response Completeness: {results_512['response_completeness']}")
