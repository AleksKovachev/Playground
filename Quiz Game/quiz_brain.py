class QuizBrain:

    def __init__(self, question_list):
        self.question_number = 0
        self.score = 0
        self.question_list = question_list
        self.current_question = self.question_list[self.question_number]
        self.off = False


    def still_has_questions(self):
        '''Pass'''
        return self.question_number < len(self.question_list)


    def next_question(self):
        '''Pass'''
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        user_answer = input((f"Q.{self.question_number}\nCategory: {self.current_question.category}\n"
                                f"Difficulty: {self.current_question.difficulty.capitalize()}\n"
                                f"{self.current_question.text} (True/False): "))
        self.check_answer(user_answer, self.current_question.answer)


    def check_answer(self, user_answer, correct_answer):
        '''Pass'''
        if (correct_answer.lower() == "true" and user_answer.lower() in ["true", "t", "1"]) or (correct_answer.lower() == "false" and user_answer.lower() in ["false", "f", "0"]):
            print("You got it right!")
            self.score += 1
            print(f'The correct answer is: {correct_answer}.')
            print(f'Your current score is: {self.score}/{len(self.question_list)}\n')
        elif (correct_answer.lower() == "true" and user_answer.lower() in ["false", "f", "0"]) or (correct_answer.lower() == "false" and user_answer.lower() in ["true", "t", "1"]):
            print("That's wrong.")
            print(f'The correct answer was: {correct_answer}.')
            print(f'Your current score is: {self.score}/{len(self.question_list)}\n')
        elif user_answer.lower() in ["o", "off", "e", "exit", "q", "quit"]:
            self.off = True
        else:
            print("Wrong input!")
            user_answer = input((f"Q.{self.question_number}: {self.current_question.text} (True/False): "))
            self.check_answer(user_answer, self.current_question.answer)
