import numpy


# Credits to https://www.upgrad.com/blog/markov-chain-in-python-tutorial/
class MarkovChain:

	def __init__(self, transition_matrix, states):
		self.transition_matrix = numpy.atleast_2d(transition_matrix)
		self.states = states

		self.index_dictionary = {
			self.states[index]: index for index in range(len(self.states))
		}

		self.state_dictionary = {
			index: self.states[index] for index in range(len(self.states))
		}

	def next_state(self, current_state):
		return numpy.random.choice(
			self.states,
			p=self.transition_matrix[self.index_dictionary[current_state], :]
		)

	def generate_states(self, current_state, states_to_generate=10):
		future_states = []
		for i in range(states_to_generate):
			next_state = self.next_state(current_state)
			future_states.append(next_state)
			current_state = next_state

		return future_states
