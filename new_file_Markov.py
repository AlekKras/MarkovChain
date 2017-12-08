'''
Modifications:
1) Using trigram in base state (None, None, None)
'''
import random
class Markov(object):

    def __init__(self):

        self.model = {}  # maps states to lists of words
        self.state = (None, None, None)  # last three words processed

    def add(self, word):

        if self.state in self.model:
            # we have an existing list of words for this state
            # just add new word
            self.model[self.state].append(word)
        else:
            # first occurrence of this state, create a new list
            self.model[self.state] = [word]
        # transition to the next state given next word
        self._transition(word)

    def randomNext(self):

        # get list of next words for this state
        lst = self.model[self.state]
        # choose one at random
        choice = random.choice(lst)
        # transition to next state, given the word choice
        self._transition(choice)
        return choice

    def _transition(self, next):

        # help function to construct next state
        self.state = (self.state[1], next)

    def reset(self):

        self.state = (None, None, None)
