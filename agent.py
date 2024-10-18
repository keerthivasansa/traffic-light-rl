from re import S
from env import Environment
from tqdm import tqdm


class Agent:

    def __init__(self):
        self.env = Environment()
        self.values = {}
        self.policy = {}

        for st in self.env.get_states():
            self.values[st] = 0

    def choose(self, state, value_store, preserve=-1):
        actions = self.env.get_actions(state)
        curr_value = -1
        curr_action = -1

        for act in actions:
            nxt, reward, pres = self.env.perform_action(state, act, preserve)
            value = reward
            if nxt is not None:
                value += self.choose(nxt, value_store, pres)[1]
            value_store[(state, act)] += value

        return curr_action, curr_value

    def calc_values(self, epochs):
        value = {}
        for st in self.env.get_states():
            for act in self.env.get_actions(st):
                value[(st, act)] = 0

        tq = tqdm(range(1, epochs + 1))
        for e in tq:
            
            msg = ''
            for st in self.env.get_states():
                best_action = -1
                best_val = float('-inf')

                for a in self.env.get_actions(st):
                    value[(st, a)] //= e
                    if best_val < value[(st, a)]:
                        best_action = a
                        best_val = value[(st, a)]

                msg += f"{st}: {best_action}   "
            
            tq.set_description(msg)

            for st in self.env.get_states():
                self.choose(st, value)

        return value
