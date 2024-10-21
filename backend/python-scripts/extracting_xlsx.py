import sys, csv, os, shutil
import pandas as pd
import xml.etree.ElementTree as ET
from openpyxl import Workbook
from os.path import join

# Extract the values from the EDI file
def extract_bill_values(file_path):
    moa_values = []
    totals_values = []
    uns_values = []
    tva_list = []
    bill_reference = ""
    formatted_date = ""
    advance_value = 0
    to_pay = 0
    
    try:
        # Open file with specified encoding
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            # Read all lines from the file
            lines = file.readlines()
            first_line = lines[0].strip()
    except FileNotFoundError:
        print(f"Error: The text file you're trying to get formatted named '{file_path}' can't be found.")
        sys.exit(1)

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

    final_moa = strings.replace

    bill_values = {
        'articles_values': moa_values,
        'advance': advance_value,
        'tva': tva,
        'net_payable': to_pay,
        'reference': bill_reference,
        'date': formatted_date
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

            # Save the extracted values to a CSV file
            with open("./uploads/totals_values.csv", "w", newline='', encoding='utf-8') as f:
                data = [
                    {"JOURNAL": "ACM", "DATE": bill_values['date'], "GENERAL": "401000", "AUXILIAIRE": "", "REFERENCE": bill_values['reference'], "LIBELLE": "Achat MB " + bill_values['reference'], "DEBIT": "", "CREDIT": bill_values['net_payable']},
                    {"JOURNAL": "ACM", "DATE": bill_values['date'], "GENERAL": "411000", "AUXILIAIRE": "", "REFERENCE": bill_values['reference'], "LIBELLE": "Achat MB " + bill_values['reference'], "DEBIT": bill_values['advance'], "CREDIT": ""},          
                    {"JOURNAL": "ACM", "DATE": bill_values['date'], "GENERAL": "445660", "AUXILIAIRE": "", "REFERENCE": bill_values['reference'], "LIBELLE": "Achat MB " + bill_values['reference'], "DEBIT": bill_values['tva'], "CREDIT": ""},          
                ]

                for i in articles:
                    data.append({"JOURNAL": "ACM", "DATE": bill_values['date'], "GENERAL": "", "AUXILIAIRE": "", "REFERENCE": bill_values['reference'], "LIBELLE": "Achat MB " + bill_values['reference'], "DEBIT": i, "CREDIT": ""})

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
def CSVtoXML(inputfile,outputfile):
    if not inputfile.lower().endswith('.csv'):
        print('Expected A CSV File')
        return 0
    if not outputfile.lower().endswith('.xml'):
        print('Expected a XML file')
        return 0
    
    df = pd.read_csv(inputfile)

    entireop='<collection allInfos="EDI content">\n'
    att=df.columns
    rowop=''
    for j in range(len(df)):
        for i in range(len(att)):
            if i==0:
                rowop=rowop+f'<{att[i]} title="{df[att[i]][j]}">\n'
            elif i==len(att)-1:
                rowop=rowop+f'<{att[i]}>{df[att[i]][j]}</{att[i]}>\n</{att[0]}>\n'
            else:
                rowop=rowop+f'<{att[i]}>{df[att[i]][j]}</{att[i]}>\n'
    entireop=entireop+rowop+'</collection>'
    with open(outputfile,'w') as f:
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
# delete_all_contents_in_folder('./uploads')

print("All files in the folder 'uploads' and 'downloads' have been deleted.")
