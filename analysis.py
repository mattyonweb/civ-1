import re, random
from math import *

VOWELS = "aeiou"
punctuation = ",.;:!? "
letters = "bcdfghjklmnpqrstvwxyzaeiou"

def count_vowels(s):
	''' Conta le vocali in una parola '''
	if s == "":
		return 0
	else:
		if s[0] in VOWELS:
			return 1 + count_vowels(s[1:])
		else:
			return count_vowels(s[1:])

def avg_vowels_per_word(s):
	vowels = sum(count_vowels(word) for word in s.split())
	return vowels / len(s.split())

def avg_consecutive_consonants(s):
	''' Ritorna la lunghezza media di consonanti consecutive in una parola '''
	con = re.findall(r'[bcdfghjklmnpqrstvwxyz]+', s, re.IGNORECASE)
	try:
		return sum(len(el) for el in con) / len(con)
	except:
		return 100

def avg_length_words(s):
	chars = sum(len(word) for word in s.split())
	return chars / len(s.split())

def strip_string(s):
	new_s = ""
	for char in s:
		if char not in punctuation:
			new_s += char

	return new_s

def varianza(s_):
	probs = {}
	
	s = strip_string(s_)
	for char in s:
		avg = s.count(char) / len(s)
		probs[char] = avg

	return sqrt(sum((probs[key]-1/26)**2 for key in probs) / 25)
	

def text(s, verbose=False):
	print("vocali per parola:", avg_vowels_per_word(s))
	print("numero di consonanti consecutive:", avg_consecutive_consonants(s))
	print("lunghezza media parole:", avg_length_words(s))
	print("varianza:", varianza(s))

def _evaluate_word(w):
	''' Solo debug '''
	print(w, "len:", len(w))
	print("VOW:",count_vowels(w))
	print("CONS CONS", avg_consecutive_consonants(w))

def bell_curve(x, a, b, c):
	''' a è l'alteza all'apice della curva.
	b è l'ascissa dell'apice della curva.
	c è la deviazione, più è grande più è larga la campana '''
	return a*e**((-(x-b)**2)/2*c**2)

def random_gauss(a, b, c):
	while True:
		x = random.randint(1,10)
		prob = bell_curve(x, a, b, c)
		if random.random() <= prob:
			return x
		
