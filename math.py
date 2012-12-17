import web
from web import form
from random import randint

render = web.template.render('templates/')

urls = ('/', 'index',)

#app = web.application(urls, globals())

additionForm = form.Form( 
	form.Textbox("thesum"),
	form.Hidden(name="num1"),
	form.Hidden(name="num2"),
	validators = [
		form.Validator("That's not the right answer", lambda i: int(i.thesum) == int(i.num1) + int(i.num2))
		]
	)

class index:
	def GET(self):
		form = additionForm()
		num1 = randint(1,20)
		form.get('num1').value = num1
		num2 = randint(1,20)
		form.get('num2').value = num2
		return render.index(form, num1, num2)
	def POST(self):
		form = additionForm()
		if not form.validates():
			return render.index(form, form.get('num1').value, form.get('num2').value)
		return render.result() 

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
