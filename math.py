import web
from web import form
from random import randint
import shelve
import bisect

web.config.debug = False



urls = ('/', 'index',
	'/subtract', 'subtraction',
	'/add', 'addition',
	'/multiply', 'multiplication',
	'/highscores', 'highscore',
	'/newhighscore', 'add_new_score',
	'/showscores', 'show_scores',)

'''app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})
render = web.template.render('templates/', globals={'context': session})
'''

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

addScoreForm = form.Form(
	form.Textbox("Initials"),
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
			raise web.seeother('/highscores')
			#return render.index(render.subtraction(form, form.get('num1').value, form.get('num2').value, "subtract"))
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
			raise web.seeother('/highscores')
			#return render.index(render.addition(form, form.get('num1').value, form.get('num2').value, "add"))
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
			raise web.seeother('/highscores')
			#return render.index(render.multiplication(form, form.get('num1').value, form.get('num2').value, "multiply"))
		if 'num_right' not in session:
			session.num_right = 1
		else:
			session.num_right += 1
		return render.index(render.result()) 

class highscore:
	def GET(self):
		score = session.num_right or 0
		d = shelve.open('high_score.db')
		try:
			data = d['scores']
		except:
			d['scores'] = [('AAA', 0),('BBB', 0),('CCC', 0),('DDD', 0),('EEE', 0),('FFF', 0),('GGG', 0),('HHH', 0),('III', 0),('JJJ', 0)]
			data = d['scores']			
		data.sort(key=lambda r:r[1])
		x = check_score(data, 'xxx', score)
		print "score is: " + str(score)
		print "X is: " + str(x)
		if x <= 9:
			raise web.seeother('/newhighscore')
		d.close()
		return render.high_scores(data)

class add_new_score:
	def GET(self):
		form = addScoreForm()
		return render.index(render.add_new_score(form))
	def POST(self):
		form = addScoreForm()
		if not form.validates():
			return render.index(render.add_new_score(form))
		d = shelve.open('high_score.db')
		data = d['scores']
		data.sort(key=lambda r:r[1])
		x = check_score(data, (form.get('Initials'), session.num_right))
		add_score(data, (form.get('Initials'), session.num_right), x)
		session.num_right = 0
		d.close()
		raise web.seeother('/show_scores')

class show_scores:
	def GET(self):
		d = shelve.open('high_score.db')
		try:
			data = d['scores']
			return render.index(render.show_scores(data))
		except:
			raise web.seeother('/')
		

def check_score(a, x, lo=0, hi=None):
	if lo < 0:
		raise ValueError('lo must be non-negative')
	if hi is None:
		hi = len(a)
	while lo < hi:
		mid = (lo+hi)//2
		if a[mid][1] < x[1]: lo = mid+1
		else: hi = mid
	return lo

def add_score(a, x, lo):
	a.insert(lo, x)
	print lo
	if len(a) > 10:
		a.pop()
		
if __name__ == "__main__":
	app = web.application(urls, globals())
	session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'num_right': 0})
	render = web.template.render('templates/', globals={'context': session})	
	app.run()
