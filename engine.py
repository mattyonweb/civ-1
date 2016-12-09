import random, analysis, itertools
punctuation = ",.;:!?"

class Fonetica:
	''' PER LA FONETICA E LA GENERAZIONE IGNORANTE DI PAROLE '''

	def __init__(self, lingua):
		self.lingua = lingua
		
		consonants = "bcdfghjklmnpqrstvwxyzçñ"
		vowels = "aeiou"
		accented = "àòùèéü"
		specials = "øƧƱŁßƋƑƏƲƸҖѦФЉДðñþæ"
		
		self.phonetics = {
			"C" : random.sample(consonants, random.randint(3,7)),
			"R" : random.sample(consonants, random.randint(2,5)),
			"V" : random.sample(vowels, random.randint(2,5)),
			"A" : random.sample(accented, random.randint(1,4))
			#"S" : random.sample(specials, random.randint(1,3))
			}
			
		self.freq = self.generate_freq()
		
		all_possible_types = []
		for r in range(1, len(list(self.phonetics))+1):
			for el in itertools.combinations(list(self.phonetics.keys()),r):
				all_possible_types.append(el)
		self.types = ["".join(random.choice(all_possible_types)) for _ in range(random.randint(2,5))]

	def generate_freq(self, mode="cubic"):
		''' Per ogni lettera, genera una frequenza che sta a indicare la
		probabilità che quella lettera appaia '''
		frequenze = dict()
		
		for key in self.phonetics:
			letters = self.phonetics[key] #le lettere di un gruppo fonetico

			if mode == "cubic":
				f = lambda x: -(8.69*(10**-6))*x**3 + 0.000563*x**2 -0.01447*self.lingua.dropoff*x + 0.14
			elif mode == "linear":
				f = lambda x: 0.11145 - 0.0058*self.lingua.dropoff*x
			elif mode == "casual":
				f = lambda x: random.random()/10

			probs = [f(i) for i in range(len(letters))]
			frequenze[key] = probs
			
		return frequenze
	
	def return_freq(self, kind, char):
		''' Siccome la sintassi dei dizionari è orribile...
		kind è il tipo di sillaba (CRMV), char è il char '''
		idx_char = self.phonetics[kind].index(char)
		return self.freq[kind][idx_char]
		
	def generate_syllabus(self):
		''' Genera una sola sillaba. '''
		syllabus = ""
		syl_types = list(random.choice(self.types)) #["C", "V"]
		for group in syl_types:
			while True:
				char = random.choice(self.phonetics[group])
				if random.random() <= self.return_freq(group,char):
					break
			syllabus += char
		return syllabus

#----

class Language:
	def __init__(self):
		''' Un dropoff maggiore riduce l'apparizione delle lettere meno
		frequenti. '''
		self.dropoff = random.uniform(0.5,1.5)
		self.avg_num_of_syllabus = random.randint(1,5)
		self.length_strictness = random.uniform(0.8,1.4)

		self.fonetica = Fonetica(self)
		self.grammar = Grammar(self)
		self.nome_lingua = self.generate_word().capitalize()
		self.vocabolario = self.generate_vocabolario()

	def generate_word(self):
		''' Genera una parola di lunghezza pseudo-casuale '''
		w = ""
		n_sillabe = analysis.random_gauss(1, self.avg_num_of_syllabus, self.length_strictness)
		
		for _ in range(n_sillabe):
			w += self.fonetica.generate_syllabus()		
		return w

	def generate_radix_word(self):
		''' Genera una parola-radice, a cui poi attaccare tutti i suffissi '''
		length = random.randint(1,2)
		radix = ""
		for sillabe in range(length):
			radix += self.fonetica.generate_syllabus()
		return radix

	def generate_text(self, word_number=100, punct=False, suspension=False):
		''' Genera un testo di parole insensate '''
		t = ""
		for words in range(word_number):
			if random.random() < 0.1 and punct:
				t += self.generate_word() + random.choice(punctuation) + " "
			else:
				t += self.generate_word() + " "
				
		if suspension:
			t += "[...]"
			
		return t

	def generate_vocabolario(self):
		''' Crea un dizionario parola italiana: radice parola straniera '''
		parole_italiane = ["libro", "casa", "albero", "mare", "cielo",
						   "stella", "montagna", "padre", "madre", "eroe",
						   "figlio", "yeti"]
		return dict(zip(parole_italiane, (self.generate_radix_word() for _ in range(len(parole_italiane)))))
		
	def generate_book_title(self):
		''' Genera un libro del tipo "Il libro del [nome]" '''
		first_word = self.grammar.apply_declension(self.vocabolario["libro"], "nominativo", "singolare")
		second_word = self.grammar.apply_declension(random.choice(list(self.vocabolario.values())), "genitivo", "singolare")
		return first_word.capitalize() + " " + second_word.capitalize()
		
	def return_informations(self):
		s = "Nome linguaggio: " + self.nome_lingua
		s += "\nAlfabeto:"
		for types in self.fonetica.phonetics.keys():
			cazzo = [el for el in self.fonetica.phonetics[types]]
			s += "\n\t" + str(types) + ": " + "".join(cazzo)
		s += "\nNumero di sillabe più probabile per parola: " + str(self.avg_num_of_syllabus)
		s += "\nVocabolario di base:"
		for word in self.vocabolario:
			s += "\n\t" + word.capitalize() + " ----> " + self.vocabolario[word].capitalize()
		s += self.grammar.print_informations()
		return s


class Grammar():
	def __init__(self, lingua):
		self.lingua = lingua
		self.fonetica = self.lingua.fonetica
		
		self.sintassi = random.choice(["SVO", "SOV", "VSO", "VOS", "OSV", "OVS"])
		self.tipologia_linguistica = self.define_tipologia_linguistica()
		self.ruolo_morfema = self.define_ruolo_morfema()
		self.suffix_order, self.case_decl, self.num_decl, self.gen_decl = self.generate_names_declination()
		
	def define_tipologia_linguistica(self):
		if self.lingua.avg_num_of_syllabus == 1:
			return "isolante"
		elif self.lingua.avg_num_of_syllabus <= 3:
			return "sintetica"
		else:
			return "polisintetica"

	def define_ruolo_morfema(self):
		return "Nessun ruolo" if self.tipologia_linguistica=="isolante" else random.choice(["agglutinante","flettiva"])

	def generate_names_declination(self):
		''' Genera l'impianto di declinazioni dei sostantivi '''
		if self.tipologia_linguistica == "isolante":
			return None,None,None,None
			
		casi = ("nominativo", "accusativo", "genitivo", "dativo", "ablativo")
		numero = ("singolare", "plurale", "duale")
		genere = ("maschile", "femminile", "neutro")

		casi_decl = dict(zip(casi, (self.fonetica.generate_syllabus() for _ in casi)))
		num_decl = dict(zip(numero, (self.fonetica.generate_syllabus() for _ in numero)))
		gen_decl = dict(zip(genere, (self.fonetica.generate_syllabus() for _ in genere)))

		order = "".join(random.sample("cng", 3))

		return order, casi_decl, num_decl, gen_decl

	def apply_declension(self, radix, case, number):
		''' Applica una declinazione ad una radice '''
		if self.tipologia_linguistica == "isolante":
			return radix
		radix += self.case_decl[case]
		radix += self.num_decl[number]
		return radix

	def print_informations(self):
		s = "\nSintassi: " + self.sintassi
		return s + "\nTipologia linguistica: lingua " + self.tipologia_linguistica
