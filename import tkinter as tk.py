import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ex4 import QuizBrain
from ex2 import Question
from ex3 import question_data

question_bank = []
for questions in question_data:
    question_text = questions["Question"]
    question_answer = questions["correct_answer"]
    if isinstance(question_answer, list):
        question_answer = question_answer[0]
    question_bank.append(Question(question_text, question_answer))

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = tk.Tk()
        self.window.title("Quiz Game")
        self.window.config(bg="white", padx=10, pady=10)

        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.progress = ttk.Progressbar(self.window, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(10,0))
        self.progress_label = tk.Label(self.window, text="0%", bg="black", fg="white", font=("Arial", 12))
        self.progress_label.place(x=320, y=10)

        self.canvas = tk.Canvas(self.window, width=350, height=150, bg="white", highlightthickness=0)
        self.canvas.create_rectangle(10, 10, 340, 140, outline="black", width=8, fill="white")
        self.question_text = self.canvas.create_text(
            175, 75,
            width=320,
            text="",
            fill= "#000000",
            font=("Arial", 16, "italic")
        )
        self.canvas.grid(row=1, column=0, columnspan=3, pady=20)


        try:
            self.true_img = ImageTk.PhotoImage(Image.open("true.png").resize((60, 60)))
        except Exception:
            self.true_img = None
        self.true_button = tk.Button(
            self.window,
            image=self.true_img if self.true_img else None, 
            text="True" if not self.true_img else "",
            command=self.true_pressed,
            borderwidth=0,
            bg="white"
        )
        self.true_button.grid(row=2, column=0, sticky="sw", padx=30, pady=30)


        try:
            self.false_img = ImageTk.PhotoImage(Image.open("false.png").resize((60, 60)))
        except Exception:
            self.false_img = None
        if self.false_img:
            self.false_button = tk.Button(
                self.window,
                image=self.false_img,
                command=self.false_pressed,
                borderwidth=0,
                bg="white"
            )
        else:
            self.false_button = tk.Button(
                self.window,
                text="False",
                command=self.false_pressed,
                borderwidth=0,
                bg="white"
            )
        self.false_button.grid(row=2, column=2, sticky="se", padx=30, pady=30)

        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question() 
            self.canvas.itemconfig(self.question_text, text=q_text)
            percent = int((self.quiz.question_number / len(self.quiz.question_list)) * 100)
            self.progress["value"] = percent
            self.progress_label.config(text=f"{percent}%")
            self.true_button.config(state="normal")
            self.false_button.config(state="normal")
        else:
        
            if self.quiz.score > 10:
                end_text = f"The End\nScore: {self.quiz.score}\nYou're an American Connoisseur!"
            else:
                end_text = f"The End\nScore: {self.quiz.score}\nYou're bad!"
            self.canvas.itemconfig(self.question_text, text=end_text)
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
            self.progress["value"] = 100
            self.progress_label.config(text="100%")
    

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")
        self.window.after(1000, self.get_next_question)

if __name__ == "__main__":
    quiz = QuizBrain(question_bank)
    QuizInterface(quiz)