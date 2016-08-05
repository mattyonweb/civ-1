import random, analysis
punctuation = ",.;:!?"
#----

class Core:

	def __init__(self):
		consonants = "bcdfghjklmnpqrstvwxyzçæðñþ"
		vowels_and_special = "aeiouøöÿăā"
		self.phonetics = {
			"C" : random.sample(consonants, random.randint(3,11)),
			"R" : random.sample(consonants, random.randint(2,5)),
			"V" : random.sample(vowels_and_special, random.randint(3,7)) }
		self.freq = {}
		self.create_freq()
		self.types = ["CV", "RV", "CRV"]

	def create_freq(self):
		for key in self.phonetics:
			letters = self.phonetics[key]
			
			rand = [random.random() for _ in letters]
			probs = [rand[i] / sum(rand) for i in range(len(letters))]
			self.freq[key] = probs

	def return_freq(self, kind, char):
		''' Siccome la sintassi dei dizionari è orribile...
		kind è il tipo di sillaba (CRMV), char è il char '''
		idx_char = self.phonetics[kind].index(char)
		return self.freq[kind][idx_char]

	def generate_word(self):
		w = ""
		
		for syllabus in range(analysis.random_gauss(1, self.avg_syllabus, self.length_strictness)):
			syl_type = random.choice(self.types)
			for kind in syl_type:
				while True:
					char = random.choice(self.phonetics[kind])
					if random.random() <= self.return_freq(kind,char):
						break
				w += char
		return w

	def generate_text(self, length=100):
		t = ""
		for words in range(length):
			if random.random() < 0.1:
				t += self.generate_word() + random.choice(punctuation) + " "
			else:
				t += self.generate_word() + " "
		return t

#----

class Language(Core):
	def __init__(self):
		self.dropoff = 1
		self.avg_syllabus = 3
		self.length_strictness = 1.3
		Core.__init__(self)
		
	def create_freq(self, mode="cubic"):
		for key in self.phonetics:
			letters = self.phonetics[key] #le lettere di un gruppo fonetico

			if mode == "cubic":
				f = lambda x: -(8.69*(10**-6))*x**3 + 0.000563*x**2 -0.01447*self.dropoff*x + 0.14
			elif mode == "linear":
				f = lambda x: 0.11145 - 0.0058*self.dropoff*x 

			probs = [f(i) for i in range(len(letters))]
			self.freq[key] = probs

	def change_dropoff(self, new_value):
		self.dropoff = new_value
		self.create_freq()

	def print_letter_freq(self):
		for kind in self.phonetics:
			for pair in zip(self.phonetics[kind], self.freq[kind]):
				print(pair)

	def print_stats(self):
		for kind in self.phonetics:
			print(kind, self.phonetics[kind])
		print(" ".join(self.types))
		print("Dropoff:", self.dropoff)
		print("Numero medio di sillabe:", self.avg_syllabus)
		print("Strictness sul numero di sillabe:", self.length_strictness)
		

