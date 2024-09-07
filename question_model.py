#class Question:

# Creating the question class which takes a question and an answer
##   def __init__(self, q_text, q_answer):
##        self.text = q_text
##        self.answer = q_answer

import html
import random
import requests
import json
class Question:
    def __init__(self, nber, cat_id):
        self.nber_of_question = nber
        self.category_id = cat_id
        self.score = 0
    def question_pool_gen(self) -> list:
        url = f"https://opentdb.com/api.php?amount={self.nber_of_question}&category={self.category_id }"
        db = requests.get(url)
        db_json = db.json()
        # with open("data_bank.json", "w") as f:
        #    json.dump(db.json(), f, indent=4)
        return db_json["results"]
    def shuffle_choices(self,rand_list ) -> list:
        random.shuffle(rand_list)
        return rand_list

    def print_shuffled_choices(self, rand_list) :
        for choice_index, choice_ans in enumerate(rand_list):
            print(f"{choice_index + 1}. {html.unescape(choice_ans)}")

    def display_question(self):
        question_pool = self.question_pool_gen()

        # go over the question list and print for player
        for actual_question in question_pool:

            # print the actual question for user
            text = html.unescape(actual_question["question"])

            #print the actual question
            print(text)

            # combine correct and incorrect answers as a list
            answer_list = html.unescape(actual_question["incorrect_answers"])
            correct_ans = html.unescape(actual_question["correct_answer"])
            answer_list.extend([correct_ans])

            # shuffling the answer list before proposing to the user
            # by calling shuffle_choices function
            multiple_choice = self.shuffle_choices(answer_list)

            # print list of shuffled choices by calling print_shuffled_choices functions
            self.print_shuffled_choices(multiple_choice)

            # get player choice by calling get_player_choice fonction
            player_choice_index = self.get_player_choice(answer_list)

            # check player answer
            player_ans = multiple_choice[player_choice_index]

            # correct_text = html.unescape(actual_question["correct_answer"])
            if player_ans == correct_ans:
                print("Your answer is CORRECT!\n")
                self.score += 1
            else:
                print(f"Your answer is Wrong. The correct answer is: {correct_ans}\n")
        print(f"Your score is: {self.score }/{self.nber_of_question }\n")
        s = input(f"Do you want to continue with the challenge? Y or N (Y=YES; N=NO)\n")
        return s

    # def get_player_choice(self, rand_list)-> int:
    #     n = len(rand_list)
    #     while True:
    #         match n:
    #             case 4:
    #                 user_choice = int(input("Enter your choice\n"))
    #                 if user_choice in range(1, 5):
    #                     return user_choice - 1
    #                 else:
    #                     print("invalid input: Enter your choice\n")
    #             case 2:
    #                 user_choice = int(input("Enter your choice\n"))
    #                 if user_choice in range(1, 3):
    #                     return user_choice - 1
    #                 else:
    #                     print("invalid input: Enter your choice\n")
    def get_player_choice(self, rand_list) -> int:
        n = len(rand_list)
        while True:
            try:
                if n == 4:
                    user_choice = int(input("Enter your choice (1-4):\n"))
                    if 1 <= user_choice <=4:
                        return user_choice -1
                    else:
                        print("Invalid input. Please enter a number between 1 and 4")
                elif n==2:
                    user_choice = int(input("Enter your choice (1-2):\n"))
                    if 1 <= user_choice <=2:
                        return user_choice -1
                    else:
                        print("Invalid input. Please enter a number between 1 and 2.")
            except ValueError:
                print("Invalid input. Please enter a valid integer")
         


