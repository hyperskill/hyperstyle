import openpyxl


def remove_sheet_with_results(path: str):
    file = openpyxl.load_workbook(path)
    file.remove(file['Inspection results'])
    file.save(path)
