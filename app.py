from flask import Flask, render_template, request  

app = Flask(__name__)

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

@app.route('/samplequestions', methods=['GET', 'POST'])
def samplequestions():
    selected_answers = {}
    correct_answers = {
        'question1': 'Paris',
        'question2': 'Oxygen',
        'question3': 'Authoritarianism',
        'question4': 'Quantum Entanglement',
        'question5': 'Absorption of excess atmospheric CO2',
        'question6': 'Cultural influence and attractiveness',
        'question7': 'Alfred Wegener',
        'question8': 'It imposed severe reparations, leading to hyperinflation and economic hardship.',
        'question9': 'World Health Organization (WHO)',
        'question10': 'Division of governmental authority into different branches to prevent abuse of power'
    }
    score = 0

    if request.method == 'POST':
        # Capture selected answers from the form
        selected_answers = {
            'question1': request.form.get('question1'),
            'question2': request.form.get('question2'),
            'question3': request.form.get('question3'),
            'question4': request.form.get('question4'),
            'question5': request.form.get('question5'),
            'question6': request.form.get('question6'),
            'question7': request.form.get('question7'),
            'question8': request.form.get('question8'),
            'question9': request.form.get('question9'),
            'question10': request.form.get('question10')
        }

        # Calculate score
        for question, correct_answer in correct_answers.items():
            if selected_answers.get(question) == correct_answer:
                score += 1  # Increase score for correct answers
            else:
                score -= 1  # Decrease score for wrong answers

    return render_template('samplequestions.html', selected_answers=selected_answers, correct_answers=correct_answers, score=score)
@app.route('/maintest')
def maintest():
    return render_template('maintest.html')


if __name__ == "__main__":
    app.run(debug=True)