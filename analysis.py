import re, random
from math import *

punctuation = ",.;:!? "

def strip_string(s):
	new_s = ""
	for char in s:
		if char not in punctuation:
			new_s += char

	return new_s

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
		
