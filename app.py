from flask import Flask, render_template, jsonify
from qcircuit import UniformDistributionCircuit
from dotenv import load_dotenv
from eightball import EightBall
import os

# 1. Load environment variables
load_dotenv()
IBM_API_KEY = os.getenv("IBM_TOKEN")

# 2. Create our Flask application
app = Flask(__name__)

# 3. Initialize your quantum sampler and the EightBall
quantum_sampler = UniformDistributionCircuit(20, IBM_API_KEY)  
eight_ball = EightBall(quantum_sampler)

def get_random_answer():
    """Helper function to get a random answer"""
    random_index = quantum_sampler.measure(sample_type="sim")
    return eight_ball.answers[random_index]

@app.route('/')
def index():
    """
    Renders the Magic 8-Ball page, injecting a random answer from the quantum sampler.
    """
    # Get initial random answer
    initial_answer = get_random_answer()
    return render_template('index.html', answer=initial_answer)

@app.route('/get_answer')
def get_answer():
    """Endpoint to get a new random answer"""
    return jsonify({'answer': get_random_answer()})

if __name__ == '__main__':
    # 5. Run the Flask dev server
    app.run(port=5001, debug=True)