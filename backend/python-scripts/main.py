import glob
import sys

from extracting_xlsx import (
    CSVtoXML,
    EDItoXLSX,
    XMLtoXLSX,
    delete_all_contents_in_folder,
    formating_csv,
    merged_xlsx,
)


def main():
    path_down = "../downloads"
    path_upp = "../uploads"
    xml_file = "./downloads/totals_values.xml"

    if len(glob.glob(path_upp + "/*")) > 1:
        for file in glob.glob(path_upp + "/*"):
            formating_csv(file)
            CSVtoXML("./uploads/totals_values.csv", xml_file)
            XMLtoXLSX(xml_file, file)
            print("File converted to xlsx")
        merged_xlsx()
    elif len(glob.glob(path_upp + "/*")) == 1:
        formating_csv(sys.argv[1])
        CSVtoXML("./uploads/totals_values.csv", xml_file)
        XMLtoXLSX(xml_file, sys.argv[1])
        print("File converted to xlsx")
    else:
        print(f"{sys.argv[1]}is neither a file nor a folder.")
        return 0
