#!/usr/bin/python3

from flask import Flask, render_template, request
import os

DEBUG = True
DIR_PATH = '.'

app = Flask(__name__, static_folder='static')

someList=[]

@app.route('/')
def index():
	global someList

	path = request.args.get('path', '')
	d_prntnl(path)
	if(path == ''):
		return render_template('files.html',myList=someList)
	return render_template('files.html',myList=dirProbe(path))

@app.route('/viewer')
def viewer():
	global someList

	vid = request.args.get('vid', '')
	link = {'vid':vid}
	title = os.path.basename(vid)
	year = ''
	des = ''
	
	if( os.path.isfile( os.path.dirname(vid)+'/details.hmsx' ) == True):
		allDetails = open(os.path.dirname(vid)+'/details.hmsx').read()
		year = unTag('YEAR_TAG', allDetails)
		if(year==-1):
			year = ''
		des = unTag('DES_TAG', allDetails)
		if(des==-1):
			des = ''
		title = unTag('TITLE_TAG', allDetails)
		if(title==-1):
			title = ''
	if(vid != ''):
		return render_template('viewer.html',link=link,year=year,des=des, title=title)
	else:
		return 'No result found'

@app.route('/browser')
def browser():
	global someList

	path = request.args.get('path', '')
	d_prntnl(path)
	if(path == ''):
		return render_template('files.html',myList=someList)
	return render_template('files.html',myList=dirProbe(path))


def dirProbe(path):
	listItems = []
	ListObjs = []

	if(path[0]=='/'):
		path = path[1:]

	listItems = os.listdir(path)
	for item in listItems:
		d_prntnl('----->'+ 'check  '+item)
		#check if file
		if(os.path.isfile(path+'/'+item) == True):
			d_prntnl(item+' is FILE')
			if(item[-4:] == '.mp4' or item[-4:] == '.MP4'):
				entry = {
					'name':item[:-4],
					'link':'viewer?vid='+path+'/'+item,
					'cur':'',
					'vid':'/'+path+'/'+item,
					'ico':'/static/img/video.png',
					'year':'',
					'des':'',
				}
				ListObjs.append(entry)
		elif(os.path.isdir(path+'/'+item) == True):
			d_prntnl(item+' is DIR')
			posterList = [0,'']
			des = [0,'']
			dirList = os.listdir(path+'/'+item)
			for innerItem in dirList:
				d_prntnl('------------------->'+ 'check content  '+innerItem)
				if(os.path.isdir(path+'/'+item+'/'+innerItem) == True):
					d_prntnl('<isdir>')
					continue
				if('poster.jpg' in innerItem  or
						'poster.jpeg' in innerItem  or
						'poster.png' in innerItem):
					d_prntnl('POSTER FOUND')
					posterList = [1,innerItem]
#				if(innerItem == 'details.hmsx'):
#					detailsFile = open(path+'/'+item+'/'+'details.hmsx')
#					allDetails = detailsFile.read()
#					des = [1,unTag('DESCREPTION',allDetails)]
#					d_prntnl(des[1])

			entry = {
				'name':item,
				'link':'browser?path='+path+'/'+item,
				'vid':'',
				'ico':'/static/img/folder.png',
				'des': ''
			}
			if posterList[0] == 1:
				entry['ico'] = path+'/'+item+'/'+posterList[1]
			if(des[0] == 1):
				entry['des'] = des[1]
			d_prntnl(entry)
			ListObjs.append(entry)
			
		else:
			d_prntnl(item+ ' is nither file nor directory')


	d_prntnl(listItems)
	d_prntnl(ListObjs)
	return ListObjs

def d_prntnl(str1):
	global DEBUG
	if DEBUG == True:
		print('[DEBUG] '+str(str1))

def d_prnt(str1,end):
	global DEBUG
	if DEBUG == True:
		print('[DEBUG] '+str(str1),end=end)
def unTag(tag, str):
	startTag = '['+tag+']'
	endTag = '[/'+tag+']'
	
	start = str.find(startTag)+len(startTag)
	end = str.find(endTag)
	if(start==-1 or end==-1):
		return -1
	return str[start:end]


if __name__ == '__main__':
#   global someList

   someList = dirProbe('static/media')
   app.run('0.0.0.0',5000)
