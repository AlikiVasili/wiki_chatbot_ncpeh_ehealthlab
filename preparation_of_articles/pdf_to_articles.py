import fitz  # PyMuPDF
import os

# Path to the PDF file
pdf_path = 'NCP_eHealth_cy_vol1.pdf'

# Output directory for text files
output_dir = 'articles'
os.makedirs(output_dir, exist_ok=True)

# Table of Contents with chapters and their respective page ranges
toc = {
    "Electronic Cross-Border Services in the EU": (2, 2),
    "My Health in the EU – General Information": (3, 4),
    "Important Information for the Patient": (5, 9),
    "Information for the Doctors in the Country of Residence": (10, 12),
    "Information for the Doctors in the Country of Travel": (13, 14),
    "Information for the Pharmacists in the Country of Travel": (15, 17),
    "NCP eHealth(CY) Portal – Access requirements": (18, 18),
    "NCP process flow Diagram": (19, 19),
    "Registry Roles": (20, 25),
    "Unified data Modelling": (26, 27),
    "User functions": (28, 28),
    "Login process": (29, 30),
    "Doctor operations (National)": (31, 53),
    "Doctor operations (EU)": (54, 59),
    "Pharmacis eDispensation": (60, 65)
}

# Open the PDF file
pdf_document = fitz.open(pdf_path)

# Loop through each chapter in the TOC
i = 0
for chapter, (start_page, end_page) in toc.items():
    chapter_text = ""
    
    # Extract text from the specified page range
    for page_num in range(start_page-1, end_page):
        page = pdf_document.load_page(page_num)
        chapter_text += page.get_text("text")
    
    # Define the output file name
    title = f"article_{i}"
    output_file_path = os.path.join(output_dir, f'{title}.txt')
    i = i +1
    
    # Save the text to the file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(chapter_text)

print("Articles created successfully.")
