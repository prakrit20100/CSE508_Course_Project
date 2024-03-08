from flask import Flask,render_template,request
import requests

app = Flask(__name__)
user_info = {
    'name': None
}
questions = [
        {
            'question': 'Who painted the Mona Lisa?',
            'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
            'correctOption': 'Leonardo da Vinci'
        },
        {
            'question': 'Who painted The Starry Night?',
            'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
            'correctOption': 'Leonardo da Vinci'
        }
    ]
@app.route('/')
def startingPage():
    return render_template('starting_page.html')

@app.route('/quiz')
def quizPage():
    name = request.args.get('username')
    user_info['name'] = name
    return render_template('quiz_template.html', questions = questions)

@app.route('/results')
def resultPage():
    score = 0
    for i in range(len(questions)):
        real_ans = questions[i]['correctOption']
        nameosfque = 'q'+str(i)
        answer = request.args.get(nameosfque)
        if answer == real_ans:
            score+=1
    print(score)
    return render_template('result_template.html', score = score, questions = questions)

if __name__ == '__main__':
    app.run(debug=True, port='6969')