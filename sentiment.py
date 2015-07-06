import sys,json,requests,re

#Delimiter To use
delimiter='--*--'

#File Name to store generated report
f1 = open('report.html','w')

#data file
fname='samplefeedback.txt'
feedback=[]

f = open(fname,'r')
for line in f.read().strip().split(delimiter):
	feedback.append(line)

f.close()
#Parallelized API Query
def processInput(text):  
	headers = {'X-Mashape-Key': 'JQ5t463vmTmsh57Wdk3HSXs5vguSp1nXi6ZjsnGTrxBULcQMUA','Content-Type': 'application/x-www-form-urlencoded','Accept': 'application/json',}
	text = re.sub('[^a-zA-Z0-9 \n\.]', '', text)
	r1 = requests.get('https://twinword-sentiment-analysis.p.mashape.com/analyze/?text='+text, headers=headers)
	resp=r1.text
	data=json.loads(resp)
	data['text']=text
	print text
	return data

from joblib import Parallel, delayed  
import multiprocessing
num_cores = 10
results = Parallel(n_jobs=num_cores)(delayed(processInput)(text) for text in feedback)  
print results
f1.write("<html><head><script type='text/javascript' src='ts/jquery-latest.js'></script><script type='text/javascript' src='ts/jquery.tablesorter.js'></script><script>$(document).ready(function() {  $('#myTable').tablesorter({  });  } );</script> <link rel='stylesheet' href='ts/docs/css/jq.css' type='text/css' media='print, projection, screen' />	<link rel='stylesheet' href='ts/themes/blue/style.css' type='text/css' id='' media='print, projection, screen' /></head><body><h1><b>Feedbacks</b></h1><table id='myTable' class='tablesorter'><thead><tr><th>Type</th><th>Feedback</th><th>Score</th><tbody>")

newlist = sorted(results, key=lambda k: k['score']) 

#Generating the Report
for tup in newlist:
			f1.write("<tr>")
			f1.write("<td>"+tup['type']+"</td>")

			f1.write("<td>"+tup['text']+"</td>")
			f1.write("<td>"+str(tup['score'])+"</td>")

			f1.write("</tr>")
			

f1.write("</tbody></table></body></html>")


f1.close()



