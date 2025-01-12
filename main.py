from qcircuit import UniformDistributionCircuit
from eightball import EightBall
from dotenv import load_dotenv
import os



if __name__ == '__main__':
   load_dotenv()
   IBM_API_KEY = os.getenv("IBM_TOKEN")
   eight_ball_distr = UniformDistributionCircuit(20, IBM_API_KEY)
   eight_ball_game = EightBall(eight_ball_distr)

   eight_ball_game.play()

