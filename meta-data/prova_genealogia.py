import random

nomi_maschili = ["andrea", "giuseppe", "pino", "oscar", "luigi", "teo", "mandragolo", "forest"]
nomi_femminili = ["gianna", "luigia", "alberta", "albertina", "cucciola", "magda", "maddalena", "palazzina"]
cognomi = ["siniscalchi", "calatafimi", "lussemburgo", "de amicis", "pinoccioli", "de luridi", "sigismondi", "ruffini", "ruggeri", "amendola"]


class Persona:
	def __init__(self, parenti):
		self.sex = random.choice(["m","f"])
		self.nome = random.choice(nomi_maschili) if self.sex == "m" else random.choice(nomi_femminili)
		self.cognome = random.choice(cognomi)
		self.eta = random.randint(0,99)

		self.parents = parenti
		self.figli = []
		self.coniuge = None

	def __str__(self):
		return self.nome + " " + self.cognome + " " + str(self.eta)

	def return_parents(self):
		if self.parents:
			return ", ".join(self.parents)
		else:
			return ""

	def return_sons(self):
		if self.figli:
			return ", ".join(self.figli)
		else:
			return ""

	def return_coniuge(self):
		if self.coniuge:
			return str(self.coniuge)
		else:
			return ""


class Genealogia:
	def __init__(self, generations=2):
		self.generations = generations
		self.persone = list()
		self.genera_stato_iniziale()

	def genera_stato_iniziale(self):
		''' Genera la genealogia al momento t=0 '''
		for gen in range(self.generations):

			if gen == 0:
				for _ in range(30):
					self.persone.append(Persona(None))
				
			else:
				num_coppie = random.randint(4, int(len(self.persone)/2 - 2))
				for _ in range(num_coppie):
					genitore1, genitore2 = random.sample(self.persone, 2)

					if not self.are_sposabili(genitore1, genitore2):
						continue

					self.make_coniugi(genitore1, genitore2)
					self.generate_sons(random.randint(0,4), genitore1, genitore2)

	def make_coniugi(self, a, b):
		''' Fa figurare a e b coniugi '''
		a.coniuge = b
		b.coniuge = a

	def generate_sons(self, num, a, b):
		''' Genera *num* figli di a e b '''
		if num == 0:
			return
			
		genitori_couple = [a, b]
		
		for _ in range(num):
			figlio = Persona(genitori_couple)
			
			self.persone.append(figlio)
			a.figli.append(figlio)
			b.figli.append(figlio)

	def are_relatives(self, a, b):
		''' Controlla se a e b sono parenti entro il primo grado '''q	
		if b in a.figli or b in a.parents:
			return True
		if a in b.figli or a in b.parents:
			return True
		if a == b.coniuge:
			return True
		return False

	def are_sposabili(self, a, b):
		''' Controlla se a e b si possono sposare oppure è sconsigliabile '''
		if a.eta < 14 or b.eta < 14:
			return False
		if self.are_relatives(a, b):
			return False
		return True

	def print_tutto(self):
		for persona in self.persone:
			print(persona)
			print("\t" + persona.return_parents())
			print("\t" + persona.return_sons())
			print("\t" + persona.return_coniuge())
		print(len(self.persone))	

g = Genealogia()
g.print_tutto()
