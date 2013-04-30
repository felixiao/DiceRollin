var numDices=new Array();
var results=new Array();
var anlysisRes=new Array();

function Dice(face)
{
	this.face=face;
	this.rollRes=parseInt(Math.random()*this.face)+1;
}
function calc()
{
	numDices=new Array();
	results=new Array();
	anlysisRes=new Array();
	var inpDice=String(document.getElementById("fn").value);
	var dices=inpDice.split("+");
	for(var i=0;i<dices.length;i++)
	{
		var num=Number(dices[i].split("d")[0]);
		var face=Number(dices[i].split("d")[1]);
		for(var j=0;j<num;j++)
		{
			numDices.push(new Dice(face));
		}
	}
	getResult(0,0);
	document.getElementById("result").innerHTML=showResult();
}

function getResult(index,res)
{
	for(var i=1;i<numDices[index].face+1;i++)
	{
		if(index<numDices.length-1)
		{
			getResult(index+1,res+i);
		}
		else if(index==numDices.length-1)
		{
			results.push(res+i);
		}
	}
}
function showResult()
{
	var display="Result:</br>";
	var sum=0;
	for(var i=0;i<numDices.length;i++)
	{
		display+="d["+(i+1)+"] f["+numDices[i].face+"]:"+numDices[i].rollRes+"</br>";
		sum+=numDices[i].rollRes;
	}
	display+="Sum="+sum+" Pobability:";
	return display;
}