from flask import Flask, render_template
import script

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", options=script.box())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)