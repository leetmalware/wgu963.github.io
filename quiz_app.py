
import tkinter as tk
from tkinter import messagebox
import json
import random
import time

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("C963 Quiz App")
        self.root.geometry("800x500")

        with open('questions.json') as f:
            self.questions = json.load(f)
        random.shuffle(self.questions)

        self.score_correct = 0
        self.score_incorrect = 0
        self.current_question_index = 0
        self.wrong_questions = []

        self.question_label = tk.Label(root, text="", wraplength=700, font=("Helvetica", 16))
        self.question_label.pack(pady=20)

        self.option_buttons = []
        for _ in range(4):
            button = tk.Button(root, text="", width=60, height=2, font=("Helvetica", 12), command=lambda b=_: self.check_answer(b))
            button.pack(pady=5)
            self.option_buttons.append(button)

        self.progress_label = tk.Label(root, text="Progress: 0/0 | Correct: 0 | Incorrect: 0", font=("Helvetica", 12))
        self.progress_label.pack(pady=10)

        self.load_question()

    def load_question(self):
        if self.current_question_index >= len(self.questions):
            self.end_quiz()
            return
        question_data = self.questions[self.current_question_index]
        self.question_label.config(text=question_data["question"])
        for i, option in enumerate(question_data["options"]):
            self.option_buttons[i].config(text=option, bg="SystemButtonFace", state=tk.NORMAL)
        self.progress_label.config(text=f"Progress: {self.current_question_index+1}/{len(self.questions)} | Correct: {self.score_correct} | Incorrect: {self.score_incorrect}")

    def check_answer(self, btn_index):
        question_data = self.questions[self.current_question_index]
        selected_option = self.option_buttons[btn_index].cget("text")
        correct_option = question_data["answer"]

        if selected_option == correct_option:
            self.option_buttons[btn_index].config(bg="green")
            self.score_correct += 1
        else:
            self.option_buttons[btn_index].config(bg="red")
            messagebox.showinfo("Wrong Answer", f"The correct answer was:
{correct_option}")
            self.score_incorrect += 1
            self.wrong_questions.append(question_data)

        for button in self.option_buttons:
            button.config(state=tk.DISABLED)
        self.progress_label.config(text=f"Progress: {self.current_question_index+1}/{len(self.questions)} | Correct: {self.score_correct} | Incorrect: {self.score_incorrect}")

        self.root.after(3000, self.next_question)

    def next_question(self):
        self.current_question_index += 1
        self.load_question()

    def end_quiz(self):
        message = f"Quiz Complete!\nCorrect: {self.score_correct}\nIncorrect: {self.score_incorrect}"
        if self.wrong_questions:
            message += "\n\nReview missed questions:"
            for q in self.wrong_questions:
                message += f"\n- {q['question']} (Answer: {q['answer']})"
        messagebox.showinfo("Results", message)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
