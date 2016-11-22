def generate_html():
	''' Genera l'HTML della home page '''
	import civilization
	code = """
	<html>
	<head>
	<meta charset='UTF-8'>
	</head>
	<body> <br>
	"""
	code += "<img src='terrain.jpg' align='right'> <br>"
	code += civilization.Civilta.generate_html_links() #qua ci sono tutti i links
	code += "</body></html>"
	return code

def generate_html_file(code):
	import os
	dire = os.path.dirname(__file__)
	filename = os.path.join(dire, './output/pagina.html')
	output_page = open(filename, "w")
	output_page.write(code)
	output_page.close()

def show_page():
	import webbrowser
	url = "./output/pagina.html"
	webbrowser.open(url,new=2)

def web_wrapper():
	code = generate_html()
	generate_html_file(code)
	show_page()

