#!/home/jrenaut/math.complainthub.com/math/bin/python
import web
from web import form
from random import randint

web.config.debug = False



urls = ('/', 'index',
	'/subtract', 'subtraction',
	'/add', 'addition',
	'/multiply', 'multiplication',
	'/gameover', 'gameover',
	)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'num_right': 0})
render = web.template.render('templates/', globals={'context': session})	

additionForm = form.Form( 
	form.Textbox("thesum"),
	form.Hidden(name="num1"),
	form.Hidden(name="num2"),
	validators = [
		form.Validator("That's not the right answer", lambda i: int(i.thesum) == int(i.num1) + int(i.num2))
		]
	)
	
subtractionForm = form.Form( 
	form.Textbox("thediff"),
	form.Hidden(name="num1"),
	form.Hidden(name="num2"),
	validators = [
		form.Validator("That's not the right answer", lambda i: int(i.thediff) == int(i.num1) - int(i.num2))
		]
	)

multiplicationForm = form.Form( 
	form.Textbox("theproduct"),
	form.Hidden(name="num1"),
	form.Hidden(name="num2"),
	validators = [
		form.Validator("That's not the right answer", lambda i: int(i.theproduct) == int(i.num1) * int(i.num2))
		]
	)

class index:
	def GET(self):
		form = additionForm()
		num1 = randint(1,20)
		form.get('num1').value = num1
		num2 = randint(1,20)
		form.get('num2').value = num2
		return render.index(render.addition(form, form.get('num1').value, form.get('num2').value, "add"))
	def POST(self):
		return "None"

class subtraction:
	def GET(self):
		form = subtractionForm()
		num1 = randint(1,20)
		form.get('num1').value = num1
		num2 = randint(1,20)
		form.get('num2').value = num2
		return render.subtraction(form, num1, num2, "subtract")
	def POST(self):
		form = subtractionForm()
		if not form.validates():
			raise web.seeother('/gameover')
		if 'num_right' not in session:
			session.num_right = 1
		else:
			session.num_right += 1
		return render.index(render.result()) 
		
class addition:
	def GET(self):
		form = additionForm()
		num1 = randint(1,20)
		form.get('num1').value = num1
		num2 = randint(1,20)
		form.get('num2').value = num2
		return render.addition(form, num1, num2, "add")
	def POST(self):
		form = additionForm()
		if not form.validates():
			raise web.seeother('/gameover')
		if 'num_right' not in session:
			session.num_right = 1
		else:
			session.num_right += 1
		return render.index(render.result()) 

class multiplication:
	def GET(self):
		form = multiplicationForm()
		num1 = randint(1,20)
		form.get('num1').value = num1
		num2 = randint(1,20)
		form.get('num2').value = num2
		return render.multiplication(form, num1, num2, "multiply")
	def POST(self):
		form = multiplicationForm()
		if not form.validates():
			raise web.seeother('/gameover')
		if 'num_right' not in session:
			session.num_right = 1
		else:
			session.num_right += 1
		return render.index(render.result()) 

class gameover:
	def GET(self):
		score = session.num_right or 0
		session.num_right = 0
		return render.index(render.gameover(score))
		
if __name__ == "__main__":
    app.run() #this is normally only called from dispatch.cgi
else:
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
