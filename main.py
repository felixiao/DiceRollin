import wsgiref.handlers
from random import randint
import webapp2
from google.appengine.ext.webapp import template
import json

calcRes='' 
resultPrb=[]
maxVal=0
class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write(template.render('index.html',{}))
	def post(self):
		global calcRes
		# calcRes=calc(self.request.get('dice'))

		self.response.content_type='text/json'
		responseText=self.request.body
		if responseText==None:
			self.response.body='none'
		elif responseText=='':
			self.response.body='empty'
		else:
			calc(responseText)
			self.response.body=json.dumps(resultPrb,sort_keys=False)


app = webapp2.WSGIApplication([('/', MainPage)],debug=True)

dices=[]
res=[]
calcCount=0

class Dice:
	"""Single Dice"""
	def __init__(self,d):
		self.min=1
		self.max=d
	def getPrb(self,r):
		if self.min<=r<=self.max:
			return 1
		else:
			return 0

class DicePair:
	"""Dice pair"""
	def __init__(self,a,b=None):
		self.diceA=a
		self.diceB=b
		if self.diceB:
			self.min= a.min+b.min
			self.max= a.max+b.max
		else:
			self.min= a.min
			self.max= a.max

	def getPrb(self,r):
		global calcCount
		calcCount+=1
		if self.diceB:
			if self.min> r or self.max < r:
				return 0
			elif self.min == r:
				return self.diceA.getPrb(self.diceA.min)*self.diceB.getPrb(self.diceB.min)
			elif self.max == r:
				return self.diceA.getPrb(self.diceA.max)*self.diceB.getPrb(self.diceB.max)
			else:
				count=0
				max=0
				if r-self.diceB.min>self.diceA.max:
					max=self.diceA.max+1
				else:
					max=r-self.diceB.min+1
				for i in range(self.diceA.min,max):
					count+=self.diceA.getPrb(i)*self.diceB.getPrb(r-i)
				return count
		else:
			if self.diceA.min<=r<=self.diceA.max:
				return 1
			else:
				return 0

def setDicePair(diceList):
	lenght=len(diceList)
	half=lenght/2
	if half>1:
		return DicePair(setDicePair(diceList[0:half]),setDicePair(diceList[half:]))
	elif lenght==1:
		return DicePair(Dice(diceList[0]))
	elif lenght==2:
		return DicePair(Dice(diceList[0]),Dice(diceList[1]))
	else:
		return DicePair(Dice(diceList[0]),DicePair(Dice(diceList[1]),Dice(diceList[2])))


def calc(t):
	global dices
	dices=[]
	
	global calcCount
	calcCount=0
	global maxVal
	totalP = 1
	di=t.split(',')
	maxVal = 0
	for i in di:
		fa=1
		try:
			fa=int(i)
		except ValueError:
			pass
		dices.append(fa)
		maxVal += fa
		totalP *= fa
		

	diceP=setDicePair(dices)
	minVal = len(dices)
	minDice=min()
	#calc probability
	prob=[]
	coun=0
	prob.append(1)
	global resultPrb
	resultPrb=[]
	resultPrb.append([minVal+coun,prob[coun]])
	coun+=1
	#get prob directly
	for s in range(0,minDice-1):
	 	prob.append(product(s,minVal))
	 	resultPrb.append([minVal+coun,prob[coun]])
	 	coun+=1
	#calc rest number till half of maxNum
	for s in range(minVal+minDice, (maxVal+minVal)/2+1):
		prob.append(diceP.getPrb(s))
		resultPrb.append([minVal+coun,prob[coun]])
	 	coun+=1
	#use the prob directly from existed half
	for r in range(0,(maxVal-minVal+1)/2):
		prob.append(prob[(maxVal-minVal-1)/2-r])
		resultPrb.append([minVal+coun,prob[coun]])
	 	coun+=1

def RollingDice(count):
	global res
	global maxVal
	res=[]
	for d in dices:
		roll(d)

	output=''
	summary=[]

	#roll the dices
	for p in range(0,count):
		sum=0
		for q in range(0,len(res)):
			output+='['+str(dices[q])+']:'+str(res[q])+', '
			sum+=res[q]
		output+=' Sum='+str(sum)+'</br>'
		summary.append(sum)
		getResult()
	
	for q in range(len(dices),maxVal+1):
		if summary.count(q)!=0:
			output+='Sum='+str(q)+' Freq='+str(summary.count(q))+'/20</br>'
	return output
	
def product(i,n):
	a = reduce(lambda   x,y:x*y,   range(n,   n+i+1))
	b = reduce(lambda   x,y:x*y,   range(1,   i+2))
	return a/b
	
def min():
	min=dices[0]
	for i in dices:
		if min>i:
			min=i
	return min
	
def getResult():
	global res
	res=[]
	for i in dices:
		roll(i)
		
def roll(face):
	global res
	res.append(randint(1,face))

		
def prob2(x,y,r):
	global calcCount
	calcCount+=1
	if x+y<r or r<2:
		return 0
	elif x+y==r or r==2:
		return 1
	elif x<r and y>r-2:
		return x
	elif x>r-2 and y<r:
		return y
	elif x>r-2 and y>r-2:
		return r-1
	else:
		return x+y+1-r
def main():
  app.RUN()

if __name__ == "__main__":
  main()