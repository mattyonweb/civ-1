import math, random

def bell_curve(x, a, b, c):
	return a*math.e**((-(x-b)**2)/2*c**2)

def random_montecarlo_bell(a, b, c):
	while True:
		r = random.random()
		if r >= bell_curve(random.random(), a, b, c):
			return r

def maprange(s,a1,a2,b1,b2):
	return b1+(((s-a1)*(b2-b1))/(a2-a1))

def noise_rescale(val):
	''' Porta il noise da [-1,1] a [0,1]'''
	return 0.5 + val/2

def distance(x1, x2, y1, y2):
	return math.sqrt( (x2-x1)**2 + (y2-y1)**2)

def avg_map(mappa):
	''' Ritorna la media dei valori di una matrix '''
	all_vals = (mappa[y][x] for y in range(len(mappa)) for x in range(len(mappa[1])))
	return sum(all_vals)/(len(mappa)*len(mappa[1]))

def blend_colors(c1, c2):
	''' Missa due colori. '''
	f = lambda x,y: int(255-(( (255-x)**2 + (255-y)**2)/2)**0.5)
	#f = lambda x,y: min(x+y,255)
	new_r = f(c1[0],c2[0])
	new_g = f(c1[1],c2[1])
	new_b = f(c1[2],c2[2])
	return (new_r, new_g, new_b)

def sigmoid_func(x, slope=0.1):
	return 1 / (0.5 + math.e**((-(x - 0.35)) / slope))
