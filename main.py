import csv
import random
import logging
from datetime import datetime

logging.basicConfig(filename=datetime.now().strftime("%Y%m%d%H%M%S") + '.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

RED = '\033[91m'
GREEN = '\033[92m'
ENDC = '\033[0m'

quiz_sections = {
    'teoria_dello_scafo' : (0,125),
    'motori' : (126,229),
    'sicurezza della navigazione' : (230,444),
    'manovra e condotta' : (445,599),
    'colreg e segnalamento marittimo' : (600,846),
    'meteorologia' : (847,966),
    'navigazione cartografica ed elettronica' : (967,1288),
    'normativa diportistica': (1288,1472)
}

def process_question(row):
    cleaned_row = [col.strip() for col in row if col.strip()]  # Remove leading/trailing spaces from each non-empty column
    
    question_idx, question, answer1, is_true1, answer2, is_true2, answer3, is_true3 = cleaned_row
    
    return question_idx, question, answer1, is_true1, answer2, is_true2, answer3, is_true3

def display_question(question_idx, question, answer1, answer2, answer3):
    print(f"\nQuestion {question_idx}: {question}")
    print(f"a) {answer1}")
    print(f"b) {answer2}")
    print(f"c) {answer3}")

def evaluate_answer(user_answer, correct_answer_idx, correct_answer):
    if user_answer.lower() == correct_answer_idx.lower():
        print(GREEN + "Correct!\n" + ENDC)
        return True
    else:
        print(RED + "Wrong!" + ENDC + f" The correct answer was {correct_answer_idx} : {correct_answer}\n")
        return False

def main():
    quiz_file_path = "quiz_entro.csv"  # Replace with the actual path to your CSV file
    
    # Display keys and wait for user input
    print("Choose a quiz section:")
    for idx, section in enumerate(quiz_sections.keys()):
        print(f"{idx}: {section}")

    # Get user input
    user_input = input("Enter the number corresponding to the quiz section: ")

    # Check if the input is a valid number
    if user_input.isdigit():
        section_idx = int(user_input)

        # Check if the index is within the valid range
        if 0 <= section_idx < len(quiz_sections):
            selected_section = list(quiz_sections.keys())[section_idx]
            print(f"You selected: {selected_section}")

            target_tuple = quiz_sections[selected_section]
        else:
            print("Invalid input. Please enter a number within the specified range.")
    else:
        print("Invalid input. Please enter a valid number.")
    
    with open(quiz_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = next(reader)  # Skip the header
        header = next(reader)  # Skip the header

        success_count = 0
        fail_count = 0
        
        rows=list(reader)
        
        new_rows = list()

        for idx, el in enumerate(rows):
            if idx in range(target_tuple[0], target_tuple[1]):
                new_rows.append(el)

        random.shuffle(new_rows)

        for row in new_rows:
            
            question_idx, question, answer1, is_true1, answer2, is_true2, answer3, is_true3 = process_question(row)
            display_question(question_idx, question, answer1, answer2, answer3)

            user_answer = input("Your choice (a, b, c): ")
            
            correct_answer_idx = 'a' if is_true1 == 'V' else ('b' if is_true2 == 'V' else 'c')
            correct_answer     = answer1 if is_true1 == 'V' else (answer2 if is_true2 == 'V' else answer3)

            if evaluate_answer(user_answer, correct_answer_idx, correct_answer):
                success_count += 1
            else:
                fail_count += 1
                
                warning_message =  f"Question {question_idx}: {question}:"
                
                warning_message += f"\na) {answer1}"
                if user_answer == 'a':
                    warning_message += " -"
                if correct_answer_idx == 'a':
                    warning_message += " +"
                    
                warning_message += f"\nb) {answer2}"
                if user_answer == 'b':
                    warning_message += " -"
                if correct_answer_idx == 'b':
                    warning_message += " +"
                    
                warning_message += f"\nc) {answer3}"
                if correct_answer_idx == 'c':
                    warning_message += " +"
                if user_answer == 'c':
                    warning_message += " -"
                
                logging.warning(warning_message)

            if success_count + fail_count == 20:  # Stop after 20 questions
                break

    print("\nQuiz Stats:")
    print(f"Total Questions: {success_count + fail_count}")
    print(f"Success Count: {success_count}")
    print(f"Fail Count: {fail_count}")

if __name__ == "__main__":
    main()
