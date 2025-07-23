
from ex4 import QuizBrain
from ex2 import Question
import tkinter as tk
from PIL import Image, ImageTk
class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = tk.Tk()
        self.window.title("Quiz Game")
        self.window.config(padx=20, pady=20, bg="#375362")

        self.score_label = tk.Label(text="Score: 0", fg="white", bg="#375362", font=("Arial", 12))
        self.score_label.grid(row=0, column=1)

        self.canvas = tk.Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150, 125,
            width=280,
            text="",
            fill="#375362",
            font=("Arial", 16, "italic")
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

       
        try:
            self.true_img = ImageTk.PhotoImage(Image.open("true.png").resize((50, 50)))
        except Exception:
            self.true_img = None
        try:
            self.false_img = ImageTk.PhotoImage(Image.open("false.png").resize((50, 50)))
        except Exception:
            self.false_img = None

        self.true_button = tk.Button(
            image=self.true_img if self.true_img else None,
            text="True" if not self.true_img else "",
            command=self.true_pressed,
            borderwidth=0
        )
        self.true_button.grid(row=2, column=0)

        self.false_button = tk.Button(
            image=self.false_img if self.false_img else None,
            text="False" if not self.false_img else "",
            command=self.false_pressed,
            borderwidth=0
        )
        self.false_button.grid(row=2, column=1)

        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.question_list[self.quiz.question_number].text
            self.canvas.itemconfig(self.question_text, text=q_text)
            self.score_label.config(text=f"Score: {self.quiz.score}")
            self.true_button.config(state="normal")
            self.false_button.config(state="normal")
        else:
            self.canvas.itemconfig(self.question_text, text="The End")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
            self.score_label.config(text=f"Final Score: {self.quiz.score}")

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
        self.window.after(1000, self.next_question_step)

    def next_question_step(self):
        self.quiz.question_number += 1
        self.get_next_question()

if __name__ == "__main__":
    QuizInterface(quiz)
