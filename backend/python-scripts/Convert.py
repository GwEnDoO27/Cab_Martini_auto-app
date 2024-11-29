import glob
import sys

from extracting_xlsx import (
    CSVtoXML,
    XMLtoXLSX,
    delete_all_contents_in_folder,
    formating_csv,
)


def main():
    xml_file = "./downloads/totals_values.xml"
    file_name = sys.argv[1]
    formating_csv(file_name)
    CSVtoXML("./uploads/totals_values.csv", xml_file)
    XMLtoXLSX(xml_file, sys.argv[1])
    print("one file name :", file_name)


if __name__ == "__main__":
    main()
