import tkinter as tk
from tkinter import messagebox, Toplevel
import random
from .questions import question_bank

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("C963 Quiz App")
        self.root.geometry("1000x700")

        self.score = 0
        self.incorrect = 0
        self.current_question_index = 0
        self.questions = random.sample(question_bank, len(question_bank))
        self.incorrect_questions = []

        self.setup_ui()

    def setup_ui(self):
        """Initialize all UI components"""
        self.question_label = tk.Label(self.root, text="", font=("Arial", 18), 
                                     wraplength=950, justify="left")
        self.question_label.pack(pady=30)

        self.buttons = []
        for i in range(4):
            button = tk.Button(self.root, text="", width=70, height=3, 
                              wraplength=800, command=lambda b=i: self.check_answer(b))
            button.pack(pady=6)
            self.buttons.append(button)

        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.feedback_label.pack(pady=15)

        self.progress_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.progress_label.pack(pady=20)

        self.load_question()

    def load_question(self):
        """Load the current question and options"""
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            self.question_label.config(text=question_data["question"])

            shuffled_options = question_data["options"][:]
            random.shuffle(shuffled_options)

            self.current_options = shuffled_options
            self.correct_option = question_data["answer"]

            for i, option in enumerate(shuffled_options):
                self.buttons[i].config(text=option, bg="SystemButtonFace", state="normal")

            self.feedback_label.config(text="")
            self.update_progress()
        else:
            self.show_summary()

    def check_answer(self, selected_index):
        """Check if the selected answer is correct"""
        selected_option = self.current_options[selected_index]
        correct_option = self.correct_option

        for button in self.buttons:
            button.config(state="disabled")

        if selected_option == correct_option:
            self.handle_correct_answer(selected_index, correct_option)
        else:
            self.handle_incorrect_answer(selected_index, correct_option)

    def handle_correct_answer(self, selected_index, correct_option):
        """Handle correct answer scenario"""
        self.score += 1
        self.buttons[selected_index].config(bg="green")
        self.feedback_label.config(
            text=f"Correct! ✅ The answer is: {correct_option}",
            fg="green"
        )
        self.root.after(3000, self.next_question)

    def handle_incorrect_answer(self, selected_index, correct_option):
        """Handle incorrect answer scenario"""
        self.incorrect += 1
        self.buttons[selected_index].config(bg="red")
        self.incorrect_questions.append({
            "question": self.questions[self.current_question_index]["question"],
            "your_answer": self.current_options[selected_index],
            "correct_answer": correct_option
        })
        messagebox.showinfo("Incorrect ❌", f"The correct answer was:\n\n{correct_option}")
        self.root.after(800, self.next_question)

    def next_question(self):
        """Move to the next question"""
        self.current_question_index += 1
        self.load_question()

    def update_progress(self):
        """Update the progress display"""
        progress_text = (f"Question {self.current_question_index + 1} of {len(self.questions)} | "
                        f"Correct: {self.score} | Incorrect: {self.incorrect}")
        self.progress_label.config(text=progress_text)

    def show_summary(self):
        """Show quiz summary and incorrect answers"""
        messagebox.showinfo("Quiz Completed",
                          f"You got {self.score} correct and {self.incorrect} incorrect "
                          f"out of {len(self.questions)} total questions!")

        if self.incorrect_questions:
            self.show_review_window()

    def show_review_window(self):
        """Display a window with incorrect answers for review"""
        review_window = Toplevel(self.root)
        review_window.title("Review Incorrect Answers")
        review_window.geometry("1000x700")

        review_label = tk.Label(review_window, text="Review of Incorrect Answers",
                              font=("Arial", 20))
        review_label.pack(pady=20)

        text_area = tk.Text(review_window, wrap="word", font=("Arial", 14), 
                           width=120, height=30)
        text_area.pack(pady=10)

        for idx, item in enumerate(self.incorrect_questions, 1):
            text_area.insert("end", f"{idx}. {item['question']}\n")
            text_area.insert("end", f"   Your answer: {item['your_answer']}\n")
            text_area.insert("end", f"   Correct answer: {item['correct_answer']}\n\n")

        text_area.config(state="disabled")