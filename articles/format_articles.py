def format_article_file(input_file, output_file):
    try:
        # Read the content of the file
        with open(input_file, 'r', encoding='utf-8') as file:
            article_text = file.read()

        # Replace line breaks with spaces
        formatted_text = article_text.replace('\n', ' ').replace('\r', ' ')

        # Remove any duplicate spaces
        formatted_text = ' '.join(formatted_text.split())

        # Write the formatted text to a new file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(formatted_text)

        print(f"Formatted article written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_file = r'C:\Users\aliki\Desktop\wiki_chatbot_ncpeh_ehealthlab\articles\article_13.txt'
output_file = r'C:\Users\aliki\Desktop\wiki_chatbot_ncpeh_ehealthlab\articles\article_13.txt'
format_article_file(input_file, output_file)
