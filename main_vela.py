import csv
import random
import logging
import os
from datetime import datetime
from quiz_section import quiz_sections_vela
from quiz_section import select_section

FILE_PATH = os.path.dirname(__file__)

filename = 'quiz_vela_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.log'
filepath = os.path.join(FILE_PATH, filename)

logging.basicConfig(filename=filepath, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

RED = '\033[91m'
GREEN = '\033[92m'
ENDC = '\033[0m'

valid_answers = ['v', 'f']

def process_question(row):
    cleaned_row = [col.strip() for col in row if col.strip()]  # Remove leading/trailing spaces from each non-empty column
    
    question_idx, question, answer1, is_true1, answer2, is_true2 = cleaned_row
    
    return question_idx, question, answer1, is_true1, answer2, is_true2

def display_question(question_idx, question):
    print(f"\nQuestion {question_idx}: {question}")

def evaluate_answer(user_answer, correct_answer_idx, correct_answer):
    if user_answer.lower() == correct_answer_idx.lower():
        print(GREEN + "Correct!\n" + ENDC)
        return True
    else:
        print(RED + "Wrong!" + ENDC + f" The correct answer was {correct_answer_idx} : {correct_answer}\n")
        return False

def main():
    quiz_file_path = os.path.join(FILE_PATH, "quiz_vela.csv")  # Replace with the actual path to your CSV file

    target_tuple, selected_section, selected_subsection = select_section(quiz_sections_vela)

    ALL_IN_ORDER = False
    
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

            question_idx = row[0]
            question     = row[1]
            answer1      = row[2]
            is_true1     = row[3]
            answer2      = row[4]

            display_question(question_idx, question)

            user_answer = input("Your choice (v, f): ")
            
            while user_answer not in valid_answers:
                user_answer = input("Your choice (v, f): ")

            correct_answer_idx = 'v' if is_true1 == 'V' else 'f'
            correct_answer     = answer1 if is_true1 == 'V' else answer2

            if evaluate_answer(user_answer, correct_answer_idx, correct_answer):
                success_count += 1
            else:
                fail_count += 1
                
                warning_message =  f"Question {question_idx}: {question}:"
                
                warning_message += f"\na) {answer1}"
                if user_answer == 'v':
                    warning_message += " -"
                if correct_answer_idx == 'v':
                    warning_message += " +"
                    
                warning_message += f"\nb) {answer2}"
                if user_answer == 'f':
                    warning_message += " -"
                if correct_answer_idx == 'f':
                    warning_message += " +"
                
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
