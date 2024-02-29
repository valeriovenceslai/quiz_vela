import csv

reader = csv.reader(open("C:\\Users\\Valerio\\Desktop\\C_exe\\quiz_vela\\quiz_entro.csv", "r"), delimiter=',')
with open("output.txt", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(reader)