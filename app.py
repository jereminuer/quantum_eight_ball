from flask import Flask, render_template
from qcircuit import UniformDistributionCircuit
from dotenv import load_dotenv
from eightball import EightBall
import os

# 1. Load environment variables
load_dotenv()
IBM_API_KEY = os.getenv("IBM_TOKEN")

# 2. Create our Flask application
app = Flask(__name__)

# 3. Import the EightBall class 


# 4. Initialize your quantum sampler and the EightBall
#    - If your UniformDistributionCircuit needs a quantum backend or token, you can load it via os.getenv.
#    - If not, and you just want local simulation, you can remove the token.
quantum_sampler = UniformDistributionCircuit(20, IBM_API_KEY)  
eight_ball = EightBall(quantum_sampler)

@app.route('/')
def index():
    """
    Renders the Magic 8-Ball page, injecting a random answer from the quantum sampler.
    """
    # Call the measure() method to pick a random index
    random_index = quantum_sampler.measure(sample_type="sim")
    # Retrieve the corresponding answer
    eight_ball_answer = eight_ball.answers[random_index]

    # Render the HTML, passing the 'eight_ball_answer' variable into the template
    return render_template('index.html', answer=eight_ball_answer)


if __name__ == '__main__':
    # 5. Run the Flask dev server
    app.run(port=5001, debug=True)