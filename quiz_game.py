import requests

from question_model import Question
class QuizGame:

    def __init__(self ):
        self.start_game()
    def print_category(self):

        # fetching all cathegories available in Open Trivia DB
        r = requests.get("https://opentdb.com/api_category.php")

        # converting data in JSON format
        r_json = r.json()
        categories_list = r_json['trivia_categories']
        #print(categories_list)

        for dict_list in categories_list:
            print(f"{dict_list['id']}:{dict_list['name']}")

    def choose_category(self):
        return int(input("Choose one category id\n"))

    def choose_number_of_question(self):
        return int(input("Select a number of question you want to answer up to 50 questions \n"))

    def start_game(self):
        self.print_category()
        category_id = self.choose_category()
        nber_of_question = self.choose_number_of_question()

        self.game(nber_of_question, category_id)

    def game(self, nber, cat_id) :
        print("===========================================================================")
        print("===================== WELCOME TO THE QUIZ GAME ============================")
        print("===========================================================================")

        #instantiate question
        questions = Question(nber , cat_id)

        # generate question an display
        s = questions.display_question()

        # End Game condition control
        if s.lower() =="n":
            print("Thanks for using the  taking part in the Quiz!!")
            exit()






