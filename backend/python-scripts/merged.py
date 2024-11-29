import glob

import pandas as pd


def merged_xlsx():
    path = "./downloads"
    file_list = glob.glob(path + "/*.xlsx")
    excel_list = []
    print(file_list)

    for file in file_list:
        excel_list.append(pd.read_excel(file))

    excel_merged = pd.concat(excel_list, ignore_index=True)
    excel_merged.to_excel("./downloads/excel_merged.xlsx", index=False)


merged_xlsx()
