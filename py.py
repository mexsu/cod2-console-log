#!/usr/bin/env python3
import time
import os
import threading
import codecs
from datetime import datetime

def follow(thefile):
	thefile.seek(0,2)
	while True:
		line = thefile.readline()
		if not line:
			time.sleep(0.1)
			continue
		yield line


def addSlashToColorNames(theName):
	slash=0
	for i,c in enumerate(theName):
		if c == '^':
		    theName = theName[:i+slash] + '\\'+ theName[i+slash:]
		    slash+=1
		if c == ';': #if name contains ';' it could be trying to exploit the server say name;rcon pass
		    break
	theName = theName.replace('\n', '').replace('\r', '')
	return theName

def playerJoined(theLine):
	#print(theLine)
	if len(theLine)>=4:
		colorName=addSlashToColorNames(theLine[3])
		osTemp = 'screen -S cod2 -p 0 -X stuff \"wait 350;say \^2Welcome to the Server \^7'+ colorName +' \^1|\^3Have fun\^1!^m\"'
		os.system(osTemp)

def playerLeft(theLine):
	#print(theLine)
	if len(theLine)>=4:
		colorName=addSlashToColorNames(theLine[3])
		osTemp = 'screen -S cod2 -p 0 -X stuff \"wait 350;say \^7'+ colorName +' \^5~ \^1Disconnected\^3||^m\"'
		os.system(osTemp)

def getKillHead(theLine):
	if len(theLine)>=13:
		colorNameKiller=addSlashToColorNames(theLine[8])
		colorNamedied=addSlashToColorNames(theLine[4])
		if theLine[11] == "MOD_HEAD_SHOT" and theLine[12] == "head":
			osTemp = 'screen -S cod2 -p 0 -X stuff \"say '+ colorNameKiller + ' \^2[\^1HeadShot\^2]\^7 ' + colorNamedied +'^m\"'
			os.system(osTemp)


def resCommand(theLine):
	if len(theLine)>=5:
		sayNames = theLine[3]
		fullSay = ''.join(theLine[4:]).lower().strip()
		if fullSay[:1] == u"\x15":
			fullSay = fullSay[1:].strip() #remove weird character "NAK" when say from (T)
		if fullSay == '!cmdlist' or fullSay == '!cmd' or fullSay == '!help':
			osTemp = 'screen -S cod2 -p 0 -X stuff "wait 20;say \^1Commands\^2:\^3!time \^1- \^3!date \^1- \^3!report^m"'
			os.system(osTemp)
		elif fullSay == '!time' or fullSay=='!date':
			osTemp = 'screen -S cod2 -p 0 -X stuff \"wait 20;say \^1Time\^2:\^3'+ datetime.now().strftime('%Y-%m-%d \^1-\^3 %H:%M:%S') +'^m\"'
			os.system(osTemp)
		elif fullSay.startswith("!report"):
			if fullSay.startswith("!report "):
			    f = open("reportLog.txt","a+")
			    f.write(sayNames+":|"+fullSay[8:]+"|:"+ datetime.now().strftime('%Y-%m-%d-%H:%M:%S')+ "\n")
			    f.close()
			    osTemp = 'screen -S cod2 -p 0 -X stuff \"wait 10;say \^3Message successfully \^2sent^m\"'
			    os.system(osTemp)
			else:
			    osTemp = 'screen -S cod2 -p 0 -X stuff \"wait 10;say \^1You have to add message example\^2:\^3!report sky hacks ^m\"'
			    os.system(osTemp)
	

def repeatMess():
	threading.Timer(240, repeatMess).start()
	osTemp = 'screen -S cod2 -p 0 -X stuff "say \^1type \^3!cmd \^1to get all Commands^m"'
	os.system(osTemp)
	time.sleep(90)
	osTemp = 'screen -S cod2 -p 0 -X stuff "say \^5~\^1Have \^2fun \^3:)^m"'
	os.system(osTemp)
	time.sleep(90)
	osTemp = 'screen -S cod2 -p 0 -X stuff "say \^5~\^1Report message to the admin by typing\^2:\^3!report message^m"'
	os.system(osTemp)

if __name__ == '__main__':
	logfile = codecs.open("/home/user/.callofduty2/mods/yes_cod2/server.log","r",encoding='utf-8', errors='ignore')
	loglines = follow(logfile)
	threading.Thread(target=repeatMess).start()
	for line in loglines:
		print(line,end='')
		line = line.strip() #remove time
		line = line.split(" ",1) #remove time
		line = ''.join(line[1:]).strip() #remove time
		if line:
			if line[0] == "J":
				line = line.split(";",3)
				playerJoined(line)
			elif line[0] == "Q":
				line = line.split(";",3)
				playerLeft(line)
			elif line[0]== "s" and line[3]== ';': #only say not sayteam
				line = line.split(";",4)
				resCommand(line)
			elif line[0] == "K":
				line = line.split(";")
				getKillHead(line)

