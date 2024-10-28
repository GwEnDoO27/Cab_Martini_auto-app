import sys, csv, os, shutil
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from openpyxl import Workbook
from os.path import join

# Extract the values from the EDI file
def extract_bill_values(file_path):
    # Mapping of the code to the corresponding general value
    code_map = {
    '001 SURGELE': '601100',
    '002 ALIMENTAIRE': '601100',
    '003 EMBALLAGE': '602201',
    '004 FOURN.OP': '606302',
    '005 HABILLEMENT': '606303',
    '006 FOURN.BUR': '606401',
    '007 JOUETS et DIV': '602202',
    '008 CADEAU/PLV': '623401',
    '009 ADMINSTR & STAT': '602610',
    '00R EMBALLAGE REUSE': '602612'
    }
    
    moa_values = []
    totals_values = []
    uns_values = []
    tva_list = []
    bill_reference = ""
    formatted_date = ""
    advance_value = 0
    to_pay = 0
    gen_values = []
    
    try:
        # Open file with specified encoding
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            # Read all lines from the file
            lines = file.readlines()
            first_line = lines[0].strip()

    except FileNotFoundError:
        print(f"Error: The text file you're trying to get formatted named '{file_path}' can't be found.")
        sys.exit(1)

    found_codes = set()

    for line in lines:
        print('line:', line)
        # Check if any of the keys from code_map are in the line
        for code in code_map:
            if code in line:
                if code in line and code not in found_codes:  # Only add if code is not in found_codes
                    print('adding this code:', code)
                    gen_values.append(code_map[code])  # Append corresponding value
                    found_codes.add(code)  # Mark this code as found

    # Loop through each line by index for more control
    for i, line in enumerate(lines):
        if "EDI" not in first_line:
            print("The file you provided is not an EDI file.")
            sys.exit(1)

        # Searching for the fourth line, where the date resides 
        if i + 1 == 4:
            parts = line.split('+')[1]
            date_info = parts.split(':')[1] 

            # Format the new date string
            if len(date_info) == 8:  # Check if date info is of the correct length
                year = date_info[:4]
                month = date_info[4:6]
                day = date_info[6:]
                formatted_date = f"{day}/{month}/{year}" 

        # Searching for the third line, where the bill reference resides 
        if i + 1 == 3:
            bill_reference = line.split('+')[2]
    
        # Check if the current line starts with 'IMD'
        if line.startswith('IMD'):
            if i > 0 and not lines[i - 1].startswith('PIA'):
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()

                    if next_line.startswith('MOA'):
                        next_line = next_line.rstrip("'")
                        parts = next_line.split('+')

                        if len(parts) > 1:
                            moa_value_part = parts[1].split(':')
                            if len(moa_value_part) > 1:
                                moa_value = moa_value_part[1]
                                moa_values.append(moa_value)
                        break  # Stop once you find the MOA after IMD

        # Check if the current line starts with 'UNS'
        if line.startswith('UNS'):
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                    
                if next_line.startswith('MOA'):
                    if len(parts) > 1:
                        next_line = next_line.rstrip("'")
                        parts = next_line.split('+')
                        moa_value_part = parts[1].split(':')                    

                    if len(moa_value_part) > 1:
                        moa_value = moa_value_part[1]
                        uns_values.append(moa_value)
                        totals_values.append(moa_value)

                tva_values = uns_values[-2:]
                tva_list = [float(i) for i in tva_values]

                tva = round(sum(tva_list), 2)

    total = max(totals_values, default=0)  # Handle case where totals_values is empty
    total = round(float(total), 2)

    for num in totals_values:
        num = float(num)
        if num < 0:
            advance_value = num
            to_pay = total + num

    bill_values = {
        'articles_values': moa_values,
        'advance': advance_value,
        'tva': tva,
        'net_payable': abs(to_pay),
        'reference': bill_reference,
        'date': formatted_date,
        'general_values': gen_values
    }

    return bill_values

# Extract the values from the EDI file and format them into a CSV file
def formating_csv():
    if __name__ == "__main__": 
        if len(sys.argv) > 1: 
            edi_filename = sys.argv[1]

            bill_values = extract_bill_values(edi_filename)

            if isinstance(bill_values, str):
                print(bill_values)  # If extract_bill_values returned an error message
                return

            # Put all the values of debit of articles in an array
            articles = bill_values['articles_values']
            print(bill_values['general_values'])

            # Save the extracted values to a CSV file
            with open("./uploads/totals_values.csv", "w", newline='', encoding='utf-8') as f:
                data = [
                    {"JOURNAL": "ACM", "DATE": bill_values['date'], "GENERAL": "401000", "AUXILIAIRE": "401LR", "REFERENCE": bill_values['reference'], "LIBELLE": "Achat MB " + bill_values['reference'], "DEBIT": "", "CREDIT": bill_values['net_payable']},
                    {"JOURNAL": "ACM", "DATE": bill_values['date'], "GENERAL": "411000", "AUXILIAIRE": "411MB", "REFERENCE": bill_values['reference'], "LIBELLE": "Achat MB " + bill_values['reference'], "DEBIT": "", "CREDIT": bill_values['advance']},          
                    {"JOURNAL": "ACM", "DATE": bill_values['date'], "GENERAL": "445660", "AUXILIAIRE": "", "REFERENCE": bill_values['reference'], "LIBELLE": "Achat MB " + bill_values['reference'], "DEBIT": bill_values['tva'], "CREDIT": ""},          
                ]

                for i, j in zip(articles, bill_values['general_values']):
                    data.append({"JOURNAL": "ACM", "DATE": bill_values['date'], "GENERAL": j, "AUXILIAIRE": "", "REFERENCE": bill_values['reference'], "LIBELLE": "Achat MB " + bill_values['reference'], "DEBIT": i, "CREDIT": ""})

                writer = csv.writer(f)

                # Write the headers first
                fieldnames = ["JOURNAL", "DATE", "GENERAL", "AUXILIAIRE", "REFERENCE", "LIBELLE", "DEBIT", "CREDIT"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

                print("Your EDI text file has been formatted and saved in 'totals_values.csv'")
        else:
            print("Usage: python3 extracting_csv.py <text_filename>")
            sys.exit(1)

# Delete all files in the folder
def delete_all_contents_in_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    # List all files and directories in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory and its contents
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

# Convert the CSV file to an XML file
def CSVtoXML(inputfile, outputfile):
    if not inputfile.lower().endswith('.csv'):
        print('Expected A CSV File')
        return 0
    if not outputfile.lower().endswith('.xml'):
        print('Expected an XML file')
        return 0
    
    df = pd.read_csv(inputfile)
    
    # Replace NaN values with empty strings
    df = df.replace(np.nan, '', regex=True)
    
    # Function to format 'DEBIT' values with commas instead of dots
    def format_debit(value):
        if isinstance(value, (int, float)) and not pd.isna(value):
            return f"{abs(value):.2f}".replace('.', ',')  # abs() to remove negative signs
        return value
    
    # Function to remove trailing .0 in 'GENERAL' column
    def remove_trailing_zero(value):
        if isinstance(value, float) and value.is_integer():
            return int(value)  # Convert to an integer if it's a whole number
        return value
    
    entireop = '<collection allInfos="EDI content">\n'
    att = df.columns
    rowop = ''
    
    for j in range(len(df)):
        for i in range(len(att)):
            # Start the row with the first column as a title
            if i == 0:
                rowop += f'<{att[i]} title="{df[att[i]][j]}">\n'
            else:
                value = df[att[i]][j]

                # Apply specific transformations to DEBIT and GENERAL columns
                if att[i] == 'DEBIT' or att[i] == 'CREDIT':
                    value = format_debit(value)
                elif att[i] == 'GENERAL':
                    value = remove_trailing_zero(value)

                # Add the formatted value to the row
                rowop += f'<{att[i]}>{value}</{att[i]}>\n'
            
            # Close the journal tag at the end of the row
            if i == len(att) - 1:
                rowop += f'</{att[0]}>\n'
    
    entireop += rowop + '</collection>'
    
    with open(outputfile, 'w') as f:
        f.write(entireop)
 
# Convert the XML file to an Excel file
def XMLtoXLSX():
    # Load the XML file
    tree = ET.parse('./downloads/totals_values.xml')
    root = tree.getroot()

    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Valeurs EDI"

    # Assuming XML structure is uniform and you want to capture child elements
    # Extract headers from the XML file (based on the first row/element)
    headers = [elem.tag for elem in root[0]]  # Gets tags of the first element's children

    # Write the headers to Excel
    ws.append(headers)

    # Iterate through the XML elements and extract the data
    for element in root:
        row_data = [child.text for child in element]  # Get text values of child elements
        ws.append(row_data)

    wb.save(join("./downloads", "excel_values.xlsx"))  

# Call the function to extract the values from the EDI file and format them into a CSV file
formating_csv()

# Merge all CSV files in the folder into a single Excel file
CSVtoXML('./uploads/totals_values.csv', './downloads/totals_values.xml')
XMLtoXLSX()

print("The CSV file has been converted to an Excel file.")

# Delete all files saved in 'uploads'
delete_all_contents_in_folder('./uploads')
print("All files in the folder 'uploads' have been deleted.")
