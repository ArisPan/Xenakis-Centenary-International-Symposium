from numpy.random import default_rng
from numpy import ones
import markov_chain
import sys

TRACKS = [
	'Beesting.wav',
	'Glitch_one.wav',
	'Glitch_two.wav',
	'Glitchbass_one.wav',
	'Glitchbass_two.wav',
	'Hightone.wav',
	'Miles.wav',
	'Moog.wav',
	'Stargate.wav',
	'Subwave.wav'
]

LENGTH = [
	'1',
	'2',
	'3'
]


def generate_transition_matrix(matrix_order):
	rng = default_rng()
	transition_matrix = []

	for i in range(matrix_order):
		probability_vector = rng.dirichlet(ones(matrix_order), size=1)
		transition_matrix.append(probability_vector.tolist()[0])

	return transition_matrix


def generate_prediction_chain(number_of_states, list):
	transition_matrix = generate_transition_matrix(len(list))
	track_chain = markov_chain.MarkovChain(
		transition_matrix=transition_matrix,
		states=list
	)

	prediction = track_chain.generate_states(
		current_state=list[0],
		states_to_generate=number_of_states
	)

	# for probability_vector in transition_matrix:
	# 	print(probability_vector)

	return prediction


def main():
	args = sys.argv[1:]

	if not args:
		print("[Error] Please, specify the number of iterations.")
		sys.exit()

	track_chain = generate_prediction_chain(int(args[0]), TRACKS)
	length_chain = generate_prediction_chain(int(args[0]), LENGTH)

	print("\n*****TRACK CHAIN*****")
	for i in range(len(track_chain)):
		print(length_chain[i] + ' ' + track_chain[i])


if __name__ == '__main__':
	main()
