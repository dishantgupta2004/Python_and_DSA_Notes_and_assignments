# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quantum-mechanics')
def quantum_mechanics():
    return render_template('quantum.html')

@app.route('/wave-particle')
def wave_particle():
    return render_template('wave_particle.html')

@app.route('/uncertainty')
def uncertainty():
    return render_template('uncertainty.html')

if __name__ == '__main__':
    app.run(debug=True)