import web
from web import form
from random import randint

render = web.template.render('templates/')

urls = ('/', 'index',
	'/subtract', 'subtraction',
	'/add', 'addition',
	'/multiply', 'multiplication',)


#app = web.application(urls, globals())

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
		return render.index(form, num1, num2, "add")
	def POST(self):
		form = additionForm()
		if not form.validates():
			return render.index(form, form.get('num1').value, form.get('num2').value, "add")
		return render.result() 

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
			return render.index(form, form.get('num1').value, form.get('num2').value, "subtract")
		return render.result() 
		
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
			return render.index(form, form.get('num1').value, form.get('num2').value, "add")
		return render.result() 

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
			return render.index(form, form.get('num1').value, form.get('num2').value, "multiply")
		return render.result() 

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
