import wsgiref.handlers
from random import randint
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render('index.html',{}))

class Calc(webapp.RequestHandler):
	def post(self):
		self.response.out.write("""
<html>
<Head>
	<link rel="stylesheet" type="text/css" href="mystyle.css" />
	<script src="calc.js" language="javascript"></script>
	<h1>Rolling Dices </h1>
</Head>
<body>
	Please enter dices:
	<form action="/calc" method="post">
		""")
		self.response.out.write('<div><input name="inpu" type="text" value="'+self.request.get('inpu')+'"/></div>')
		self.response.out.write("""
		<div><input type="submit" value="Roll"></div>
	</form>
	<p id="result">Result:</p>""")
		
		self.response.out.write(calc(self.request.get('inpu')))
		self.response.out.write("""
</body>
</html>""")

app = webapp.WSGIApplication([('/', MainPage),('/calc',Calc)],debug=True)

dices=[]
res=[]


def calc(t):
	global dices
	dices=[]
	global res
	res=[]
	totalP = 1
	di=t.split('+')
	maxVal = 0
	for i in range(0,len(di)):
		d = di[i].split('d')
		count=int(d[0])
		for j in range(0,count):
			fa=int(d[1])
			dices.append(fa)
			maxVal += fa
			totalP *= fa
			roll(fa)
	minVal = len(dices)
	output ='['+str(minVal)+'] 1/'+str(totalP)+'</br>'
	for k in range(minVal+1,maxVal):
		output +='['+str(k)+'] '+ str(probability(k,0))+'/'+str(totalP)+'</br>'
	output +='['+str(maxVal)+'] 1/'+str(totalP)+'</br>'
	summary=[]
	for p in range(0,20):
		sum=0
		for q in range(0,len(res)):
			output+='['+str(dices[q])+']:'+str(res[q])+', '
			sum+=res[q]
		output+=' Sum='+str(sum)+'</br>'
		summary.append(sum)
		getResult()
	for q in range(minVal+1,maxVal):
		if summary.count(q)!=0:
			output+='Sum='+str(q)+' Freq='+str(summary.count(q))+'/20</br>'
		
	return output
	
def getResult():
	global res
	res=[]
	for i in dices:
		roll(i)
		
def roll(face):
	global res
	res.append(randint(1,face))
	
def prob(x,y,r):
	if x+y<r:
		return 0
	elif x+y==r:
		return 1
	elif r<2:
		return 0
	elif x<r and y>r-2:
		return x
	elif x>r-2 and y<r:
		return y
	elif x>r-2 and y>r-2:
		return r-1
	else:
		return x+y+1-r

def probability(r,index):
	if index==len(dices)-2:
		return prob(dices[index],dices[-1],r)
	else:
		p=0
		for i in range(0,dices[index]):
			if r-i-1<=0:
				continue
			p+=probability(r-i-1,index+1)
		return p
			
def main():
  run_wsgi_app(app)

if __name__ == "__main__":
  main()