import re
import random
from collections import defaultdict, deque

class MarkovChain:

  def __init__(self, keywords=2):
    self.keywords = keywords
    self.dict = defaultdict(list)
    self._punctuation_regex = re.compile('[,.!;\?\:\-\[\]\n]+')
    self._seeded = False
    self.__seed_me()

  def __seed_me(self, rand_seed=None):
    if self._seeded is not True:
      try:
        if rand_seed is not None:
          random.seed(rand_seed)
        else:
          random.seed()
        self._seeded = True
      except NotImplementedError:
        self._seeded = False

  """
  " Build Markov Chain from data source.
  " Use add_file() or add_string() to add the appropriate format source
  """
  def add_file(self, file_path):
    content = ''
    with open(file_path, 'r') as fh:
      self.__add_source_data(fh.read())

  def add_string(self, str):
    self.__add_source_data(str)

  def __add_source_data(self, str):
    clean_str = self._punctuation_regex.sub(' ', str).lower()
    tuples = self.__generate_tuple_keys(clean_str.split())
    for t in tuples:
      self.dict[t[0]].append(t[1])

  def __generate_tuple_keys(self, data):
    if len(data) < self.keywords:
      return

    for i in xrange(len(data) - self.keywords):
      yield [ tuple(data[i:i+self.keywords]), data[i+self.keywords] ]

  """
  " Generates text based on the data the Markov Chain contains
  " max_length is the maximum number of words to generate
  """
  def generate_text(self, max_length=20):
    context = deque()
    output = []
    if len(self.dict) > 0:
      self.__seed_me(rand_seed=len(self.dict))

      idx = random.randint(0, len(self.dict)-1)
      chain_head = list(self.dict.keys()[idx])
      context.extend(chain_head)

      while len(output) < (max_length - self.keywords):
        next_choices = self.dict[tuple(context)]
        if len(next_choices) > 0:
          next_word = random.choice(next_choices)
          context.append(next_word)
          output.append(context.popleft())
        else:
          break
      output.extend(list(context))
    return output