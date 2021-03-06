from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import h5py
from flask import jsonify
from flask_cors import CORS, cross_origin
from random import randint
from pickle import load
import keras
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from random import randint

# load doc into memory
def load_doc(filename):
	# open the file as read only
	file = open(filename, 'r')
	# read all text
	text = file.read()
	# close the file
	file.close()
	return text

# generate a sequence from a language model
def generate_seq(model, tokenizer, seq_length, seed_text, n_words):
	result = list()
	in_text = seed_text
	# generate a fixed number of words
	for _ in range(n_words):
		# encode the text as integer
		encoded = tokenizer.texts_to_sequences([in_text])[0]
		# truncate sequences to a fixed length
		encoded = pad_sequences([encoded], maxlen=seq_length, truncating='pre')
		# predict probabilities for each word
		yhat = model.predict_classes(encoded, verbose=0.5)
		# map predicted word index to word
		out_word = ''
		for word, index in tokenizer.word_index.items():
			if index == yhat:
				out_word = word
				break
		# append to input
		in_text += ' ' + out_word
		result.append(out_word)
	result = ' '.join(result)
	sentences = result.split('endofsentence')
	filter(None, sentences)
	return sentences[0]

# load cleaned text sequences
in_filename = 'material3.txt'
doc = load_doc(in_filename)
lines = doc.split('\n')
seq_length = len(lines[0].split()) - 1

# load the model
model = load_model('model.h5')

# load the tokenizer
tokenizer = load(open('tokenizer.pkl', 'rb'))


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def generate_seed():
	random_seed = lines[randint(0, len(lines))]
	sentences = random_seed.split('endofsentence')
	filter(None, sentences)
	longest_sentence = max(sentences, key=len)
	words = longest_sentence.split(' ')[:3]
	seed_text = ' '.join(words)
	seed_text = seed_text.strip()
	return seed_text


@app.route('/')
def index():
	return 'hello'

@app.route('/random_text')
def Random_text():
	seed_text = generate_seed()
	print('Using seed:\n', seed_text + '\n')
	# generate new text
	number_of_words = randint(15, 30)
	generated = seed_text + ' ' + generate_seq(model, tokenizer, seq_length, seed_text, number_of_words)
	print('Generated text:\n', generated)
	capitalized = generated.capitalize().replace(' i ', ' I ').replace(' i.', ' I.')
	capitalized = capitalized.strip()
	result = {'data': capitalized + '.'}
	return jsonify(result)


if __name__ == "__main__":
	app.run()
