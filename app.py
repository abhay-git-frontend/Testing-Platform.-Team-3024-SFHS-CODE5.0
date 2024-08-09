from flask import Flask, render_template

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

@app.route("/samplequestions")
def samplequestions():
    return render_template('samplequestions.html')

@app.route("/maintest")
def maintest():
    return render_template('maintest.html')


if __name__ == "__main__":
    app.run(debug=True)