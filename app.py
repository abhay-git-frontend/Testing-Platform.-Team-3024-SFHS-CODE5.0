from flask import Flask, render_template, request, url_for, redirect, session, jsonify
import json
import random
import subprocess
import sqlite3
app = Flask(__name__)
app.secret_key = '47c34e58e179a8a09903c0736da8dd04' 

@app.route("/")
def hello_world():
    return render_template('index.html')
    # return "<p>Hello, World!</p>"

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/testrules")
def testrules():
    return render_template('testrules.html')

all_questions = {
    'What is the capital of France?': ['Paris', 'London', 'Rome', 'Berlin'],
    'What is the chemical symbol for Oxygen?': ['Oxygen', 'Hydrogen', 'Carbon Dioxide', 'Nitrogen'],
    'Which type of government is characterized by a concentration of power in one leader?': ['Authoritarianism', 'Democracy', 'Communism', 'Monarchy'],
    'Which concept in physics describes the phenomenon where particles become interconnected regardless of distance?': ['Quantum Entanglement', 'Classical Mechanics', 'String Theory', 'Relativity'],
    'What is the process by which excess atmospheric CO2 is absorbed?': ['Absorption of excess atmospheric CO2', 'Reduction of CO2 emissions', 'Afforestation', 'Energy conservation'],
    'Which factor is associated with cultural influence and attractiveness?': ['Cultural influence and attractiveness', 'Economic stability', 'Political freedom', 'Technological advancement'],
    'Who is known for the theory of continental drift?': ['Alfred Wegener', 'Charles Darwin', 'Isaac Newton', 'Galileo Galilei'],
    'What was one significant economic impact of the Treaty of Versailles on Germany?': ['It imposed severe reparations, leading to hyperinflation and economic hardship.', 'It led to increased trade and economic growth.', 'It resulted in a stronger military alliance.', 'It had minimal impact on the economy.'],
    'Which organization is responsible for international public health?': ['World Health Organization (WHO)', 'United Nations (UN)', 'International Monetary Fund (IMF)', 'World Bank'],
    'What is the purpose of dividing governmental authority into different branches?': ['Division of governmental authority into different branches to prevent abuse of power', 'Establishment of a single governing authority', 'Centralization of economic resources', 'Restriction of political freedoms']
}

@app.route('/samplequestions', methods=['GET', 'POST'])
def samplequestions():
    correct_answers = {
        'What is the capital of France?': 'Paris',
        'What is the chemical symbol for Oxygen?': 'Oxygen',
        'Which type of government is characterized by a concentration of power in one leader?': 'Authoritarianism',
        'Which concept in physics describes the phenomenon where particles become interconnected regardless of distance?': 'Quantum Entanglement',
        'What is the process by which excess atmospheric CO2 is absorbed?': 'Absorption of excess atmospheric CO2',
        'Which factor is associated with cultural influence and attractiveness?': 'Cultural influence and attractiveness',
        'Who is known for the theory of continental drift?': 'Alfred Wegener',
        'What was one significant economic impact of the Treaty of Versailles on Germany?': 'It imposed severe reparations, leading to hyperinflation and economic hardship.',
        'Which organization is responsible for international public health?': 'World Health Organization (WHO)',
        'What is the purpose of dividing governmental authority into different branches?': 'Division of governmental authority into different branches to prevent abuse of power'
    }

    # Shuffle options for each question
    questions = {q: random.sample(a, len(a)) for q, a in all_questions.items()}
    score = 0
    selected_answers = {}

    if request.method == 'POST':
        # Capture selected answers from the form
        selected_answers = {
            q: request.form.get(q)
            for q in all_questions.keys()
        }

        # Calculate score
        for question, correct_answer in correct_answers.items():
            if selected_answers.get(question) == correct_answer:
                score += 1  # Increase score for correct answers
            else:
                score -= 1  # Decrease score for wrong answers

    return render_template('samplequestions.html', questions=questions, selected_answers=selected_answers, correct_answers=correct_answers, score=score)


@app.route('/maintest', methods=['GET', 'POST'])
def maintest():

    return render_template('maintest.html')
@app.route("/")
def home():
    return render_template('index.html')  # Ensure you have an index.html file

@app.route('/home')
def home_redirect():
    return redirect(url_for('home'))

@app.route('/start-camera', methods=['GET'])
def start_camera():
    try:
        # Start the camera script as a subprocess
        subprocess.Popen(['python', 'camera.py'])
        return jsonify({"status": "Camera started successfully"}), 200
    except Exception as e:
        return jsonify({"status": "Failed to start camera", "error": str(e)}), 500
    
@app.route('/home')
def homee():
    return render_template('index.html')
def start_test():
    # If the test has already been completed or the user has been redirected, prevent access
    if session.get('test_redirected', False):
        return redirect(url_for('homee'))
    return render_template('maintest.html')


@app.route('/end-test')
def end_test():
    session['test_started'] = False
    session['test_redirected'] = True
    return redirect(url_for('homee'))


DATABASE = 'form_data.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    mobile = request.form['mobile']
    dob = request.form['dob']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the email already exists
    cursor.execute('SELECT * FROM form_data WHERE email = ?', (email,))
    existing_entry = cursor.fetchone()

    if existing_entry:
        conn.close()
        return jsonify({'status': 'error', 'message': 'You cannot retake the test. Your details already exist.'})

    # Insert the new data into the database
    cursor.execute('INSERT INTO form_data (name, email, age, mobile, dob) VALUES (?, ?, ?, ?, ?)',
                   (name, email, age, mobile, dob))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Your details have been recorded successfully. You can start the test.'})
if __name__ == "__main__":
    app.run(debug=True)