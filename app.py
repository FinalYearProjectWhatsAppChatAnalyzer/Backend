# import sys

# print(sys.path)

# import pandas as pd
# from wordcloud import WordCloud

from flask import Flask,render_template,request,render_template_string,redirect,url_for
from preprocess import preprocess
import helper as hp
import matplotlib.pyplot as plt
import io
import base64
import subprocess
# import psutil


app = Flask(__name__)

@app.route('/')
def home():
    # return 'Hello, World!'
    return render_template("index.html")


@app.route("/result")
def result():
    # Start the Streamlit app in a new process using subprocess
    streamlit_process = subprocess.Popen(["streamlit", "run", "result.py"])

    # Return a JSON response to let the client know the Streamlit app has started
    return jsonify(success=True)


@app.route('/aboutUs')
def about():
    return render_template("aboutUs.html")


@app.route('/faq')
def faq():
    return render_template("faq.html")


@app.route('/howTo')
def howTo():
    return render_template("howTo.html")


@app.route('/contactUs')
def contact():
    return render_template("contactUs.html")


if __name__=='__main__':
    app.run(debug=True)