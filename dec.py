import numpy as np
import codecs
import sys
import os
import json
from ast import literal_eval as le

def fullpath(file):
	path = os.path.join(os.getcwd(),file)
	return path

#global variables Section

data = json.load(open(fullpath('data.json')))
matrix = data['key']
defaultDecFile = data['defaultDecFile']
mod = data['mod']


#####################
#functions Section


def write2file(path,cipher):
	file = open(path,'w',encoding='utf-8')
	file.write(''.join(map(str,cipher)))
	file.close()


def file2list(file):
	f = open(file,'r',encoding='utf-8')
	l=[]
	result = []
	for c in f.read():
		l.append(c)

	step = 0
	for cursor in range(0,len(l)):

		if step != 0:
			step-=1
			continue
		
		if l[cursor] == '\\':
			
			if l[cursor+1] == 'n' or l[cursor+1]=='r' or l[cursor+1] == 't':
				result.append(''.join(map(str,l[cursor:cursor+1])))
				step = 1
				continue

			elif l[cursor+1] == '\\':
				result.append(''.join(map(str,l[cursor:cursor+1])))
				step=1
				continue

			result.append(''.join(map(str,l[cursor:cursor+4])))
			step = 3

		else:
			result.append(l[cursor])
	f.close()
	return result


def text2list(text):
	l=[]
	result = []
	for c in text:
		l.append(c)

	step = 0
	for cursor in range(0,len(l)):

		if step != 0:
			step-=1
			continue
		
		if l[cursor] == '\\':
			
			if l[cursor+1] == 'n' or l[cursor+1]=='r' or l[cursor+1] == 't':
				result.append(''.join(map(str,l[cursor:cursor+1])))
				step = 1
				continue

			elif l[cursor+1] == '\\':
				result.append(''.join(map(str,l[cursor:cursor+1])))
				step=1
				continue

			result.append(''.join(map(str,l[cursor:cursor+4])))
			step = 3


		else:
			result.append(l[cursor])
	return result


def adjoint(matrix):

	minors = {
			'00':'(({0}[2][2]*{0}[1][1]) - ({0}[2][1]*{0}[1][2]))'.format(matrix),
			'01':'(({0}[1][0]*{0}[2][2]) - ({0}[1][2]*{0}[2][0]))'.format(matrix),
			'02':'(({0}[2][1]*{0}[1][0]) - ({0}[2][0]*{0}[1][1]))'.format(matrix),
			'10':'(({0}[2][2]*{0}[0][1]) - ({0}[2][1]*{0}[0][2]))'.format(matrix),
			'11':'(({0}[0][0]*{0}[2][2]) - ({0}[0][2]*{0}[2][0]))'.format(matrix),
			'12':'(({0}[0][0]*{0}[2][1]) - ({0}[2][0]*{0}[0][1]))'.format(matrix),
			'20':'(({0}[1][2]*{0}[0][1]) - ({0}[1][1]*{0}[0][2]))'.format(matrix),
			'21':'(({0}[1][2]*{0}[0][0]) - ({0}[1][0]*{0}[0][2]))'.format(matrix),
			'22':'(({0}[0][0]*{0}[1][1]) - ({0}[0][1]*{0}[1][0]))'.format(matrix)
		}
	
	newl = []
	counter = 0
	for r in range(len(matrix)):
		vlist = []

		for c in range(len(matrix)):
			min_pls = 1
			if counter%2 == 1:
				min_pls = -1
			index = "{}{}".format(r,c)
			result = eval(minors[index])*(min_pls)
			vlist.append(result)
			counter+=1

		newl.append(vlist)
	return np.transpose(newl)

adj = adjoint(matrix)%mod
det = int(np.linalg.det(matrix))
inv_det = pow(det,-1,mod)

key = (inv_det * adj)%mod



def D(key,cipher):

	planlist = []
	plantext = []
	k_demention = len(key)

	for i in range(0,len(cipher),k_demention):

		group_calc= i+k_demention
		vlist = []
		vlist=cipher[i:group_calc]

		if len(vlist)<k_demention:
			for reminder in range(len(vlist),k_demention):
				vlist.append('\0')

		for column in range(k_demention):
			echar = 0

			for row in range(k_demention):
				vchar = vlist[row]
			
				if len(vchar) > 1:
					echar += ord(codecs.decode(vchar,'unicode_escape'))*key[row][column]
				else:
					echar += ord(vchar)*key[row][column]

			plantext.append(chr(echar%mod))
	for i in range(3):
		cursor = i-3
		s= repr(plantext[cursor])

		if s.replace("'",'').startswith('\\'):
			plantext.pop(cursor)
		cursor-+i

	return plantext


##########################
##cli ArgvControl Section

typeInput = False
typeFile = False

argvlist = list(sys.argv)

if len(argvlist) >= 2:

	for i in range(1,len(argvlist)):
		if argvlist[i] == '-t':
			text = list(str(input(">> ")))
			try:
				if argvlist[i+1] == '-path':
					pathTo = argvlist[i+2]
					print("writing To File [{}]".format(pathTo))
			except (IndexError,FileNotFoundError):
				print("destination file not specified ,writing result to default file [{}]".format(defaultDecFile))
				pathTo =fullpath(defaultDecFile)
			typeInput = True
			break

		if argvlist[i] == '-f':

			try:
				pathFrom = argvlist[i+1]
				text = file2list(pathFrom)
			except (IndexError,FileNotFoundError):
				print("valid source file required !\nexit() ...")
				sys.exit()

			try:
				if argvlist[i+2] == '-path':
					pathTo = argvlist[i+3]
					print("write result to File [{}]".format(pathTo))
			except (IndexError,FileNotFoundError):
				print("destination file not specified ,writing result to default file [{}]".format(defaultDecFile))
				pathTo = fullpath(defaultDecFile)
			
			typeFile = True
			break

		else:
			print("invalid argument ..")
			sys.exit()



###################
#Execution Section

if typeFile:

	try:
		write2file(pathTo,D(key,text))
	except TypeError:
		print('the file specified is decrypted indeed !')

if typeInput:
	try:
		write2file(pathTo,D(key,text2list(text)))
	except TypeError:
		print('the file specified is decrypted indeed !')