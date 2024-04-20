from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)


class QuizApp:
    def __init__(self):
        self.signUp = 0
        self.logIn = 0
        self.questionNumber = -1
        self.score = 0
        self.user_info = {
            'name': None
        }
        self.questions = [
        {
            'question': 'Who painted the Mona Lisa?',
            'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
            'correctOption': 'Leonardo da Vinci',
            'image' : 'https://api.nga.gov/iiif/c6ed44da-05f3-4798-916d-e2f5030b0fd7/full/!200,200/0/default.jpg',
            'review': 'Huge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge Text'
        },
        {
            'question': 'Who painted The Starry Night? Who painted the Mona Lisa? Who painted the Mona Lisa?',
            'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
            'correctOption': 'Leonardo da Vinci',
            'image' : 'https://api.nga.gov/iiif/c6ed44da-05f3-4798-916d-e2f5030b0fd7/full/!200,200/0/default.jpg',
            'review': 'Huge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge Text'

        },
        {
            'question': 'Who painted The Starry Night? Who painted the Mona Lisa? Who painted the Mona Lisa?',
            'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
            'correctOption': 'Leonardo da Vinci',
            'image' : 'https://api.nga.gov/iiif/c6ed44da-05f3-4798-916d-e2f5030b0fd7/full/!200,200/0/default.jpg',
            'review': 'Huge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge Text'

        },
        {
            'question': 'Who painted The Starry Night? Who painted the Mona Lisa? Who painted the Mona Lisa?',
            'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
            'correctOption': 'Leonardo da Vinci',
            'image' : 'https://api.nga.gov/iiif/c6ed44da-05f3-4798-916d-e2f5030b0fd7/full/!200,200/0/default.jpg',
            'review': 'Huge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge Text'

        },
        {
            'question': 'Who painted The Starry Night? Who painted the Mona Lisa? Who painted the Mona Lisa?',
            'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
            'correctOption': 'Leonardo da Vinci',
            'image' : 'https://api.nga.gov/iiif/c6ed44da-05f3-4798-916d-e2f5030b0fd7/full/!200,200/0/default.jpg',
            'review': 'Huge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge Text'

        },
        {
            'question': 'Who painted The Starry Night? Who painted the Mona Lisa? Who painted the Mona Lisa?',
            'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
            'correctOption': 'Leonardo da Vinci',
            'image' : 'https://api.nga.gov/iiif/c6ed44da-05f3-4798-916d-e2f5030b0fd7/full/!200,200/0/default.jpg',
            'review': 'Huge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge Text'

        },
        {
            'question': 'Who painted The Starry Night? Who painted the Mona Lisa? Who painted the Mona Lisa?',
            'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
            'correctOption': 'Leonardo da Vinci',
            'image' : 'https://api.nga.gov/iiif/c6ed44da-05f3-4798-916d-e2f5030b0fd7/full/!200,200/0/default.jpg',
            'review': 'Huge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge Text'

        },
        {
            'question': 'Who painted The Starry Night? Who painted the Mona Lisa? Who painted the Mona Lisa?',
            'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
            'correctOption': 'Leonardo da Vinci',
            'image' : 'https://api.nga.gov/iiif/c6ed44da-05f3-4798-916d-e2f5030b0fd7/full/!200,200/0/default.jpg',
            'review': 'Huge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge Text'

        },
        {
            'question': 'Who painted The Starry Night? Who painted the Mona Lisa? Who painted the Mona Lisa?',
            'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
            'correctOption': 'Leonardo da Vinci',
            'image' : 'https://api.nga.gov/iiif/c6ed44da-05f3-4798-916d-e2f5030b0fd7/full/!200,200/0/default.jpg',
            'review': 'Huge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge Text'

        },
        {
            'question': 'Who painted The Starry Night? Who painted the Mona Lisa? Who painted the Mona Lisa?',
            'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
            'correctOption': 'Leonardo da Vinci',
            'image' : 'https://api.nga.gov/iiif/c6ed44da-05f3-4798-916d-e2f5030b0fd7/full/!200,200/0/default.jpg',
            'review': 'Huge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge Text'

        },
        {
            'question': 'Who painted The Starry Night? Who painted the Mona Lisa? Who painted the Mona Lisa?',
            'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
            'correctOption': 'Leonardo da Vinci',
            'image' : 'https://api.nga.gov/iiif/c6ed44da-05f3-4798-916d-e2f5030b0fd7/full/!200,200/0/default.jpg',
            'review': 'Huge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge TextHuge Text'

        }
            ]

    def starting_page(self):
        return render_template('starting_page.html')

    def sign_up_page(self):
        self.signUp = 1
        return render_template('signup.html')

    def login(self):
        self.logIn = 1
        return render_template('login.html')

    def lobby_page(self):
        email = request.args.get('email')
        password = request.args.get('password')
        if self.logIn == 1:
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                username = user.username
                return render_template('lobby.html', user_name=username)
            else:
                return render_template('login.html')
        elif self.signUp == 1:
            username = request.args.get('username')
            password_hash = generate_password_hash(password)
            new_user = User(username=username, password=password_hash, email=email)
            db.session.add(new_user)
            db.session.commit()
            return render_template('lobby.html', user_name=username)

    def quiz_page(self):
        self.questionNumber += 1
        ques = self.questions[self.questionNumber]
        if self.questionNumber > len(self.questions):
            return render_template('review.html', review=self.questions[self.questionNumber]['review'],
                                   img=self.questions[self.questionNumber]['image'], score=self.score)
        return render_template('quiz.html', question=ques, quesNum=self.questionNumber)

    def review_page(self):
        real_ans = self.questions[self.questionNumber]['correctOption']
        answer = request.values.get('answer')
        if answer == real_ans:
            value = "Correct Answer"
            self.score += 1
        else:
            value = "Wrong Answer"
        return render_template('review.html', review=self.questions[self.questionNumber]['review'],
                               img=self.questions[self.questionNumber]['image'], score=self.score, val=value)

    def result_page(self):
        return render_template('result.html', score=self.score, Noofques=self.questionNumber)


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def starting_page():
    return quiz_app.starting_page()


@app.route('/signup')
def sign_up_page():
    return quiz_app.sign_up_page()


@app.route('/login')
def login():
    return quiz_app.login()


@app.route('/lobby')
def lobby_page():
    return quiz_app.lobby_page()


@app.route('/quiz')
def quiz_page():
    return quiz_app.quiz_page()


@app.route('/review', methods=['GET', 'POST'])
def review_page():
    return quiz_app.review_page()


@app.route('/results')
def result_page():
    return quiz_app.result_page()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    quiz_app = QuizApp()
    app.run(debug=True, port='6969')
