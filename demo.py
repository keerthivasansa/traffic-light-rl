from agent import Agent
from env import Environment

agent = Agent()
env = Environment()

print(agent.calc_values(epochs=25))