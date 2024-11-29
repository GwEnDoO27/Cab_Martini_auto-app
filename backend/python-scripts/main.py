import glob
import sys

from extracting_xlsx import delete_all_contents_in_folder, merged_xlsx


def main():
    path_down = "./downloads"
    path_upp = "./uploads"
    xml_file = "./downloads/totals_values.xml"

    if len(glob.glob(path_upp + "/*")) > 1:
        merged_xlsx()
        lenght = len(glob.glob(path_upp + "/*"))
        print(f"Nombre de fichiers dans le dossier uploads : {lenght}")
    else:
        print(f"{sys.argv[1]} is a single file.")
        return 0


if __name__ == "__main__":
    main()
