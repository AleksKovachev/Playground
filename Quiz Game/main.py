from question_model import Question
from data import question_data
from quiz_brain import QuizBrain
from random import shuffle

question_bank = []
questions = 0

for question in question_data:
    question_category = question["category"]
    question_difficulty = question["difficulty"]
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer, question_category, question_difficulty)
    question_bank.append(new_question)

shuffle(question_bank)
quiz = QuizBrain(question_bank)

while quiz.still_has_questions() and not quiz.off:
    quiz.next_question()
    questions += 1

if not quiz.still_has_questions() or quiz.off:
    print("You've completed the quiz!")
    print(f"Your final score is: {quiz.score}/{questions - 1}")
