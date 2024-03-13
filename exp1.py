class QuizApp:
    def __init__(self, master):

        self.master = master
        self.master.title("Quiz App")

        self.correct= False

        # Variable to track if the user has clicked
        self.master.user_clicked = tk.BooleanVar(value=False)

        quiz_file_path = os.path.join(FILE_PATH, "quiz_entro.csv")  # Replace with the actual path to your CSV file

        with open(quiz_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            header = next(reader)  # Skip the header

            success_count = 0
            fail_count = 0
            
            rows=list(reader)
            
            new_rows = list()

            for idx, el in enumerate(rows):
                if idx in range(1, 10):
                    new_rows.append(el)

            if ALL_IN_ORDER is False:
                random.shuffle(new_rows)

            for row in new_rows:

                question_idx, fig_idx, question, answer1, is_true1, answer2, is_true2, answer3, is_true3 = process_question(row)

                question_window = tk.Toplevel(self.master)
                question_window.title("Question")

                self.question_label = tk.Label(question_window, text=question)
                self.question_label.pack()

                selected_answer = tk.StringVar()

                correct_answer_idx = 'a' if is_true1 == 'V' else ('b' if is_true2 == 'V' else 'c')
                correct_answer     = answer1 if is_true1 == 'V' else (answer2 if is_true2 == 'V' else answer3)

                # Create radio buttons for answer options
                self.answer_options = [
                    (answer1, answer1),
                    (answer2, answer2),
                    (answer3, answer3)
                ]
                for text, answer in self.answer_options:
                    tk.Radiobutton(question_window, text=text, variable=selected_answer, value=answer).pack(anchor=tk.W)

                self.submit_button = tk.Button(question_window, text="Submit", command=lambda: self.check_answer(selected_answer.get(), correct_answer, question_window))

                self.submit_button.pack()

                self.master.wait_variable(self.master.user_clicked)

                self.master.user_clicked.set(False)

    def check_answer(self, selected_answer, correct_answer, question_window):

        if selected_answer == correct_answer:
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showerror("Result", f"Incorrect! The correct answer is {correct_answer}.")


        question_window.destroy()  
        self.master.user_clicked.set(True)


def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
