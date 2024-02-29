def concatenate_lines_with_space(filename):
    concatenated_lines = []

    is_split = False

    with open(filename, 'r', encoding='utf-8') as file:
        previous_line = ''
        for line in file:
            if line.startswith(' '):

                # print(f"previous_line {previous_line}")
                # print(f"line          {line}")
                # input()

                # is_split = True

                # Concatenate with the previous line
                concatenated_lines[-1] += line.strip()
            else:
                # Append the line as is
                concatenated_lines.append(line.strip())
            previous_line = line

            # if is_split is True:
                # print(f"concatenated_lines {concatenated_lines[-1]}")
                # input()

    return concatenated_lines

# Example usage
filename = 'C:\\Users\\Valerio\\Desktop\\C_exe\\quiz_vela\\tmp\\quiz_entro.csv'
concatenated_lines = concatenate_lines_with_space(filename)

quiz_file_path =  "C:\\Users\\Valerio\\Desktop\\C_exe\\quiz_vela\\tmp\\out_file.csv"

with open(quiz_file_path, 'w') as output_file:
    
    for line in concatenated_lines:

        print(line)

        output_file.write(line + '\n')

# # Example usage
# csv_file = 'C:\\Users\\Valerio\\Desktop\\C_exe\\quiz_vela\\tmp\\quiz_entro.csv'
# remove_newlines_and_write(csv_file)
