import math, random, os, shutil

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
	return (x2-x1)**2 + (y2-y1)**2

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

def sq_distance(x0, y0, xf, yf):
	return (xf-x0)**2 + (yf-y0)**2

def find_path(matrix, x0, y0, xf, yf, sea_level, mount_level):
	''' Questo dovrebbe essere un algoritmo A*? '''
	neigh_vectors = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
	
	new_matrix = [[0 for x in range(len(matrix[0]))] for y in range(len(matrix))]

	open_dict = { (x0,y0): 0 }
	closed_list = set()

	while len(open_dict) != 0:
		#prendo le coordinate del valore più piccolo di f in open_dict
		curr_x, curr_y = min(open_dict, key=open_dict.get)
		del open_dict[(curr_x, curr_y)]

		#print(curr_x,curr_y)
		for vector in neigh_vectors:
			#coordinate del vicino di curr
			new_x, new_y = curr_x + vector[0], curr_y + vector[1]
			
			#assicurarsi che il vicino non sia fuori dalla matrix
			try:
				matrix[new_y][new_x]
			except:
				continue
			
			g = 1.4 if vector[0] == vector[1] else 1
			e = (1 + (matrix[new_y][new_x] - matrix[curr_y][curr_x])/2)
			
			#se il vicino è già stato esaminato in precedenza, ignoralo
			if (new_x, new_y) in closed_list:
				continue
			elif matrix[new_y][new_x] < sea_level or matrix[new_y][new_x] > mount_level: #ostacolo
				continue
			elif new_y < 0 or new_x < 0:
				continue

			#se si è raggiunti il punto d'arrivo
			if (new_x, new_y) == (xf, yf):
				new_matrix[yf][xf] = (curr_x, curr_y)
				return path_coordinates(new_matrix, xf, yf, x0, y0)

			#se il vicino non era mai stato raggiunto prima, salvalo
			if (new_x, new_y) not in open_dict.keys():
				open_dict[(new_x, new_y)] = g + sq_distance(new_x, new_y, xf, yf)*e
				new_matrix[new_y][new_x] = (curr_x, curr_y)
				
			else:
				new_f = g + sq_distance(new_x, new_y, xf, yf)*e
				curr_f = open_dict[(new_x, new_y)]
				if new_f < curr_f:
					open_dict[(new_x, new_y)] = new_f
					new_matrix[new_y][new_x] = (curr_x, curr_y)
					
		closed_list.add((curr_x, curr_y))
		
	else:
		print("Non si è trovata una strada. Messaggio da utils/find_path")
		return None


def path_coordinates(matrix, xf, yf, x0, y0):
	path = [(xf,yf)]
	x_, y_ = xf, yf
	while (x_, y_) != (x0, y0):
		path.append(matrix[y_][x_])
		try:
			x_, y_ = matrix[y_][x_]
		except:
			return path
	return path

def remove_dir_content(relative_path="./civs"):
	shutil.rmtree(relative_path)
	os.makedirs(relative_path)
