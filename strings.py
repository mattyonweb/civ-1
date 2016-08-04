def religion_resume(self, religion, gods):
		if religion == "Ateismo":
			s = random.choice([
			"Non vi è una religione diffusa, in generale vi è disinteresse nei confronti dell'ultraterreno.",
			"La popolazione è prevalentemente atea, priva di interesse nei confronti dell'aldilà."
			"Dio, o gli dei, non ricadono negli interessi della popolazione." ])

		elif religion == "Agnosticismo":
			s = random.choice([
			"La popolazione non sa se credere o no in qualche Dio, rifugiandosi nell'esercizio del dubbio."])

		elif religion == "Animismo":
			s = random.choice([
			"Sebbene non esista un Dio di riferimento, la maggior parte delle persone crede nell'esistenza di una forza vitale all'interno di tutte le cose.",
			"Un pneuma, secondo i locali, esiste in tutti gli oggetti, gli animali e le persone, anche se la natura di questo soffio non trascende la natura stessa."])

		elif religion == "Deismo":
			if len(gods) > 1:
				s = random.choice([
				"Secondo la popolazione, esistono divinità creatrici di tutte le cose, che però non toccano gli uomini e non li influenzano.",
				"La gente generalmente riconosce l'esistenza di Dei, ma senza lasciarsi influenzare troppo dalla loro presenza.",
				"La loro religione stabilisce l'esistenza di alcuni principii primi, che tuttavia non modificano il corso della storia umana."])
				s += "Gli dei in questione sono: " + ",".join(gods)
			else:
				s = random.choice([
				"Secondo la popolazione, esiste una divinità creatrice di tutte le cose, che però non tocca gli uomini e non li influenza.",
				"La gente generalmente riconosce l'esistenza di Dio, ma senza lasciarsi influenzare troppo dalla sua presenza.",
				"La loro religione stabilisce l'esistenza di un principio primo, che tuttavia non modifica il corso della storia umana."])
				s += "Il dio in questione è " + gods[0]

		elif religion == "Monoteismo":
			s = random.choice([
				"La gente adora e venera un solo dio: ",
				"La religione è pratica diffusa presso questa civiltà, in particolare per quanto riguarda il Dio ",
				])
			s += gods[0]

		elif religion == "Enoteismo":
			s = random.choice([
			"Sebbene il Pantheon indichi la presenza di diverse divinità, una in particolare viene lodata e adorata:",
			"Ufficialmente di religione politeista, questo popolo concentra le proprie preghiere soprattutto su "])
			s += gods[0]
			s += ". Gli altri dei sono: " + ",".join(gods[1:])

		elif religion == "Politeismo":
			s = random.choice([
			"La religione è tipicamente politeista. Gli dei sono: ",
			"La gente del posto adora più di un dio: "])
			s += ",".join(gods)

		return s
