from flask import Flask,render_template,request
import requests
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from questionGenerator import generateQuestion

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

signUp = 0
logIn = 0
QuestionsAttempted = 0
questionNumber = 0
score = 0
userLogin = 0
reviewExist = 0
username = None
questions = []

@app.route('/')
def startingPage():
    return render_template('starting_page.html')

@app.route('/signup')
def signUpPage():
    global signUp
    signUp = 1
    return render_template('signup.html')


@app.route('/login')
def login():
    global logIn
    logIn = 1
    return render_template('login.html')


@app.route('/lobby')
def lobbyPage():
    global userLogin
    global score
    global username
    score = 0
    print(userLogin)
    if userLogin == 1:
        return render_template('lobby.html', user_name = username)
    else:
        global logIn
        global signUp
        userLogin = 1
        email = request.args.get('email')
        password = request.args.get('password')
        print(email, password)
        if logIn == 1:
            user = User.query.filter_by(email=email).first()
            logIn = 0
            if user and check_password_hash(user.password, password):
                print('Login Success')
                username = user.username
                return render_template('lobby.html', user_name = username)
            else:
                return render_template('login.html')

        elif signUp == 1:
            username = request.args.get('username')
            password_hash = generate_password_hash(password)
            new_user = User(username=username, password=password_hash, email=email)
            db.session.add(new_user)
            db.session.commit()
            signUp = 0
            userLogin = 1
            print('User added login success')
            return render_template('lobby.html',user_name = username)
    # return render_template('lobby.html', user_name = user_info['name'])

@app.route('/practice', methods=['GET', 'POST'])
def practice():
    return render_template('practice.html')

@app.route('/practicequestion', methods=['GET', 'POST'])
def practicequestion():
    global questionNumber
    global questions
    questionNumber=0
    title = request.form.get('title')
    review = request.form.get('review')
    photo = request.files['image']
    filename = photo.filename
    photo.save('uploads/' + filename)
    #Multimodality Integration



    questions =[{'question': 'What is the name of the drawing by Hans Gustav Burkhardt?', 
                 'options': ['Plate 13: Designs with Cross, Chimayo: From Portfolio "Spanish Colonial Designs of New Mexico"', 'Coca Cola', 'Untitled', 'Marion Feasting the British Officer on Sweet Potatoes'], 
                 'correctOption': 'Untitled', 
                 'image': 'https://api.nga.gov/iiif/0895792b-7f50-4670-a452-317ab9e0a6b9/full/!400,400/0/default.jpg', 
                 'review': 'Untitled, a Drawing by Hans Gustav Burkhardt, was developed over a period spanning from 1980 to 1990, executed in the medium of watercolor and felt-tip pen on sketchbook paper.'}]
    ques = questions[questionNumber]
    print(title, review, photo)
    return render_template('practicequestion.html', question = ques, quesNum = questionNumber)


@app.route('/quiz', methods=['GET', 'POST'])
def quizPage():
    global QuestionsAttempted
    global questionNumber
    global questions
    global reviewExist
    questionNumber=0
    QuestionsAttempted += 1
    if reviewExist >0:
        review_text = request.form.get('review')
        rating = request.form.get('difficulty')
        print(review_text, rating)
    try:
        diff = request.form.get('questiondifficulty')
        print(diff)
    except:
        print()
    # questions = generateQuestion(1)
    questions =[{'question': 'What is the name of the drawing by Hans Gustav Burkhardt?', 'options': ['Plate 13: Designs with Cross, Chimayo: From Portfolio "Spanish Colonial Designs of New Mexico"', 'Coca Cola', 'Untitled', 'Marion Feasting the British Officer on Sweet Potatoes'], 'correctOption': 'Untitled', 'image': 'https://api.nga.gov/iiif/0895792b-7f50-4670-a452-317ab9e0a6b9/full/!400,400/0/default.jpg', 'review': 'Untitled, a Drawing by Hans Gustav Burkhardt, was developed over a period spanning from 1980 to 1990, executed in the medium of watercolor and felt-tip pen on sketchbook paper.'}]
    ques = questions[questionNumber]
    print(questionNumber)
    print(ques)
    print(ques['question'], ques['correctOption'])
    print()
    if questionNumber > len(questions):
        return render_template('review.html', review = questions[questionNumber]['review'], img = questions[questionNumber]['image'], score = score)
    return render_template('quiz.html', question = ques, quesNum = questionNumber)


@app.route('/review', methods=['GET', 'POST'])
def reviewPage():
    global score
    global questionNumber
    global reviewExist
    reviewExist += 1
    print(questionNumber)
    real_ans = questions[questionNumber]['correctOption']
    answer =request.values.get('answer')
    print(answer, real_ans, format(answer))
    if answer == real_ans:
        value = "Correct Answer"
        score+=1
    else:
        value = "Wrong Answer"
    print(score)
    return render_template('review.html', review = questions[questionNumber]['review'], img = questions[questionNumber]['image'], score = score, val = value)


@app.route('/results' , methods=['GET', 'POST'])
def resultPage():
    global score
    global QuestionsAttempted
    print(score)
    review_text = request.form.get('review')
    rating = request.form.get('difficulty')
    print(review_text, rating)
    return render_template('result.html', score = score, Noofques = QuestionsAttempted)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True, port='6969')