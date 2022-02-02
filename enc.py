import sys
import os
import json
import codecs



def fullpath(file):
	full = os.path.join(os.getcwd(),file)
	return full

###################
#global vars

data = json.load(open(fullpath("data.json")))
key = data['key']
defaultEncFile = data['defaultEncFile']
mod = data['mod']

###################
#functions section

def write2file(target,cipher):
	with open(target,'w',encoding='utf-8') as file:
		file.write(''.join(map(str,cipher)))
	


def file2list(file):
	
	file = open(file)

	l=[]
	for char in file.read():
		l.append(char)
	file.close()
	return l

def E(key,plan):
	cipherList = []
	cipherText = []
	k_demention = len(key)

	for i in range(0,len(plan),k_demention):

		group_calc = i + k_demention
		vlist = []
		vlist=plan[i:group_calc]
		if len(vlist)<k_demention:
			for r in range(len(vlist),k_demention):
				vlist.append("\0")
				
		for column in range(k_demention):
			echar = 0
			for row in range(k_demention):
				echar += (ord(vlist[row])*(key[row][column]))%mod
			
			cipherText.append(repr(chr(echar)).replace("'",''))


	return cipherText



#############################
#cli ArgumentControll Section

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
			except (IndexError,FileNotFoundError):
				print("destination file not specified ,writing Result to default file [{}]".format(defaultEncFile))
				pathTo = fullpath(defaultEncFile)
			typeInput = True
			break

		if argvlist[i] == '-f':
			try:
				pathFrom = argvlist[i+1]
				text = file2list(pathFrom)
			except (IndexError,FileNotFoundError):
				print("Please enter a valid File !\nexiting ... ")
				sys.exit()

			try:
				if argvlist[i+2] == '-path':
					pathTo = argvlist[i+3]
			except (IndexError,FileNotFoundError):
				print("destination file not specified ,writing Result to default file [{}]".format(defaultEncFile))
				pathTo = fullpath(defaultEncFile)
			
			typeFile = True
			break
		else:
			print("invalid syntax ..")
			sys.exit()



########################
# execution Section


if typeFile:

	try:
		write2file(pathTo,E(key,text))
	except TypeError:
		print('the file specified is encrypted indeed !')
elif typeInput:

	try:
		print(pathTo)
		write2file(pathTo,E(key,text))
	except TypeError:
		print('the file specified is encrypted indeed !')

 



