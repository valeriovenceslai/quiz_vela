import csv
import random
import logging
import os
from datetime import datetime

logging.basicConfig(filename=datetime.now().strftime("%Y%m%d%H%M%S") + '.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

FILE_PATH = os.path.dirname(__file__)

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
    'navigazione cartografica ed elettronica' : 
        {"All" : (967,1288),
        "Coordinate geografiche" : (967,1011),
        "Carte nautiche e proiezione di Mercatore" : (1012,1067),
        "Navigazione elettronica" : (1068,1080),
        "Orientamento e rosa dei venti" : (1081,1091),
        "Bussole magnetiche" : (1092,1129),
        "Elementi di navigazione stimata: tempo, spazio e velocità" : (1130,1201),
        "Elementi di navigazione costiera" : (1202,1250),
        "Prora e rotta, scarroccio e deriva per effetto del vento e della corrente" : (1251,1280),
        "Pubblicazioni" : (1281,1288)
        },
    'normativa diportistica': (1288,1472)
}

valid_answers = ['a', 'b', 'c']

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
    quiz_file_path = os.path.join(FILE_PATH, "quiz_entro.csv")  # Replace with the actual path to your CSV file

    ALL_IN_ORDER = True
    
    
    def select_section():
        while True:
            print("Choose a quiz section:")
            for idx, section in enumerate(quiz_sections.keys()):
                print(f"{idx}: {section}")

            user_input = input("Enter the number corresponding to the quiz section: ")

            if user_input.isdigit():
                section_idx = int(user_input)

                if 0 <= section_idx < len(quiz_sections):
                    selected_section = list(quiz_sections.keys())[section_idx]
                    print(f"You selected: {selected_section}")

                    if isinstance(quiz_sections[selected_section], dict):
                        target_tuple = select_subsection(quiz_sections[selected_section])
                    else:
                        target_tuple = quiz_sections[selected_section]
                        print(f"Section tuple: {target_tuple}")
                    break
                else:
                    print("Invalid input. Please enter a number within the specified range.")
            else:
                print("Invalid input. Please enter a valid number.")

        return target_tuple

    def select_subsection(subsections):
        while True:
            print("Choose a subsection:")
            for idx, subsection in enumerate(subsections.keys()):
                print(f"{idx}: {subsection}")

            user_input = input("Enter the number corresponding to the subsection: ")

            if user_input.isdigit():
                subsection_idx = int(user_input)

                if 0 <= subsection_idx < len(subsections):
                    selected_subsection = list(subsections.keys())[subsection_idx]
                    print(f"You selected: {selected_subsection}")
                    target_tuple = subsections[selected_subsection]
                    print(f"Subsection tuple: {target_tuple}")
                    break
                else:
                    print("Invalid input. Please enter a number within the specified range.")
            else:
                print("Invalid input. Please enter a valid number.")

        return target_tuple

    # Call the function to select the section
    target_tuple = select_section()
    
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

        if ALL_IN_ORDER is False:
            random.shuffle(new_rows)

        for row in new_rows:
            
            question_idx, question, answer1, is_true1, answer2, is_true2, answer3, is_true3 = process_question(row)
            display_question(question_idx, question, answer1, answer2, answer3)

            user_answer = input("Your choice (a, b, c): ")
            
            while user_answer not in valid_answers:
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
            
            if ALL_IN_ORDER is False:
                if success_count + fail_count == 20:  # Stop after 20 questions
                    break

    print("\nQuiz Stats:")
    print(f"Total Questions: {success_count + fail_count}")
    print(f"Success Count: {success_count}")
    print(f"Fail Count: {fail_count}")

if __name__ == "__main__":
    main()
