
from flask import Flask, render_template, request, redirect, url_for, session
import requests
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class Question:
    def __init__(self, nber, cat_id):
        self.nber_of_question = nber
        self.category_id = cat_id

    def question_pool_gen(self):
        url = f"https://opentdb.com/api.php?amount={self.nber_of_question}&category={self.category_id}&type=multiple"
        response = requests.get(url)
        questions = response.json()['results']
        for question in questions:
            question['choices'] = [question['correct_answer']] + question['incorrect_answers']
            random.shuffle(question['choices'])
        return questions
    
@app.route('/question', methods=['GET', 'POST'])
def question():
    #Ensure the session contains questions and current index: redirect if not
    if 'questions' not in session or  'current_question_index' not in session:
        return redirect(url_for('quiz'))
    
    questions = session.get('questions',[])
    current_index = session.get('current_question_index',0)

    if request.method == 'POST':
        user_answer = request.form.get('choice')

        correct_answer = questions[current_index]['correct_answer']
        if user_answer == correct_answer:
            session['score'] = session.get('score',0) + 1
        session['current_question_index'] = current_index + 1

        if current_index + 1 < len(questions):
            return redirect(url_for('question'))
        else:
            return redirect(url_for('result'))
           
    return render_template('question.html', question=questions[current_index])

class QuizGame:
    def fetch_categories(self):
        response = requests.get("https://opentdb.com/api_category.php")
        categories = response.json()['trivia_categories']
        return categories

    def start_game(self, nber_of_question, category_id):
        questions = Question(nber_of_question, category_id)
        session['questions'] = questions.question_pool_gen()
        session['current_question_index'] = 0
        session['score'] = 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    quiz_game = QuizGame()
    if request.method == 'POST':
        session['user_name']= request.form['name']
        category_id = int(request.form['category'])
        num_questions = int(request.form['num_questions'])
        session['current_category'] = category_id
        session['progress'] = {}
        session['scores']={}
        quiz_game.start_game(num_questions, category_id)
        return redirect(url_for('question'))
    
    categories = quiz_game.fetch_categories()
    return render_template('quiz.html', categories=categories)



@app.route('/result')
def result():
    score = session.get('score', 0)
    progress = session.get('progress', {})
    user_name = session.get('user_name','Guest')
    session.clear()
    return render_template('result.html', score=score,user_name=user_name,progress=progress)

if __name__ == '__main__':
    app.run(debug=True)

