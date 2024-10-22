import pdfplumber

pdf_file_path = "./uploads/liste.pdf"

extracted_values = []

with pdfplumber.open(pdf_file_path) as pdf:
    for page in pdf.pages:
        # Extract text from the page
        text = page.extract_text()
        if text:
            # Split the text into lines or values
            lines = text.split('\n')
            extracted_values.extend(lines)  # Add the lines to the main list

print(extracted_values)  # This will print all extracted values