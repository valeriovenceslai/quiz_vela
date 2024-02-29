import csv

def add_empty_column(input_csv, output_csv):
    with open(input_csv, newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            # Insert an empty string as the second element in each row
            row.insert(1, 'None')
            writer.writerow(row)

# Example usage
input_csv = 'C:\\Users\\Valerio\\Desktop\\C_exe\\quiz_vela\\quiz_entro.csv'
output_csv = 'output.csv'
add_empty_column(input_csv, output_csv)
