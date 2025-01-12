from qcircuit import UniformDistributionCircuit
from dotenv import load_dotenv
import os


class EightBall:
   def __init__(self, sampler):
      """
      Initializes:
         self.answers (list): list of all possible eight ball outcomes
         self.random_sampler: method of sampling random number -- meant to use quantum sampler.
      """
      # List of Answers
      self.answers = [
         "The wavefunction collapsed to a positive outcome",
         "Your question has been projected into a |+> state", 
         "the electron spin is giving that a huge thumbs up by the right hand rule", 
         "The quantum algorithm solved it—’yes’ is the answer!", 
         "Unitary evolution of your state leads to a definite YES",
         "The expectation value of that observable is a clear affirmative",
         "The qubits have spoken. Go for it!",
         "The wavefunction’s interference pattern suggests success",
         "Alice and Bob measured NO so that means you will measure YES!",
         "Is Schrodenger’s cat dead or alive? YES!",
         "The wavefunction collapsed to NO!",
         "NO, The wavefunctions have destructively interfered",
         "Even the electron spin is giving a thumbs down by the right hand rule",
         "There is no branch of the wavefunction where that is a good idea",
         "The expectation value of that observable is an obvious NO",
         "Heisenberg might agree with you, but we can't be 100% certain",
         "Your fate is in superposition — it could go either way!",
         "The state is still in a superposition. Maybe try measuring again",
         "Even Schodenger has no clue!",
         "The outcome depends on your measurement basis"
      ]
      # Random Number Generator
      self.random_sampler = sampler
   
   def play(self):
      user_in = input("Welcome to Eight Ball! Type 'q' to quit. Type your query and let the universe guide you. \n")
      while user_in != 'q':
         val = self.random_sampler.measure(sample_type="sim")
         print(self.answers[val])
         user_in = input("\n")
