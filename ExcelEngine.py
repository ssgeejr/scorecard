import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font


class XEngine:
    def __init__(self):
        # Get the path to the .openai directory in the user's home directory
        print('XEngine initialized ... ')

    def runTest(self):
        # Define the headers
        headers = ["Issue", "Level", "Created", "Description"]

        # Sample data
        data = [
            ["ISSUE-001", "Critical", "2024-01-01", "System outage in region A"],
            ["ISSUE-002", "High", "2024-01-02", "Database connection issue"],
            ["ISSUE-003", "Medium", "2024-01-03", "Minor UI bug in dashboard"],
            ["ISSUE-004", "Low", "2024-01-04", "Typo in help documentation"]
        ]

        # Create a pandas DataFrame
        df = pd.DataFrame(data, columns=headers)

        # Write the DataFrame to an Excel file
        excel_file = "issues_report.xlsx"
        df.to_excel(excel_file, index=False)

        # Load the workbook using openpyxl to modify the Excel file
        wb = load_workbook(excel_file)
        ws = wb.active

        # Insert a new row after the header row (which is row 1)
        ws.insert_rows(2)

        # Add "SET ONE" with merged cells (A, B, C) and blue font in row 2
        ws.merge_cells('A2:C2')  # Merge columns A, B, C in the second row
        set_one_cell = ws['A2']
        set_one_cell.value = "SET ONE"
        set_one_cell.alignment = Alignment(horizontal='left')  # Align text to the left
        set_one_cell.font = Font(bold=True, color="0000FF")  # Blue font color in hex, bold text

        # Set the column widths
        ws.column_dimensions['A'].width = 12  # Issue column
        ws.column_dimensions['B'].width = 12  # Level column
        ws.column_dimensions['C'].width = 12  # Created column
        ws.column_dimensions['D'].width = 250  # Description column

        # Get the number of rows in the current data (after inserting the new row)
        num_rows = ws.max_row

        # Add a new row with merged cells (A, B, C) and left-aligned text after the first data set
        merged_text = "End of first data set"
        ws.merge_cells(f'A{num_rows + 1}:C{num_rows + 1}')  # Merging columns A, B, C
        merged_cell = ws[f'A{num_rows + 1}']
        merged_cell.value = merged_text
        merged_cell.alignment = Alignment(horizontal='left')

        # Make the "End of first data set" text bold and blue
        merged_cell.font = Font(bold=True, color="0000FF")  # Blue font color in hex

        # Add the second copy of the data starting from the row after the merged row
        for i, row in enumerate(data, start=num_rows + 2):
            ws.append(row)

        # Add a new row with merged cells (A, B, C) and blue font for "DATA THREE"
        num_rows = ws.max_row
        ws.merge_cells(f'A{num_rows + 1}:C{num_rows + 1}')  # Merging columns A, B, C
        data_three_cell = ws[f'A{num_rows + 1}']
        data_three_cell.value = "DATA THREE"
        data_three_cell.alignment = Alignment(horizontal='left')
        data_three_cell.font = Font(bold=True, color="0000FF")  # Blue font for "DATA THREE"

        # Add the third copy of the data starting from the row after "DATA THREE"
        for i, row in enumerate(data, start=num_rows + 2):
            ws.append(row)

        # Save the workbook with the modifications
        wb.save(excel_file)

        print(f"Excel file '{excel_file}' created successfully with three data sets, titles in blue, and duplicated data.")
