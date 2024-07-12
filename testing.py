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

# Example usage
text = """Electronic Cross-Border Healthcare is a set of services that allow European citizens to access healthcare in another EU country, while travelling or living abroad.
The services are available under the brand “MyHealth@EU” and facilitate optimum response to EU Cross-Border Health Emergencies.
The services are available under the brand “MyHealth@EU” and facilitate optimum response to EU Cross-Border Health Emergencies.
The services are available under the brand “MyHealth@EU” and facilitate optimum response to EU Cross-Border Health Emergencies."""

cleaned_text = remove_repetitions(text)
print(cleaned_text)
