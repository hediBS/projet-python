from ex2 import Question
from ex4 import QuizBrain
from ex3 import question_data
from ex5  import QuizInterface
if __name__ == "__main__":

    from ex3 import question_data
    question_bank = []
    for questions in question_data:
        question_text = questions["Question"]
        question_answer = questions["correct_answer"]
        question_bank.append(Question(question_text, question_answer))
    quiz = QuizBrain(question_bank)
    QuizInterface(quiz)

while quiz.still_has_questions():
    print(quiz.next_question())
print("The End")
print(f"Your final score was: {quiz.score}/{len(question_bank)}")