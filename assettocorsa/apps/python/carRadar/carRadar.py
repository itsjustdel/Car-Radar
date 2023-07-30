import math
import sys
import os
import subprocess
import time
import platform

import ac
import acsys

import shutil

if platform.architecture()[0] == "64bit":
	sysdir = os.path.dirname(__file__)+'/stdlib64'
else:
	sysdir = os.path.dirname(__file__)+'/stdlib'

sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."

from sidekick_lib.sim_info import info

# import ctypes
# from ctypes import wintypes

######user variables
##below are variables which I decided not to put in to the user controllable menu, but you may want to change them anyway

#change how large the background hex,square or diamond is
backgroundSize = 10
#I let it so even when the cars are fully solid, the background is slightly see through, AC official apps all have a slight transparency to them
#if you want it solid. change to 1, and if you want it more transparent, lower, always keep between 0.0 and 1.0
backgroundMaxOpacity = 0.9

#hide player car always by making False
drawPlayerCar = True
#Force all outlines off
drawOutlineOfCars = True
##force main body of cars off
drawMeshOfCars = True

######end of user variables

playerCarMeshColour = (1,1,1)
playerCarMeshColourIndex = 0
playerCarOutlineColourIndex = 0
otherCarOutlineColourIndex = 0
otherCarMeshColourIndex = 0
otherCarMeshColour = (1,1,1)

playerCarOutlineColour = (0,0,0)
otherCarOutlineColour = (0,0,0)

scale = 10
scaleLimit = 100

carAura = 20
angleOfInfluence = 90
rearCutOffDistance = 10
######
#range animation
raiseCarAura = False
lowerCarAura = False
carAuraTarget = 20#starting same as carAura
raiseRearCutOffDistance = False
lowerRearCutOffDistance = False

appWindow = 0
titleLabel = 0

carList = []
tempCarList = []
carTypes = []
carTypesToConvert = []
carTypesBeingConverted = []
filesToRemove = []

##UI
windowWidth = 200 #clickable area
elapsed = 0
configButton = 0
background = 0
extendConfigButton = False
retractConfigButton = False
configSizeSmall = 20
configSizeCurrent = 0
configSizeLarge = 200
drop = 0
carColours = [(1,1,1),(0,0,0),(189,0,0),(189,86,0),(0,113,113),(0,151,0),(189/255,0,0),(189/255,86/255,0),(0,113/255,113/255),(0,151/255,0)]
backgroundColours = [(255/255,255/255,255/255),(212.5/255,212.5/255,212.5/255), (170/255,170/255,170/255),(127.5/255,127.5/255,127.5/255),(85/255,85/255,85/255),(42.5/255,42.5/255,42.5/255),(0,0,0)]
scaleButtons = []

lowerAngle = False
raiseAngle = False
angleTarget = 90

##how long it takes for car to fade out
fadeTime = 10 # 1 meams off, 10 means on  - changes to 10 onlcik to make it on# Was thinking about making it a slider- I'll leave it a int in case i decdide to change this

##gfx setting
highPerformanceOn = 0
highPerformanceOnClicked = False
#
indicatorMode = False
indicatorFlagMode = True
proxRange =  8#using anymore?
proxSolid = True
flagWidth = 1
flagLength = 1

blueFlags = False

##overall opacity
overallOpacity = 1

backgroundColourIndex = 0
backgroundShape = 0

##counters etc
cogRotation = 0
timeStart = 0
activatedStart = 0
configWindowOpen = False
border = False
borderRadius = 0
boundary = 0
testRun = False

#bottleneck protection vars
converterAvailable = True
converterWait = False
converterWaitCount = 0

def acMain(ac_version):
	global appWindow,title,configButton,configButton2,configSizeCurrent,configSizeSmall,configSizeLarge,scaleButtons,background,scale,playerCarMeshColourIndex,playerCarOutlineColourIndex,otherCarMeshColourIndex,otherCarOutlineColourIndex,carAura,fadeTime,fadeSwitch,carAuraTarget,angleOfInfluence,angleTarget,highPerformanceOn,highPerformanceOnClicked,indicatorSwitch,indicatorMode,otherColourLabel,otherColourPlus,otherColourMinus,proximityLabel,proxPlus,proxMinus,proxRange,blueFlags,blueFlagSwitch,overallOpacity,indicatorFlagMode,indicatorFlagSwitch,flagClickUp,flagClickDown,proxSolid,flagTypeSwitch,flagWidth,flagLength,flagTypeButton,indicatorWidthButton,indicatorLengthButton,flag,indicatorMinus,indicatorPlus,indicatorLengthMinus,indicatorLengthPlus, backgroundColourIndex,backgroundColourSwitch,backgroundColourLabel,backgroundTypePlus,backgroundTypeMinus,backgroundTypeLabel,backgroundShape,rearCutOffDistance,rearCutOffDistanceClickUp,rearCutOffDistanceClickDown


	#check for config file
	#get user directory		

	homeDirectory = os.path.expanduser("~")

	

	d = os.path.join(homeDirectory,"Documents","Assetto Corsa","apps","carRadar")
	#if this path doesnt exist, delete old folder and create a new one in the place which mirrors AC installation folder - I had this in the wrong place- only delete old fodler once in case somebody else makes same mistake
	if(not os.path.isdir(d)):
		toRemove = os.path.join(homeDirectory,"Documents","Assetto Corsa","content","apps")
		if(os.path.isdir(toRemove)):		
			shutil.rmtree(toRemove)
		

	#check if we have dropped file before
	filename = 'config.txt'
	configFileLocation = os.path.join(d, filename)
	#ac.log(str(configFileLocation))
	configAvailable = os.path.isfile(configFileLocation)
	
	lines = []
	if(configAvailable):
		configFile = open(configFileLocation, "r")
		lines = configFile.readlines()

	if configAvailable and len(lines) > 0:	
		#grab values from the file and enter in to variables		
		line = lines[0]
		lineList = line.split(" ")
		scale = int(lineList[1])

		line = lines[1]
		lineList = line.split(" ")
		playerCarMeshColourIndex = int(lineList[1])

		line = lines[2]
		lineList = line.split(" ")
		playerCarOutlineColourIndex = int(lineList[1])

		line = lines[3]
		lineList = line.split(" ")
		otherCarMeshColourIndex = int(lineList[1])

		line = lines[4]
		lineList = line.split(" ")
		otherCarOutlineColourIndex = int(lineList[1])

		#check to see if lines have been written yet, will not be written first use after update
		if(len(lines) > 5):
			#ac.log("Reading angle and range from file")
			line = lines[5]
			lineList = line.split(" ")
			carAura = float(lineList[1])
			carAuraTarget = float(lineList[1])


			line = lines[6]
			lineList = line.split(" ")
			angleOfInfluence = float(lineList[1])
			angleTarget = float(lineList[1])
		#addin simple mode on second update
		if len(lines) > 7:
			line = lines[7]
			lineList = line.split(" ")
			if(int(lineList[1]) == 0):
				highPerformanceOnClicked = False
			else:
				highPerformanceOnClicked = True

			line = lines[8]
			lineList = line.split(" ")
			if(int(lineList[1]) == 0):
				indicatorMode = False
			else:
				indicatorMode = True

			line = lines[9]
			lineList = line.split(" ")
			#proxRange = int(lineList[1]) # not using anymore

		if(len(lines) > 10):
			line = lines[10]
			lineList = line.split(" ")
			if(int(lineList[1]) == 0):
				blueFlags = False
			else:
				blueFlags = True

		if(len(lines) > 11):
			line = lines[11]
			lineList = line.split(" ")
			if(int(lineList[1]) == 1):
				fadeTime = 1
			else:
				fadeTime = 10		

		if(len(lines) > 12):
			line = lines[12]
			lineList = line.split(" ")
			overallOpacity = float(lineList[1])

		if(len(lines) > 13):
			line = lines[13]
			lineList = line.split(" ")
			if(int(lineList[1]) == 0):
				indicatorFlagMode = False
			else:
				indicatorFlagMode = True

		if(len(lines) > 14):			
			line = lines[14]
			lineList = line.split(" ")
			if(int(lineList[1]) == 0):				
				proxSolid = False
			else:				
				proxSolid = True

		if(len(lines) > 15):			
			line = lines[15]
			lineList = line.split(" ")
			flagWidth = int(lineList[1])

		if(len(lines) > 16):			
			line = lines[16]
			lineList = line.split(" ")
			backgroundColourIndex = int(lineList[1])

		if(len(lines) > 17):			
			line = lines[17]
			lineList = line.split(" ")
			backgroundShape = int(lineList[1])

		if(len(lines) > 18):			
			line = lines[18]
			lineList = line.split(" ")
			flagLength = float(lineList[1])

		if(len(lines) > 19):			
			line = lines[19]
			lineList = line.split(" ")
			rearCutOffDistance = float(lineList[1])

		configFile.close()

	else:
		##do we need this? makes the file on shutdown anyway
		#ac.log("writing file")
		if not os.path.exists(d):
			#ac.log("Making config dir")
			os.makedirs(d)

		#no file, we need to create one
		#ac.log(str(configFileLocation))
		cf = open(configFileLocation, "w")
		#ac.log("opened file")
		cf.write("scale " + str(scale)+'\n')
		cf.write("playerColour " + str(playerCarMeshColourIndex)+'\n')
		cf.write("playerOutline " + str(playerCarOutlineColourIndex)+'\n')
		cf.write("otherColour " + str(otherCarMeshColourIndex)+'\n')
		cf.write("otherOutline " + str(otherCarOutlineColourIndex)+'\n')
		cf.write("range " + str(carAuraTarget)+'\n')
		cf.write("angle " + str(angleTarget)+'\n')

		if(highPerformanceOnClicked == False):
			cf.write("simpleMode " + str(0)+'\n')
		else:
			cf.write("simpleMode " + str(1)+'\n')

		if(indicatorMode == False):
			cf.write("proximityMode " + str(0)+'\n')
		else:
			cf.write("proximityMode " + str(1)+'\n')

		cf.write("proxRange " + str(proxRange)+'\n')

		if(blueFlags == False):
			cf.write("blueFlags " + str(0)+'\n')
		else:
			cf.write("blueFlags " + str(1)+'\n')

		if(fadeTime == 1):
			cf.write("fadeTime " + str(1)+'\n')
		else:
			cf.write("fadeTime " + str(10)+'\n')

		if(overallOpacity == False):
			cf.write("overallOpacity " + str(0)+'\n')
		else:
			cf.write("overallOpacity " + str(1)+'\n')

		if(indicatorFlagMode == False):
			cf.write("indicatorFlagMode " + str(0)+'\n')
		else:
			cf.write("indicatorFlagMode " + str(1)+'\n')

		if(proxSolid == False):
			cf.write("proxSolid " + str(0)+'\n')
		else:
			cf.write("proxSolid " + str(1)+'\n')

		cf.write("flagWidth " + str(flagWidth)+'\n')

		cf.write("backgroundColourIndex " + str(backgroundColourIndex)+'\n')

		cf.write("backgroundShape " + str(backgroundShape)+ '\n')

		cf.write("flagLength " + str(flagLength)+ '\n')

		cf.write("rearCutOffDistance " + str(rearCutOffDistance)+'\n')

		cf.close()

	appWindow = ac.newApp("carRadar")
	#strip title name, we don't want it floating there
	ac.setTitle(appWindow, "")
	#titleLabel = ac.addLabel(appWindow,"Car Radar Label")
	#hide AC icon
	ac.setIconPosition(appWindow, 10000, 10000)
	ac.setSize(appWindow, windowWidth, windowWidth)
	ac.drawBorder(appWindow,0)
	#tell AC to render every frame
	ac.addRenderCallback(appWindow , goGoCarRadar)
	#only run code if app is active??????????????
	
	ac.addOnAppActivatedListener(appWindow,onActivated)


	#tell Ac to listen for any clicks on the app window
	ac.addOnClickedListener(appWindow,onClick)

	configButton = ac.addButton(appWindow,"")
	ac.setVisible(configButton,0)
	ac.setFontAlignment(configButton,"left")
	ac.setBackgroundOpacity(configButton,0)
	ac.drawBorder(configButton,0)
	ac.drawBackground(configButton,0)
	ac.setSize(configButton,50,50)
	ac.setPosition(configButton,windowWidth,0)
	ac.addOnClickedListener(configButton,extend)	
	ac.addOnClickedListener(configButton,retract)

	#background
	background = ac.addButton(appWindow,"")
	ac.setVisible(background,1)	
	ac.setBackgroundOpacity(background,0.66)
	ac.drawBorder(background,0)
	ac.drawBackground(background,1)
	ac.setSize(background,50,50)
	ac.setPosition(background,windowWidth,0)
	

	#scale
	scaleLabel = ac.addLabel(appWindow,"SCALE")
	ac.setFontAlignment(scaleLabel,"left")
	ac.drawBorder(scaleLabel,1)
	ac.setSize(scaleLabel,80,20)
	ac.setPosition(scaleLabel,windowWidth + 20 ,20)
	ac.setVisible(scaleLabel,0)
	scaleButtons.append(scaleLabel)

	scaleButtonPlus = ac.addButton(appWindow," + ")	
	ac.setFontAlignment(scaleButtonPlus,"left")
	ac.drawBorder(scaleButtonPlus,1)
	ac.setSize(scaleButtonPlus,20,20)
	ac.setPosition(scaleButtonPlus,windowWidth + 20 + 80 + 20 + 20 + 20,20)
	ac.setVisible(scaleButtonPlus,0)
	scaleButtons.append(scaleButtonPlus)
	ac.addOnClickedListener(scaleButtonPlus,scaleClickUp)

	scaleButtonMinus = ac.addButton(appWindow," - ")	
	ac.setFontAlignment(scaleButtonMinus,"left")
	ac.drawBorder(scaleButtonMinus,1)
	ac.setSize(scaleButtonMinus,20,20)
	ac.setPosition(scaleButtonMinus,windowWidth + 20 + 80 + 20 + 20,20)
	ac.setVisible(scaleButtonMinus,0)
	scaleButtons.append(scaleButtonMinus)
	ac.addOnClickedListener(scaleButtonMinus,scaleClickDown)

	playerColourLabel = ac.addLabel(appWindow,"PLAYER COLOUR")
	ac.setFontAlignment(playerColourLabel,"left")
	ac.drawBorder(playerColourLabel,1)
	ac.setSize(playerColourLabel,100,20)
	ac.setPosition(playerColourLabel,windowWidth + 20 ,40)
	ac.setVisible(playerColourLabel,0)
	scaleButtons.append(playerColourLabel)

	playerColourMinus = ac.addButton(appWindow," - ")	
	#ac.setFontSize(playerColourMinus,14)
	ac.setFontAlignment(playerColourMinus,"left")
	ac.drawBorder(playerColourMinus,1)
	ac.setSize(playerColourMinus,20,20)
	ac.setPosition(playerColourMinus,windowWidth + 20 + 80+ 20 +20 ,40)
	ac.setVisible(playerColourMinus,0)
	scaleButtons.append(playerColourMinus)
	ac.addOnClickedListener(playerColourMinus,playerColourMinusClick)

	playerColourPlus = ac.addButton(appWindow," + ")	
	ac.setFontAlignment(playerColourPlus,"left")
	ac.drawBorder(playerColourPlus,1)
	ac.setSize(playerColourPlus,20,20)
	ac.setPosition(playerColourPlus,windowWidth + 20 + 80 + 20 +40 ,40)
	ac.setVisible(playerColourPlus,0)
	scaleButtons.append(playerColourPlus)
	ac.addOnClickedListener(playerColourPlus,playerColourPlusClick)

	playerOutlineLabel = ac.addLabel(appWindow,"PLAYER OUTLINE")
	ac.setFontAlignment(playerOutlineLabel,"left")
	ac.drawBorder(playerOutlineLabel,1)
	ac.setSize(playerOutlineLabel,100,20)
	ac.setPosition(playerOutlineLabel,windowWidth + 20 ,60)
	ac.setVisible(playerOutlineLabel,0)
	scaleButtons.append(playerOutlineLabel)

	playerOutlineMinus = ac.addButton(appWindow," - ")	
	ac.setFontAlignment(playerOutlineMinus,"left")
	ac.drawBorder(playerOutlineMinus,1)
	ac.setSize(playerOutlineMinus,20,20)
	ac.setPosition(playerOutlineMinus,windowWidth + 20 + 80+ 20 +20 ,60)
	ac.setVisible(playerOutlineMinus,0)
	scaleButtons.append(playerOutlineMinus)
	ac.addOnClickedListener(playerOutlineMinus,playerOutlineMinusClick)

	playerOutlinePlus = ac.addButton(appWindow," + ")	
	ac.setFontAlignment(playerOutlinePlus,"left")
	ac.drawBorder(playerOutlinePlus,1)
	ac.setSize(playerOutlinePlus,20,20)
	ac.setPosition(playerOutlinePlus,windowWidth + 20 + 80 + 20 +40 ,60)
	ac.setVisible(playerOutlinePlus,0)
	scaleButtons.append(playerOutlinePlus)
	ac.addOnClickedListener(playerOutlinePlus,playerOutlinePlusClick)	

	otherColourLabel = ac.addLabel(appWindow,"OTHER COLOUR")
	ac.setFontAlignment(otherColourLabel,"left")
	ac.drawBorder(otherColourLabel,1)
	ac.setSize(otherColourLabel,100,20)
	ac.setPosition(otherColourLabel,windowWidth + 20 ,80)
	ac.setVisible(otherColourLabel,0)
	scaleButtons.append(otherColourLabel)

	otherColourMinus = ac.addButton(appWindow," - ")	
	ac.setFontAlignment(otherColourMinus,"left")
	ac.drawBorder(otherColourMinus,1)
	ac.setSize(otherColourMinus,20,20)
	ac.setPosition(otherColourMinus,windowWidth + 20 + 80+ 20 + 20 ,80)
	ac.setVisible(otherColourMinus,0)
	scaleButtons.append(otherColourMinus)
	ac.addOnClickedListener(otherColourMinus,otherColourMinusClick)

	otherColourPlus = ac.addButton(appWindow," + ")	
	ac.setFontAlignment(otherColourPlus,"left")
	ac.drawBorder(otherColourPlus,1)
	ac.setSize(otherColourPlus,20,20)
	ac.setPosition(otherColourPlus,windowWidth + 20 + 80 + 20 + 40 ,80)
	ac.setVisible(otherColourPlus,0)
	scaleButtons.append(otherColourPlus)
	ac.addOnClickedListener(otherColourPlus,otherColourPlusClick)

	if(indicatorMode):
		ac.setFontColor(otherColourLabel,1,1,1,0.2)
		ac.setFontColor(otherColourPlus,1,1,1,0.2)
		ac.setFontColor(otherColourMinus,1,1,1,0.2)


	otherOutlineLabel = ac.addLabel(appWindow,"OTHER OUTLINE")
	ac.setFontAlignment(otherOutlineLabel,"left")
	ac.drawBorder(otherOutlineLabel,1)
	ac.setSize(otherOutlineLabel,100,20)
	ac.setPosition(otherOutlineLabel,windowWidth + 20 ,100)
	ac.setVisible(otherOutlineLabel,0)
	scaleButtons.append(otherOutlineLabel)

	otherOutlineMinus = ac.addButton(appWindow," - ")	
	ac.setFontAlignment(otherOutlineMinus,"left")
	ac.drawBorder(otherOutlineMinus,1)
	ac.setSize(otherOutlineMinus,20,20)
	ac.setPosition(otherOutlineMinus,windowWidth + 20 + 80+ 20 + 20 ,100)
	ac.setVisible(otherOutlineMinus,0)
	scaleButtons.append(otherOutlineMinus)
	ac.addOnClickedListener(otherOutlineMinus,otherOutlineMinusClick)

	otherOutlinePlus = ac.addButton(appWindow," + ")	
	ac.setFontAlignment(otherOutlinePlus,"left")
	ac.drawBorder(otherOutlinePlus,1)
	ac.setSize(otherOutlinePlus,20,20)
	ac.setPosition(otherOutlinePlus,windowWidth + 20 + 80 + 20 + 40 ,100)
	ac.setVisible(otherOutlinePlus,0)
	scaleButtons.append(otherOutlinePlus)
	ac.addOnClickedListener(otherOutlinePlus,otherOutlinePlusClick)	

	rangeLabel = ac.addLabel(appWindow,"RANGE")
	ac.setFontAlignment(rangeLabel,"left")
	ac.drawBorder(rangeLabel,1)
	ac.setSize(rangeLabel,80,20)
	ac.setPosition(rangeLabel,windowWidth + 20 ,120)
	ac.setVisible(rangeLabel,0)
	scaleButtons.append(rangeLabel)

	rangeMinus = ac.addButton(appWindow," - ")
	ac.setFontAlignment(rangeMinus,"left")
	ac.drawBorder(rangeMinus,1)
	ac.setSize(rangeMinus,20,20)
	ac.setPosition(rangeMinus,windowWidth + 20 + 80 + 20 + 20 ,120)
	ac.setVisible(rangeMinus,0)
	scaleButtons.append(rangeMinus)
	ac.addOnClickedListener(rangeMinus,rangeClickDown)

	rangePlus = ac.addButton(appWindow," + ")	
	ac.setFontAlignment(rangePlus,"left")
	ac.drawBorder(rangePlus,1)
	ac.setSize(rangePlus,20,20)
	ac.setPosition(rangePlus,windowWidth + 20 + 80 + 20 + 20 + 20,120)
	ac.setVisible(rangePlus,0)
	scaleButtons.append(rangePlus)
	ac.addOnClickedListener(rangePlus,rangeClickUp)

	
	rearCutOffDistanceLabel = ac.addLabel(appWindow,"REAR CUT OFF")
	ac.setFontAlignment(rearCutOffDistanceLabel,"left")
	ac.drawBorder(rearCutOffDistanceLabel,1)
	ac.setSize(rearCutOffDistanceLabel,80,20)
	ac.setPosition(rearCutOffDistanceLabel,windowWidth + 20 ,140)
	ac.setVisible(rearCutOffDistanceLabel,0)
	scaleButtons.append(rearCutOffDistanceLabel)

	rearCutOffDistanceMinus = ac.addButton(appWindow," - ")
	ac.setFontAlignment(rearCutOffDistanceMinus,"left")
	ac.drawBorder(rearCutOffDistanceMinus,1)
	ac.setSize(rearCutOffDistanceMinus,20,20)
	ac.setPosition(rearCutOffDistanceMinus,windowWidth + 20 + 80 + 20 + 20 ,140)
	ac.setVisible(rearCutOffDistanceMinus,0)
	scaleButtons.append(rearCutOffDistanceMinus)
	ac.addOnClickedListener(rearCutOffDistanceMinus,rearCutOffDistanceClickDown)

	rearCutOffDistancePlus = ac.addButton(appWindow," + ")	
	ac.setFontAlignment(rearCutOffDistancePlus,"left")
	ac.drawBorder(rearCutOffDistancePlus,1)
	ac.setSize(rearCutOffDistancePlus,20,20)
	ac.setPosition(rearCutOffDistancePlus,windowWidth + 20 + 80 + 20 + 20 + 20,140)
	ac.setVisible(rearCutOffDistancePlus,0)
	scaleButtons.append(rearCutOffDistancePlus)
	ac.addOnClickedListener(rearCutOffDistancePlus,rearCutOffDistanceClickUp)

	fadeLabel = ac.addLabel(appWindow,"SMOOTH FADE")
	ac.setFontAlignment(fadeLabel,"left")
	ac.drawBorder(fadeLabel,1)
	ac.setSize(fadeLabel,80,20)
	ac.setPosition(fadeLabel,windowWidth + 20 ,160)
	ac.setVisible(fadeLabel,0)
	scaleButtons.append(fadeLabel)

	fadeSwitch = ac.addButton(appWindow,"")	
	ac.setFontAlignment(fadeSwitch,"left")
	ac.drawBackground(fadeSwitch,1)	
	if(fadeTime == 1):
		#set red
		ac.setBackgroundColor(fadeSwitch,189/255,0,0)
	else:
		#set green
		ac.setBackgroundColor(fadeSwitch,0,151/255,0)

	ac.setBackgroundOpacity(fadeSwitch,1)
	ac.drawBorder(fadeSwitch,1)
	ac.setSize(fadeSwitch,20,20)
	ac.setPosition(fadeSwitch,windowWidth + 20 + 80 + 20 + 20 + 20,160)
	ac.setVisible(fadeSwitch,0)
	scaleButtons.append(fadeSwitch)
	ac.addOnClickedListener(fadeSwitch,fadeClick)


	angleLabel = ac.addLabel(appWindow,"ANGLE")
	ac.setFontAlignment(angleLabel,"left")
	ac.drawBorder(angleLabel,1)
	ac.setSize(angleLabel,80,20)
	ac.setPosition(angleLabel,windowWidth + 20 ,180)
	ac.setVisible(angleLabel,0)
	scaleButtons.append(angleLabel)

	angleMinus = ac.addButton(appWindow," - ")
	ac.setFontAlignment(angleMinus,"left")
	ac.drawBorder(angleMinus,1)
	ac.setSize(angleMinus,20,20)
	ac.setPosition(angleMinus,windowWidth + 20 + 80 + 20 + 20 ,180)
	ac.setVisible(angleMinus,0)
	scaleButtons.append(angleMinus)
	ac.addOnClickedListener(angleMinus,angleClickDown)

	anglePlus = ac.addButton(appWindow," + ")	
	ac.setFontAlignment(anglePlus,"left")
	ac.drawBorder(anglePlus,1)
	ac.setSize(anglePlus,20,20)
	ac.setPosition(anglePlus,windowWidth + 20 + 80 + 20 + 20 + 20,180)
	ac.setVisible(anglePlus,0)
	scaleButtons.append(anglePlus)
	ac.addOnClickedListener(anglePlus,angleClickUp)

	highPerformance = ac.addLabel(appWindow,"SIMPLE MODE")
	ac.setFontAlignment(highPerformance,"left")
	ac.drawBorder(highPerformance,1)
	ac.setSize(highPerformance,80,20)
	ac.setPosition(highPerformance,windowWidth + 20 ,200)
	ac.setVisible(highPerformance,0)
	scaleButtons.append(highPerformance)

	highPerformanceOn = ac.addButton(appWindow,"")	
	ac.setFontAlignment(highPerformanceOn,"left")
	ac.drawBackground(highPerformanceOn,1)	
	#ac.setBackgroundColor(highPerformanceOn,carColours[2][0],carColours[2][1],carColours[2][2])
	if(highPerformanceOnClicked == False):
		#set red
		ac.setBackgroundColor(highPerformanceOn,189/255,0,0)
	else:
		#set green
		ac.setBackgroundColor(highPerformanceOn,0,151/255,0)

	ac.setBackgroundOpacity(highPerformanceOn,1)
	ac.drawBorder(highPerformanceOn,1)
	ac.setSize(highPerformanceOn,20,20)
	ac.setPosition(highPerformanceOn,windowWidth + 20 + 80 + 20 + 20 + 20,200)
	ac.setVisible(highPerformanceOn,0)
	scaleButtons.append(highPerformanceOn)
	ac.addOnClickedListener(highPerformanceOn,highPerformanceOnClick)

	indicatorButton = ac.addLabel(appWindow,"CAR PROXIMITY")
	ac.setFontAlignment(indicatorButton,"left")
	ac.drawBorder(indicatorButton,1)
	ac.setSize(indicatorButton,80,20)
	ac.setPosition(indicatorButton,windowWidth + 20 ,220)
	ac.setVisible(indicatorButton,0)
	scaleButtons.append(indicatorButton)

	indicatorSwitch = ac.addButton(appWindow,"")	
	ac.setFontAlignment(indicatorSwitch,"left")
	ac.drawBackground(indicatorSwitch,1)	
	#ac.setBackgroundColor(highPerformanceOn,carColours[2][0],carColours[2][1],carColours[2][2])
	if(indicatorMode == False):
		#set red
		ac.setBackgroundColor(indicatorSwitch,189/255,0,0)
	else:
		#set green
		ac.setBackgroundColor(indicatorSwitch,0,151/255,0)

	ac.setBackgroundOpacity(indicatorSwitch,1)
	ac.drawBorder(indicatorSwitch,1)
	ac.setSize(indicatorSwitch,20,20)
	ac.setPosition(indicatorSwitch,windowWidth + 20 + 80 + 20 + 20 + 20,220)
	ac.setVisible(indicatorSwitch,0)
	scaleButtons.append(indicatorSwitch)
	ac.addOnClickedListener(indicatorSwitch,indicatorClick)

	indicatorFlagsButton = ac.addLabel(appWindow,"WARNING FLAGS")
	ac.setFontAlignment(indicatorFlagsButton,"left")
	ac.drawBorder(indicatorFlagsButton,1)
	ac.setSize(indicatorFlagsButton,80,20)
	ac.setPosition(indicatorFlagsButton,windowWidth + 20 ,240)
	ac.setVisible(indicatorFlagsButton,0)
	scaleButtons.append(indicatorFlagsButton)

	indicatorFlagSwitch = ac.addButton(appWindow,"")	
	ac.setFontAlignment(indicatorFlagSwitch,"left")
	ac.drawBackground(indicatorFlagSwitch,1)	
	#ac.setBackgroundColor(highPerformanceOn,carColours[2][0],carColours[2][1],carColours[2][2])
	if(indicatorFlagMode == False):
		#set red
		ac.setBackgroundColor(indicatorFlagSwitch,189/255,0,0)
	else:
		#set green
		ac.setBackgroundColor(indicatorFlagSwitch,0,151/255,0)

	ac.setBackgroundOpacity(indicatorFlagSwitch,1)
	ac.drawBorder(indicatorFlagSwitch,1)
	ac.setSize(indicatorFlagSwitch,20,20)
	ac.setPosition(indicatorFlagSwitch,windowWidth + 20 + 80 + 20 + 20 + 20,240)
	ac.setVisible(indicatorFlagSwitch,0)
	scaleButtons.append(indicatorFlagSwitch)
	ac.addOnClickedListener(indicatorFlagSwitch,indicatorFlagClick)

	flagTypeButton = ac.addLabel(appWindow," - TYPE")
	ac.setFontAlignment(flagTypeButton,"left")
	ac.drawBorder(flagTypeButton,1)
	ac.setSize(flagTypeButton,80,20)
	ac.setPosition(flagTypeButton,windowWidth + 20 ,260)
	ac.setVisible(flagTypeButton,0)
	scaleButtons.append(flagTypeButton)

	flagTypeSwitch = ac.addButton(appWindow,"")	
	ac.setFontAlignment(flagTypeSwitch,"left")
	ac.drawBackground(flagTypeSwitch,1)	
	#ac.setBackgroundColor(highPerformanceOn,carColours[2][0],carColours[2][1],carColours[2][2])
	if(proxSolid == True):		
		ac.setBackgroundColor(flagTypeSwitch,255/255,255/255,51/255)
		ac.setBackgroundOpacity(flagTypeSwitch,.8)		

	else:		
		ac.setBackgroundColor(flagTypeSwitch,255/255,128/255,0)
		ac.setBackgroundOpacity(flagTypeSwitch,1)
	
	ac.drawBorder(flagTypeSwitch,1)
	ac.setSize(flagTypeSwitch,20,20)
	ac.setPosition(flagTypeSwitch,windowWidth + 20 + 80 + 20 + 20 + 20,260)
	ac.setVisible(flagTypeSwitch,0)
	scaleButtons.append(flagTypeSwitch)
	ac.addOnClickedListener(flagTypeSwitch,proxSolidClick)


	indicatorWidthButton = ac.addLabel(appWindow," - WIDTH")
	ac.setFontAlignment(indicatorWidthButton,"left")
	ac.drawBorder(indicatorWidthButton,1)
	ac.setSize(indicatorWidthButton,80,20)
	ac.setPosition(indicatorWidthButton,windowWidth + 20 ,280)
	ac.setVisible(indicatorWidthButton,0)
	scaleButtons.append(indicatorWidthButton)

	indicatorMinus = ac.addButton(appWindow," - ")
	ac.setFontAlignment(indicatorMinus,"left")
	ac.drawBorder(indicatorMinus,1)
	ac.setSize(indicatorMinus,20,20)
	ac.setPosition(indicatorMinus,windowWidth + 20 + 80 + 20 + 20 ,280)
	ac.setVisible(indicatorMinus,0)
	scaleButtons.append(indicatorMinus)
	ac.addOnClickedListener(indicatorMinus,flagClickDown)

	indicatorPlus = ac.addButton(appWindow," + ")	
	ac.setFontAlignment(indicatorPlus,"left")
	ac.drawBorder(indicatorPlus,1)
	ac.setSize(indicatorPlus,20,20)
	ac.setPosition(indicatorPlus,windowWidth + 20 + 80 + 20 + 20 + 20,280)
	ac.setVisible(indicatorPlus,0)
	scaleButtons.append(indicatorPlus)
	ac.addOnClickedListener(indicatorPlus,flagClickUp)

	indicatorLengthButton = ac.addLabel(appWindow," - LENGTH")
	ac.setFontAlignment(indicatorLengthButton,"left")
	ac.drawBorder(indicatorLengthButton,1)
	ac.setSize(indicatorLengthButton,80,20)
	ac.setPosition(indicatorLengthButton,windowWidth + 20 ,300)
	ac.setVisible(indicatorLengthButton,0)
	scaleButtons.append(indicatorLengthButton)

	indicatorLengthMinus = ac.addButton(appWindow," - ")
	ac.setFontAlignment(indicatorLengthMinus,"left")
	ac.drawBorder(indicatorLengthMinus,1)
	ac.setSize(indicatorLengthMinus,20,20)
	ac.setPosition(indicatorLengthMinus,windowWidth + 20 + 80 + 20 + 20 ,300)
	ac.setVisible(indicatorLengthMinus,0)
	scaleButtons.append(indicatorLengthMinus)
	ac.addOnClickedListener(indicatorLengthMinus,flagLengthClickDown)

	indicatorLengthPlus = ac.addButton(appWindow," + ")	
	ac.setFontAlignment(indicatorLengthPlus,"left")
	ac.drawBorder(indicatorLengthPlus,1)
	ac.setSize(indicatorLengthPlus,20,20)
	ac.setPosition(indicatorLengthPlus,windowWidth + 20 + 80 + 20 + 20 + 20,300)
	ac.setVisible(indicatorLengthPlus,0)
	scaleButtons.append(indicatorLengthPlus)
	ac.addOnClickedListener(indicatorLengthPlus,flagLengthClickUp)


	blueFlagLabel = ac.addLabel(appWindow,"BLUE FLAGS")
	ac.setFontAlignment(blueFlagLabel,"left")
	ac.drawBorder(blueFlagLabel,1)
	ac.setSize(blueFlagLabel,80,20)
	ac.setPosition(blueFlagLabel,windowWidth + 20 ,320)
	ac.setVisible(blueFlagLabel,0)
	scaleButtons.append(blueFlagLabel)

	blueFlagSwitch = ac.addButton(appWindow,"")	
	ac.setFontAlignment(blueFlagSwitch,"left")
	ac.drawBorder(blueFlagSwitch,1)
	ac.setSize(blueFlagSwitch,20,20)
	ac.setPosition(blueFlagSwitch,windowWidth + 20 + 80 + 20 + 20 + 20,320)
	ac.setVisible(blueFlagSwitch,0)
	scaleButtons.append(blueFlagSwitch)
	if blueFlags == True:
		
		ac.setBackgroundColor(blueFlagSwitch,0.15,0.15,200/255)		
		ac.setBackgroundOpacity(blueFlagSwitch,1)
	else:
		#
		ac.setBackgroundColor(blueFlagSwitch,1,1,1)
		ac.setBackgroundOpacity(blueFlagSwitch,0.2)

	ac.addOnClickedListener(blueFlagSwitch,blueFlagClick)

	backgroundColourLabel = ac.addLabel(appWindow,"BACKGROUND")
	ac.setFontAlignment(backgroundColourLabel,"left")
	ac.drawBorder(backgroundColourLabel,1)
	ac.setSize(backgroundColourLabel,80,20)
	ac.setPosition(backgroundColourLabel,windowWidth + 20 ,340)
	ac.setVisible(backgroundColourLabel,0)
	scaleButtons.append(backgroundColourLabel)

	backgroundColourSwitch = ac.addButton(appWindow,"")	
	ac.setFontAlignment(backgroundColourSwitch,"left")
	ac.drawBorder(backgroundColourSwitch,1)
	ac.setSize(backgroundColourSwitch,20,20)
	ac.setPosition(backgroundColourSwitch,windowWidth + 20 + 80 + 20 + 20 + 20,340)
	ac.setVisible(backgroundColourSwitch,0)
	scaleButtons.append(backgroundColourSwitch)
	if backgroundColourIndex == 0:
		
		ac.setBackgroundColor(backgroundColourSwitch,0.15,0.15,200/255)		
		ac.setBackgroundOpacity(backgroundColourSwitch,1)
	else:
		#
		ac.setBackgroundColor(backgroundColourSwitch,1,1,1)
		ac.setBackgroundOpacity(backgroundColourSwitch,1)

	ac.addOnClickedListener(backgroundColourSwitch,backgroundColourClick)

	backgroundTypeLabel = ac.addLabel(appWindow," - SHAPE")
	ac.setFontAlignment(backgroundTypeLabel,"left")
	ac.drawBorder(backgroundTypeLabel,1)
	ac.setSize(backgroundTypeLabel,80,20)
	ac.setPosition(backgroundTypeLabel,windowWidth + 20 ,360)
	ac.setVisible(backgroundTypeLabel,0)
	scaleButtons.append(backgroundTypeLabel)

	backgroundTypeMinus = ac.addButton(appWindow," - ")
	ac.setFontAlignment(backgroundTypeMinus,"left")
	ac.drawBorder(backgroundTypeMinus,1)
	ac.setSize(backgroundTypeMinus,20,20)
	ac.setPosition(backgroundTypeMinus,windowWidth + 20 + 80 + 20 + 20 ,360)
	ac.setVisible(backgroundTypeMinus,0)
	scaleButtons.append(backgroundTypeMinus)
	ac.addOnClickedListener(backgroundTypeMinus,backgroundTypeMinusClick)

	backgroundTypePlus = ac.addButton(appWindow," + ")	
	ac.setFontAlignment(backgroundTypePlus,"left")
	ac.drawBorder(backgroundTypePlus,1)
	ac.setSize(backgroundTypePlus,20,20)
	ac.setPosition(backgroundTypePlus,windowWidth + 20 + 80 + 20 + 20 + 20,360)
	ac.setVisible(backgroundTypePlus,0)
	scaleButtons.append(backgroundTypePlus)
	ac.addOnClickedListener(backgroundTypePlus,backgroundTypePlusClick)

	overallOpacityLabel = ac.addLabel(appWindow,"OPACITY")
	ac.setFontAlignment(overallOpacityLabel,"left")
	ac.drawBorder(overallOpacityLabel,1)
	ac.setSize(overallOpacityLabel,80,20)
	ac.setPosition(overallOpacityLabel,windowWidth + 20 ,380)
	ac.setVisible(overallOpacityLabel,0)
	scaleButtons.append(overallOpacityLabel)

	overallOpacityMinus = ac.addButton(appWindow," - ")
	ac.setFontAlignment(overallOpacityMinus,"left")
	ac.drawBorder(overallOpacityMinus,1)
	ac.setSize(overallOpacityMinus,20,20)
	ac.setPosition(overallOpacityMinus,windowWidth + 20 + 80 + 20 + 20 ,380)
	ac.setVisible(overallOpacityMinus,0)
	scaleButtons.append(overallOpacityMinus)
	ac.addOnClickedListener(overallOpacityMinus,opacityDown)

	overallOpacityPlus = ac.addButton(appWindow," + ")	
	ac.setFontAlignment(overallOpacityPlus,"left")
	ac.drawBorder(overallOpacityPlus,1)
	ac.setSize(overallOpacityPlus,20,20)
	ac.setPosition(overallOpacityPlus,windowWidth + 20 + 80 + 20 + 20 + 20,380)
	ac.setVisible(overallOpacityPlus,0)
	scaleButtons.append(overallOpacityPlus)
	ac.addOnClickedListener(overallOpacityPlus,opacityUp)

	##switches, not all are here, some are done when declaring the buttons above
	if indicatorFlagMode == False:
		
		ac.setBackgroundColor(indicatorFlagSwitch,189/255,0,0)
		ac.setBackgroundOpacity(indicatorFlagSwitch,1)
		ac.setFontColor(otherColourLabel,1,1,1,1)
		ac.setFontColor(otherColourMinus,1,1,1,1)
		ac.setFontColor(otherColourPlus,1,1,1,1)
		ac.setFontColor(flagTypeButton,1,1,1,0.5)
		ac.setFontColor(indicatorWidthButton,1,1,1,.5)
		ac.setFontColor(indicatorLengthButton,1,1,1,.5)
		ac.setBackgroundOpacity(flagTypeSwitch,0.5)
		ac.setFontColor(indicatorMinus,1,1,1,0.5)
		ac.setFontColor(indicatorPlus,1,1,1,0.5)		
		ac.setFontColor(indicatorLengthMinus,1,1,1,0.5)
		ac.setFontColor(indicatorLengthPlus,1,1,1,0.5)

	else:
		ac.setBackgroundColor(indicatorFlagSwitch,0,151/255,0)
		ac.setBackgroundOpacity(indicatorFlagSwitch,1)		
		#grey out other colour selector
		ac.setFontColor(otherColourLabel,1,1,1,0.2)
		ac.setFontColor(otherColourMinus,1,1,1,0.2)
		ac.setFontColor(otherColourPlus,1,1,1,0.2)
		##make other options to do with this not greyed out
		ac.setFontColor(flagTypeButton,1,1,1,1)
		ac.setFontColor(indicatorWidthButton,1,1,1,1)
		ac.setFontColor(indicatorLengthButton,1,1,1,1)
		ac.setBackgroundOpacity(flagTypeSwitch,1)
		ac.setFontColor(indicatorMinus,1,1,1,1)
		ac.setFontColor(indicatorPlus,1,1,1,1)
		ac.setFontColor(indicatorLengthMinus,1,1,1,1)
		ac.setFontColor(indicatorLengthPlus,1,1,1,1)

	##background colour setter
	if(backgroundColourIndex == 0):
		#no background, disable other background buttons
		ac.setBackgroundOpacity(backgroundTypePlus,.2)
		#ac.setBackgroundOpacity(backgroundTypeMinus,.2)
		#ac.setBackgroundOpacity(backgroundTypeLabel,.2)
		ac.setFontColor(backgroundTypeMinus,1,1,1,0.2)
		ac.setFontColor(backgroundTypePlus,1,1,1,0.2)

		ac.setFontColor(backgroundTypeLabel,1,1,1,0.2)

		ac.setBackgroundOpacity(backgroundColourSwitch,.2)
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[0][0],backgroundColours[0][1],backgroundColours[0][2])

	elif (backgroundColourIndex == 1):
		#ac.setBackgroundOpacity(backgroundTypePlus,1)
		#ac.setBackgroundOpacity(backgroundTypeMinus,1)
		ac.setFontColor(backgroundTypeMinus,1,1,1,1)
		ac.setFontColor(backgroundTypePlus,1,1,1,1)
		#ac.setBackgroundOpacity(backgroundTypeLabel,1)
		ac.setFontColor(backgroundTypeLabel,1,1,1,1)

		ac.setBackgroundOpacity(backgroundColourSwitch,1)
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[0][0],backgroundColours[0][1],backgroundColours[0][2])

	elif (backgroundColourIndex == 2):
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[1][0],backgroundColours[1][1],backgroundColours[1][2])		

	elif (backgroundColourIndex == 3):
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[2][0],backgroundColours[2][1],backgroundColours[2][2])		

	elif (backgroundColourIndex == 4):
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[3][0],backgroundColours[3][1],backgroundColours[3][2])

	elif (backgroundColourIndex == 5):	
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[4][0],backgroundColours[4][1],backgroundColours[4][2])

	elif (backgroundColourIndex == 6):	
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[5][0],backgroundColours[5][1],backgroundColours[5][2])

	elif (backgroundColourIndex == 7):	
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[6][0],backgroundColours[6][1],backgroundColours[6][2])

	doClick()

	buildCarList()
	return "carRadar"

def onActivated(*args):
	doClick()

def onClick(name,state):
	doClick()

def doClick():
	global appWindow,titleLabel,timeStart,border, borderRadius,extendConfigButton,configButton
	#ac.console("click")
	ac.setTitle(appWindow,"Car Radar")
	timeStart = time.clock() + 0.0001 #adding.001 because of the way the loop works below to catch the timer - I think this is bacause i don't fully understand how time.clock is working
	#ac.console(str(timeStart) + 'time started')
	border = True
	borderRadius = 0
	ac.setVisible(configButton,1)

def disappear(name, state):
	global configButton2
	#ac.log(str("pressed button"))
	x = ac.setVisible(configButton2,0)
	#ac.log(str(x))

def extend(name, state):
	global configButton,extendConfigButton,configSizeCurrent,configSizeSmall
	if configSizeCurrent == 0:
		#ac.console(str("pressed button - extend"))
		extendConfigButton = True

def retract(name, state):
	global configButton,retractConfigButton,configSizeCurrent,configSizeLarge
	if configSizeCurrent == configSizeLarge:
		#ac.console(str("pressed button - retract"))
		retractConfigButton = True
	#ac.log(str(x))

def scaleClickUp(name,state):
	global scale,scaleLimit
	if scale < scaleLimit:
		scale += 1

def scaleClickDown(name,state):
	global scale
	scale -= 1

	if(scale < 1):
		scale = 1

def showPlayerClick(name, state):
	global drawPlayerCar
	drawPlayerCar = not drawPlayerCar
	#ac.console(str(drawPlayerCar))	

def scaleClickUpBig(name,state):
	global scale,scaleValue	
	scale+= 10	

def scaleClickDownBig(name,state):
	global scale,scaleValue	
	scale-= 10

	if(scale < 0):
		scale = 0

def playerColourPlusClick(name,state):
	global playerCarMeshColourIndex
	playerCarMeshColourIndex += 1

	l = len(carColours)
	if playerCarMeshColourIndex > l-1:
		playerCarMeshColourIndex = 0

def playerColourMinusClick(name,state):
	global playerCarMeshColourIndex
	playerCarMeshColourIndex -= 1

	l = len(carColours)
	if playerCarMeshColourIndex < 0:
		playerCarMeshColourIndex = l-1	

def playerOutlinePlusClick(name,state):
	global playerCarOutlineColourIndex
	playerCarOutlineColourIndex += 1

	l = len(carColours)
	if playerCarOutlineColourIndex > l-1:
		playerCarOutlineColourIndex = 0

def playerOutlineMinusClick(name,state):
	global playerCarOutlineColourIndex
	playerCarOutlineColourIndex -= 1

	l = len(carColours)
	if playerCarOutlineColourIndex < 0:
		playerCarOutlineColourIndex = l-1

def otherColourPlusClick(name,state):
	global otherCarMeshColourIndex,indicatorMode
	
	if(indicatorMode):
		return

	otherCarMeshColourIndex += 1

	l = len(carColours)
	if otherCarMeshColourIndex > l-1:
		otherCarMeshColourIndex = 0

def otherColourMinusClick(name,state):
	global otherCarMeshColourIndex,indicatorMode
	if(indicatorMode):
		return

	otherCarMeshColourIndex -= 1

	l = len(carColours)
	if otherCarMeshColourIndex < 0:
		otherCarMeshColourIndex = l-1	

def otherOutlinePlusClick(name,state):
	global otherCarOutlineColourIndex
	
	otherCarOutlineColourIndex += 1

	l = len(carColours)
	if otherCarOutlineColourIndex > l-1:
		otherCarOutlineColourIndex = 0

def otherOutlineMinusClick(name,state):
	global otherCarOutlineColourIndex
	otherCarOutlineColourIndex -= 1

	l = len(carColours)
	if otherCarOutlineColourIndex < 0:
		otherCarOutlineColourIndex = l-1

def rangeClickUp(name,state):
	global carAuraTarget,raiseCarAura
	
	raiseCarAura = True
	carAuraTarget += 5	

def rangeClickDown(name,state):
	global carAuraTarget,lowerCarAura

	lowerCarAura = True
	carAuraTarget -= 5
	if(carAuraTarget < 0):
		carAuraTarget = 0

def rearCutOffDistanceClickUp(name,state):
	global rearCutOffDistance, raiseRearCutOffDistance, carAura
	
	raiseRearCutOffDistance = True
	rearCutOffDistance += 2.5	
	if(rearCutOffDistance > carAura - 2.5):
		rearCutOffDistance = carAura - 2.5

def rearCutOffDistanceClickDown(name,state):
	global rearCutOffDistance, lowerRearCutOffDistance

	lowerRearCutOffDistance = True
	rearCutOffDistance -= 2.5
	if(rearCutOffDistance < 0):
		rearCutOffDistance = 0

def angleClickUp(name, state):
	global angleTarget,raiseAngle

	raiseAngle = True
	angleTarget -= 10
	if angleTarget < 0:
		angleTarget = 0

def angleClickDown(name, state):
	global angleTarget,lowerAngle

	lowerAngle = True
	angleTarget += 10
	if angleTarget > 360:
		angleTarget = 360

def opacityUp(name,state):
	global overallOpacity	
	overallOpacity += 0.1

	if((overallOpacity>=1)):
		overallOpacity = 1	

def opacityDown(name,state):
	global overallOpacity
	overallOpacity -= 0.1

	if(overallOpacity <= 0.4):
		overallOpacity = 0.4

def highPerformanceOnClick(name,state):
	global highPerformanceOnClicked,carColours,highPerformanceOn

	#ac.setBackgroundColor(highPerformanceOn,carColours[5][0],carColours[5][1],carColours[5][2])
	if highPerformanceOnClicked == False:
		#change it to green
		ac.setBackgroundColor(highPerformanceOn,0,151/255,0)
		ac.setBackgroundOpacity(highPerformanceOn,1)
		highPerformanceOnClicked = True
		
	else:
		ac.setBackgroundColor(highPerformanceOn,189/255,0,0)
		ac.setBackgroundOpacity(highPerformanceOn,1)
		highPerformanceOnClicked = False

def fadeClick(name,state):
	global fadeTime,fadeSwitch

	#ac.setBackgroundColor(highPerformanceOn,carColours[5][0],carColours[5][1],carColours[5][2])
	if fadeTime == 1:
		#change it to green
		
		ac.setBackgroundColor(fadeSwitch,0,151/255,0)		
		ac.setBackgroundOpacity(fadeSwitch,1)
		fadeTime = 10
		
	else:
		ac.setBackgroundColor(fadeSwitch,189/255,0,0)
		ac.setBackgroundOpacity(fadeSwitch,1)
		fadeTime = 1

def indicatorClick(name,state):
	global indicatorMode,indicatorSwitch,otherColourLabel,otherColourPlus,otherColourMinus,proximityLabel,proxMinus,proxPlus

	#ac.setBackgroundColor(highPerformanceOn,carColours[5][0],carColours[5][1],carColours[5][2])
	if indicatorMode == False:
		#change it to green
		ac.setBackgroundColor(indicatorSwitch,0,151/255,0)
		ac.setBackgroundOpacity(indicatorSwitch,1)
		
		#grey out other colour selector
		ac.setFontColor(otherColourLabel,1,1,1,0.2)
		ac.setFontColor(otherColourMinus,1,1,1,0.2)
		ac.setFontColor(otherColourPlus,1,1,1,0.2)

		#ac.setFontColor(proximityLabel,1,1,1,1)
		#ac.setFontColor(proxMinus,1,1,1,1)
		#ac.setFontColor(proxPlus,1,1,1,1)

		indicatorMode = True

	else:
		ac.setBackgroundColor(indicatorSwitch,189/255,0,0)
		ac.setBackgroundOpacity(indicatorSwitch,1)

		ac.setFontColor(otherColourLabel,1,1,1,1)
		ac.setFontColor(otherColourMinus,1,1,1,1)
		ac.setFontColor(otherColourPlus,1,1,1,1)


		#ac.setFontColor(proximityLabel,1,1,1,.2)
		#ac.setFontColor(proxMinus,1,1,1,.2)
		#ac.setFontColor(proxPlus,1,1,1,.2)
		indicatorMode = False

def indicatorFlagClick(name,state):
	global indicatorFlagMode,indicatorFlagSwitch,otherColourLabel,otherColourPlus,otherColourMinus,proximityLabel,proxMinus,proxPlus,flagTypeButton,indicatorWidthButton,indicatorLengthButton,flagTypeSwitch,indicatorMinus,indicatorPlus,indicatorLengthPlus,indicatorLengthMinus
	
	#ac.setBackgroundColor(highPerformanceOn,carColours[5][0],carColours[5][1],carColours[5][2])
	if indicatorFlagMode == False:
		#change it to green
		ac.setBackgroundColor(indicatorFlagSwitch,0,151/255,0)
		ac.setBackgroundOpacity(indicatorFlagSwitch,1)
		
		#grey out other colour selector
		ac.setFontColor(otherColourLabel,1,1,1,0.2)
		ac.setFontColor(otherColourMinus,1,1,1,0.2)
		ac.setFontColor(otherColourPlus,1,1,1,0.2)

		#ac.setFontColor(proximityLabel,1,1,1,1)
		#ac.setFontColor(proxMinus,1,1,1,1)
		#ac.setFontColor(proxPlus,1,1,1,1)

		##make other options to do with this not greyed out
		ac.setFontColor(flagTypeButton,1,1,1,1)
		ac.setFontColor(indicatorWidthButton,1,1,1,1)
		ac.setFontColor(indicatorLengthButton,1,1,1,1)
		ac.setBackgroundOpacity(flagTypeSwitch,1)
		ac.setFontColor(indicatorMinus,1,1,1,1)
		ac.setFontColor(indicatorPlus,1,1,1,1)

		ac.setFontColor(indicatorLengthMinus,1,1,1,1)
		ac.setFontColor(indicatorLengthPlus,1,1,1,1)

		indicatorFlagMode = True

	else:
		ac.setBackgroundColor(indicatorFlagSwitch,189/255,0,0)
		ac.setBackgroundOpacity(indicatorFlagSwitch,1)

		ac.setFontColor(otherColourLabel,1,1,1,1)
		ac.setFontColor(otherColourMinus,1,1,1,1)
		ac.setFontColor(otherColourPlus,1,1,1,1)

		ac.setFontColor(flagTypeButton,1,1,1,0.5)
		ac.setFontColor(indicatorWidthButton,1,1,1,.5)
		ac.setFontColor(indicatorLengthButton,1,1,1,.5)
		ac.setBackgroundOpacity(flagTypeSwitch,0.5)
		ac.setFontColor(indicatorMinus,1,1,1,0.5)
		ac.setFontColor(indicatorPlus,1,1,1,0.5)
		ac.setFontColor(indicatorLengthMinus,1,1,1,0.5)
		ac.setFontColor(indicatorLengthPlus,1,1,1,0.5)
		#ac.setFontColor(proxPlus,1,1,1,.2)
		indicatorFlagMode = False

def blueFlagClick(name,state):
	global blueFlags,blueFlagSwitch

	if(blueFlags == True):
		blueFlags = False
		ac.setBackgroundColor(blueFlagSwitch,1,1,1)
		ac.setBackgroundOpacity(blueFlagSwitch,0.2)		

	else:
		blueFlags = True
		ac.setBackgroundColor(blueFlagSwitch,0.15,0.15,200/255)
		ac.setBackgroundOpacity(blueFlagSwitch,1)		

def flagClickUp(name,state):
	global flagWidth,indicatorFlagMode

	#make button unclickable if mode is off
	if(indicatorFlagMode == False):
		return
	
	if(flagWidth <30):
		flagWidth += 5	

def flagClickDown(name,state):
	global flagWidth,indicatorFlagMode

	if(indicatorFlagMode == False):
		return

	if(flagWidth > 5):
		flagWidth -= 5

def flagLengthClickUp(name,state):
	global flagLength,indicatorFlagMode

	#make button unclickable if mode is off
	if(indicatorFlagMode == False):
		return
	
	if(flagLength < 2):
		flagLength += 0.2	

def flagLengthClickDown(name,state):
	global flagLength,indicatorFlagMode

	if(indicatorFlagMode == False):
		return

	if(flagLength > 0.2):
		flagLength -= 0.2

def proxSolidClick(name,state):
	global proxSolid,flagTypeSwitch,indicatorFlagMode

	#make button unclickable if mode is off
	if(indicatorFlagMode == False):
		return

	if(proxSolid == False):
		proxSolid = True
		ac.setBackgroundColor(flagTypeSwitch,255/255,255/255,51/255)
		ac.setBackgroundOpacity(flagTypeSwitch,.8)		

	else:
		proxSolid = False
		ac.setBackgroundColor(flagTypeSwitch,255/255,128/255,0)
		ac.setBackgroundOpacity(flagTypeSwitch,1)

def backgroundColourClick(name,state):
	global backgroundColourIndex,backgroundColourSwitch,backgroundColourLabel,backgroundTypePlus,backgroundTypeMinus,backgroundColours

	backgroundColourIndex += 1

	if(backgroundColourIndex > len(backgroundColours)): #greater than becaus 0 is off and not in the array of colours
		backgroundColourIndex = 0

	if(backgroundColourIndex == 0):
		#no background, disable other background buttons
		ac.setBackgroundOpacity(backgroundTypePlus,.2)
		#ac.setBackgroundOpacity(backgroundTypeMinus,.2)
		#ac.setBackgroundOpacity(backgroundTypeLabel,.2)
		ac.setFontColor(backgroundTypeMinus,1,1,1,0.2)
		ac.setFontColor(backgroundTypePlus,1,1,1,0.2)

		ac.setFontColor(backgroundTypeLabel,1,1,1,0.2)

		ac.setBackgroundOpacity(backgroundColourSwitch,.2)
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[0][0],backgroundColours[0][1],backgroundColours[0][2])

	elif (backgroundColourIndex == 1):
		#ac.setBackgroundOpacity(backgroundTypePlus,1)
		#ac.setBackgroundOpacity(backgroundTypeMinus,1)
		ac.setFontColor(backgroundTypeMinus,1,1,1,1)
		ac.setFontColor(backgroundTypePlus,1,1,1,1)
		#ac.setBackgroundOpacity(backgroundTypeLabel,1)
		ac.setFontColor(backgroundTypeLabel,1,1,1,1)

		ac.setBackgroundOpacity(backgroundColourSwitch,1)
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[0][0],backgroundColours[0][1],backgroundColours[0][2])

	elif (backgroundColourIndex == 2):
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[1][0],backgroundColours[1][1],backgroundColours[1][2])		

	elif (backgroundColourIndex == 3):
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[2][0],backgroundColours[2][1],backgroundColours[2][2])		

	elif (backgroundColourIndex == 4):
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[3][0],backgroundColours[3][1],backgroundColours[3][2])

	elif (backgroundColourIndex == 5):	
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[4][0],backgroundColours[4][1],backgroundColours[4][2])

	elif (backgroundColourIndex == 6):	
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[5][0],backgroundColours[5][1],backgroundColours[5][2])

	elif (backgroundColourIndex == 7):	
		ac.setBackgroundColor(backgroundColourSwitch,backgroundColours[6][0],backgroundColours[6][1],backgroundColours[6][2])

def backgroundTypeMinusClick(name,state):
	global backgroundShape,backgroundColourIndex

	if(backgroundColourIndex == 0):
		return

	backgroundShape -= 1

	if(backgroundShape < 0):
		backgroundShape = 0

def backgroundTypePlusClick(name,state):
	global backgroundShape,backgroundColourIndex

	if(backgroundColourIndex == 0):
		return

	backgroundShape += 1

	if(backgroundShape > 2):
		backgroundShape = 2

def drawBorder(radius):
	global appWindow,title,windowWidth
	#Rotate a point counterclockwise by a given angle around a given origin.
	#The angle should be given in radians.
	#centre of app window
	#ox, oy = origin
	ox = windowWidth/2
	oy = windowWidth/2

	#1stpoint is (0,0)
	px = (windowWidth/2)*radius
	py = 0

	detail = 32

	points = []
	for i in range(0,detail): #exclusive of top number
		#topleft to bottom left
		
		#degrees
		degrees = 0

		if i!=0:
			fraction = 360 / detail
			degrees = fraction * i
		#radians
		#ac.log(str(degrees) + ' degrees')
		angle = math.radians(degrees)
		#ac.log(str(angle) + ' rads')
		

		qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
		qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

		#ac.glVertex2f(qx,qy)
		#ac.glVertex2f(windowWidth/2,windowWidth/2)
		points.append((qx,qy))

	alpha = 1-(radius/10)
	
	ac.glColor4f(1,1,1,alpha)
	#o for lines
	
	#draw circle
	for i in range(0,detail -1):
		#open and close gl everytime, limit of ten points in one call?
		ac.glBegin(1)

		ac.glVertex2f(points[i][0],points[i][1])
		ac.glVertex2f(points[i+1][0],points[i+1][1])
		ac.glEnd()

	ac.glBegin(1)
	ac.glVertex2f(points[len(points)-1][0],points[len(points)-1][1])
	ac.glVertex2f(points[0][0],points[0][1])
	ac.glEnd()
	radius += 0.05

	return radius

def drawBackground(alpha):
	global scale,overallOpacity,backgroundType,backgroundOutline,backgroundColourIndex,backgroundColours,backgroundShape,configWindowOpen,backgroundSize,backgroundMaxOpacity

	if(backgroundColourIndex == 0):
		return
	#no point in continuing, it won't be seen anyway with alpha at 0
	if(alpha == 0 and configWindowOpen == False):
		return

	backgroundType = backgroundShape
	backgroundOutline = True
	#user can choose shape type? circle, hex, or square?
	
	if(backgroundType == 0):
		sides = 6
	elif(backgroundType == 1):
		sides = 4
	elif(backgroundType == 2):
		sides = 4

	
	split = True
	splits = 1 ##started to try and split it up to make it look like a chequered flag or rings but performance was way too bad

	#create unit vector, multiply by size and then rotate by 360 degrees divided by sides until complete
	unitVectorX = 0
	unitVectorY = 1

	startPos = (windowWidth/2,windowWidth/2)

	thisAlpha = backgroundMaxOpacity * overallOpacity * alpha#add opacity setting?
	#edgeAlpha = .9 * overallOpacity * alpha

	if (configWindowOpen):
		thisAlpha = backgroundMaxOpacity*overallOpacity

	j = 0
	x = 1
	#array/list for rendering for each ring
	points = []
	while j < backgroundSize:

		ring = []
		
		i = 0
		while i <= 360:
			#if user wants square (not spun) we need to use this variable to spin it round
			spinAmount = 0
			if(backgroundType == 2):
				spinAmount =45
			#do the maths to rotate the unit vector arm by degrees (i)
			ca = math.cos(math.radians(i + spinAmount))
			sa = math.sin(math.radians(i + spinAmount))
			
			rX = (ca * unitVectorX - sa * unitVectorY)
			rY = (sa * unitVectorX + ca * unitVectorY)
			
			startDistance = 0#(j- (1 - j*0.5)) *(scale)
			endDistance = startDistance + (backgroundSize/splits)*scale

			nearest = (startPos[0] + (rX*startDistance),startPos[1] + (rY*startDistance))
			furthest = (startPos[0] + (rX*endDistance),startPos[1] + (rY*endDistance))

			#add to list for triangles/renderinf
			ring.append((nearest[0],nearest[1]))
			ring.append((furthest[0],furthest[1]))

			i+=360/sides

		points.append(ring)

		j+= (backgroundSize/splits)
		
		
	for j in range(0,len(points)):
		ring = points[j]
		for i in range(0,len(ring)-3,2):
			
			#there is a nicer way to do this im sure
			if(backgroundColourIndex == 0):
				r = backgroundColours[0][0]
				g = backgroundColours[0][1]
				b = backgroundColours[0][2]

			elif(backgroundColourIndex == 1):
				r = backgroundColours[0][0]
				g = backgroundColours[0][1]
				b = backgroundColours[0][2]

			elif(backgroundColourIndex == 2):
				r = backgroundColours[1][0]
				g = backgroundColours[1][1]
				b = backgroundColours[1][2]

			elif(backgroundColourIndex == 3):
				r = backgroundColours[2][0]
				g = backgroundColours[2][1]
				b = backgroundColours[2][2]

			elif(backgroundColourIndex == 4):
				r = backgroundColours[3][0]
				g = backgroundColours[3][1]
				b = backgroundColours[3][2]

			elif(backgroundColourIndex == 5):
				r = backgroundColours[4][0]
				g = backgroundColours[4][1]
				b = backgroundColours[4][2]

			elif(backgroundColourIndex == 6):
				r = backgroundColours[5][0]
				g = backgroundColours[5][1]
				b = backgroundColours[5][2]

			elif(backgroundColourIndex == 7):
				r = backgroundColours[6][0]
				g = backgroundColours[6][1]
				b = backgroundColours[6][2]

			triangles = True

			if triangles:
				ac.glBegin(2)
				ac.glColor4f(r,g,b,thisAlpha)
				ac.glVertex2f(ring[i+1][0],ring[i+1][1])
				ac.glVertex2f(ring[i][0],ring[i][1])
				ac.glVertex2f(ring[i+2][0],ring[i+2][1])		
						
				ac.glVertex2f(ring[i+1][0],ring[i+1][1])
				ac.glVertex2f(ring[i+2][0],ring[i+2][1])
				ac.glVertex2f(ring[i+3][0],ring[i+3][1])
				
				ac.glEnd()


			if backgroundOutline:

				if(backgroundColourIndex == 0):
					r = backgroundColours[0][0]
					g = backgroundColours[0][1]
					b = backgroundColours[0][2]

				elif(backgroundColourIndex == 1):
					r = backgroundColours[6][0]
					g = backgroundColours[6][1]
					b = backgroundColours[6][2]

				elif(backgroundColourIndex == 2):
					r = backgroundColours[5][0]
					g = backgroundColours[5][1]
					b = backgroundColours[5][2]

				elif(backgroundColourIndex == 3):
					r = backgroundColours[4][0]
					g = backgroundColours[4][1]
					b = backgroundColours[4][2]

				elif(backgroundColourIndex == 4):
					r = backgroundColours[3][0]
					g = backgroundColours[3][1]
					b = backgroundColours[3][2]

				elif(backgroundColourIndex == 5):
					r = backgroundColours[2][0]
					g = backgroundColours[2][1]
					b = backgroundColours[2][2]

				elif(backgroundColourIndex == 6):
					r = backgroundColours[1][0]
					g = backgroundColours[1][1]
					b = backgroundColours[1][2]

				elif(backgroundColourIndex == 7):
					r = backgroundColours[0][0]
					g = backgroundColours[0][1]
					b = backgroundColours[0][2]

				ac.glBegin(0)

				ac.glColor4f(r,g,b,thisAlpha)
				##ac.glVertex2f(ring[i][0],ring[i][1])
				##ac.glColor4f(r,g,b,edgeAlpha)
				##ac.glVertex2f(ring[i+1][0],ring[i+1][1])

				ac.glVertex2f(ring[i+1][0],ring[i+1][1])
				ac.glVertex2f(ring[i+3][0],ring[i+3][1])

				#ac.glVertex2f(ring[i][0],ring[i][1])
				#ac.glVertex2f(ring[i+2][0],ring[i+2][1])

				ac.glEnd()

def drawConfig():
	global configButton,retractConfigButton,extendConfigButton,configSizeCurrent,configSizeSmall,configSizeLarge,scaleButtons,windowWidth,drop,cogRotation,border,configWindowOpen,background,carAura,angleOfInfluence,scale,carAuraTarget,lowerCarAura,raiseCarAura,raiseAngle,lowerAngle,angleTarget,overallOpacity,rearCutOffDistance

	

	#spin cog if clicked
	if configSizeCurrent > 0:	
		#always make button visible if window is open
		ac.setVisible(configButton,1)
		configWindowOpen = True
		if(cogRotation==360):
			cogRotation = 0
		cogRotation+=0.5
	else:
		configWindowOpen = False		
		if not border:
			#if border isnt active and we have closed the window, hide clickable button
			ac.setVisible(configButton,0)
			#get outta here!
			return

	##ac.console(str("here"))
	#always make button clickable if border is being anmimated - radar blip
	#if border:
	#	ac.setVisible(configButton,1)

	#####UI
	#quad
	
	buttonSize = 50
	topBorder = 00	
	animationSpeed = 10
	if extendConfigButton:		
		if configSizeCurrent < configSizeLarge:
			configSizeCurrent += animationSpeed
			#ac.setSize(configButton,configSizeCurrent,configSizeCurrent)
			#move label along with window			
			x = windowWidth + configSizeCurrent
			y = topBorder
			ac.setPosition(configButton,x,y)
			
		if configSizeCurrent == configSizeLarge:
			extendConfigButton = False
			#show buttons
			for button in scaleButtons:
				ac.setVisible(button,1)



	if retractConfigButton:
		#remove buttons as soon as pressed
		for button in scaleButtons:
				ac.setVisible(button,0)

		if configSizeCurrent > 0:
			configSizeCurrent -= animationSpeed
			x = windowWidth + configSizeCurrent
			y = topBorder
			ac.setPosition(configButton,x,y)
			#ac.setSize(configButton,configSizeCurrent,configSizeCurrent)
		if configSizeCurrent == 0:
			drop = 0
			retractConfigButton = False

	#adjust drop	
	#ac.console(str(drop))
	if configSizeCurrent == configSizeLarge:
		if drop < 350:
			#if 50, set next buttons to show
			#if 100, set next buttons to show,etc
			#figure out animation on the way back up? -when to remove text, might be ok, just magickin it away -- do cog, spin on activate
			drop += animationSpeed


	#background
	x = configSizeCurrent
	y = topBorder + drop + buttonSize
	ac.setSize(background,x,y)

	#config icon box
	#tris	
	alpha = (configSizeCurrent/windowWidth)
	
	##overallOpacity#not using for settings panel
	##alpha -= 1 - overallOpacity

	##ac.setBackgroundOpacity(background,alpha)
	
	
	ac.glBegin(2)
	ac.glColor4f(189/255,0,0,alpha)
	#top left	
	ac.glVertex2f(windowWidth + configSizeCurrent,topBorder)
	#bottomleft
	ac.glVertex2f(windowWidth + configSizeCurrent,buttonSize + topBorder)
	#bottom right
	ac.glVertex2f(windowWidth + buttonSize + configSizeCurrent, buttonSize + topBorder)

	#bottom right
	ac.glVertex2f(windowWidth + buttonSize + configSizeCurrent,buttonSize + topBorder)
	#top right	
	ac.glVertex2f(windowWidth + buttonSize + configSizeCurrent,topBorder)
	#top left	
	ac.glVertex2f(windowWidth + configSizeCurrent,topBorder)
	ac.glEnd()
	#border for config icon box
	ac.glBegin(0)
	ac.glColor4f(1,1,1,alpha)
	#top left	
	ac.glVertex2f(windowWidth + configSizeCurrent,topBorder)
	#bottomleft
	ac.glVertex2f(windowWidth + configSizeCurrent,buttonSize + topBorder)

	#bottomleft
	ac.glVertex2f(windowWidth + configSizeCurrent,buttonSize + topBorder)
	#bottom right
	ac.glVertex2f(windowWidth + buttonSize + configSizeCurrent, buttonSize + topBorder)

	#bottom right
	ac.glVertex2f(windowWidth + buttonSize + configSizeCurrent,buttonSize + topBorder)
	#top right	
	ac.glVertex2f(windowWidth + buttonSize + configSizeCurrent,topBorder)
	#top right	
	ac.glVertex2f(windowWidth + buttonSize + configSizeCurrent,topBorder)
	#top left	
	ac.glVertex2f(windowWidth + configSizeCurrent,topBorder)	
	ac.glEnd()

	#border				
	ac.glBegin(0)
	ac.glColor4f(1,1,1,alpha)
	
	#topright
	ac.glVertex2f(windowWidth + configSizeCurrent,topBorder)
	#topleft
	ac.glVertex2f(windowWidth,topBorder)

	#topleft
	ac.glVertex2f(windowWidth,topBorder)
	#bottomleft
	ac.glVertex2f(windowWidth,buttonSize + topBorder + drop)

	#bottomleft
	ac.glVertex2f(windowWidth,buttonSize + topBorder + drop)	
	#bottom right
	ac.glVertex2f(windowWidth + configSizeCurrent,buttonSize + topBorder + drop)	

	#bottom right
	ac.glVertex2f(windowWidth + configSizeCurrent,buttonSize + topBorder + drop)		
	#topright
	ac.glVertex2f(windowWidth + configSizeCurrent,topBorder)

	#header box bottom line
	#bottomleft
	#ac.glVertex2f(windowWidth ,buttonSize + topBorder)
	#bottom right
	#ac.glVertex2f(windowWidth + configSizeCurrent,buttonSize + topBorder)
	ac.glEnd()	
	#1stpoint is (0,0)
	detail = 10
	points = []
	
	#cog
	ox = 0
	oy = 0
	#normalized vector
	px = 1
	py = 0

	insideCogLength = buttonSize*0.5*0.5
	insideCogWidth = detail*0.4
	outsideCogLength = buttonSize*0.75*0.5
	outsideCogWidth = detail*0.25

	holeSize = buttonSize*0.25*0.5
	#build the teeth of the gear
	if border:
		alpha = 1

	

	outline = []

	for i in range(0,detail): #exclusive of top number
		#degrees
		degrees = 0

		#if i!=0:
		fraction = 360 / detail
		degrees = fraction * i
		degrees += cogRotation
		angle = math.radians(degrees)
		#rotate arm
		qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
		qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
		#now rotate 90 degrees
		#The right-hand normal of vector (x, y) is (y, -x), and the left-hand normal is (-y, x)
		rightHandNormal = (qy,-qx)
		leftHandNormal = (-qy,qx)

		#multiply by length and add sidways direction (normal)

		#inside
		aX = qx*insideCogLength + (leftHandNormal[0]*insideCogWidth)
		aY = qy*insideCogLength + (leftHandNormal[1]*insideCogWidth)

		bX = qx*insideCogLength + (rightHandNormal[0]*insideCogWidth)
		bY = qy*insideCogLength + (rightHandNormal[1]*insideCogWidth)

		#outside

		aX2 = qx*outsideCogLength + (leftHandNormal[0]*outsideCogWidth)
		aY2 = qy*outsideCogLength + (leftHandNormal[1]*outsideCogWidth)

		bX2 = qx*outsideCogLength + (rightHandNormal[0]*outsideCogWidth)
		bY2 = qy*outsideCogLength + (rightHandNormal[1]*outsideCogWidth)

		##add button location to points
		aX += windowWidth + buttonSize*0.5 + configSizeCurrent
		aY += buttonSize*0.5
		bX += windowWidth+ buttonSize*0.5 + configSizeCurrent
		bY += buttonSize*0.5

		aX2 += windowWidth+ buttonSize*0.5+ configSizeCurrent
		aY2 += buttonSize*0.5

		bX2 += windowWidth+ buttonSize*0.5+ configSizeCurrent
		bY2 += buttonSize*0.5
		
		ac.glColor4f(1,1,1,alpha)
		ac.glBegin(2)
		#bottom left
		ac.glVertex2f(bX,bY)
		#bottom right
		ac.glVertex2f(aX,aY)
		#top right		
		ac.glVertex2f(bX2,bY2)

		#2nd tri
		#top right
		ac.glVertex2f(bX2,bY2)
		#bottom left
		ac.glVertex2f(aX,aY)
		#bottom right
		ac.glVertex2f(aX2,aY2)	
		ac.glEnd()

		#save for outline points
		outline.append((aX,aY))
		outline.append((aX2,aY2))

		outline.append((aX2,aY2))
		outline.append((bX2,bY2))

		outline.append((bX2,bY2))
		outline.append((bX,bY))
	
	#build the innder circle of the gear
	circlePoints = []
	for i in range(0,detail): #exclusive of top number
		#degrees
		degrees = 0

		if i!=0:
			fraction = 360 / detail
			degrees = fraction * i
		angle = math.radians(degrees)
		#rotate arm
		qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
		qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

		
		innerX = qx* holeSize + buttonSize*0.5 + windowWidth + configSizeCurrent
		innerY = qy* holeSize + buttonSize*0.5


		outerX = qx* (insideCogLength+2) + windowWidth + buttonSize*0.5 + configSizeCurrent #+2 is to make sure circle overlaps and space at edge of teeth (because i havent rotated this circle by half gear tooth)
		outerY = qy * (insideCogLength+2) + buttonSize*0.5

		circlePoints.append((innerX,innerY))
		circlePoints.append((outerX,outerY))


	#triangulate inner points
	circlePointsLength = len(circlePoints)
	#add start to end to make a loop for easy triangulating
	circlePoints.append(circlePoints[0])
	circlePoints.append(circlePoints[1])

	
	
	for i in range(0,circlePointsLength,2):
		
		ac.glColor4f(1,1,1,alpha)
		ac.glBegin(2)
		#perhaps this seems a bit wonky, but is due to our rotation working in an anti clockwise direction
		
		ac.glVertex2f(circlePoints[i][0],circlePoints[i][1])		
		ac.glVertex2f(circlePoints[i+3][0],circlePoints[i+3][1])
		ac.glVertex2f(circlePoints[i+1][0],circlePoints[i+1][1])
		#2nd tri
		#bottom left
		ac.glVertex2f(circlePoints[i][0],circlePoints[i][1])
		ac.glVertex2f(circlePoints[i+2][0],circlePoints[i+2][1])
		ac.glVertex2f(circlePoints[i+3][0],circlePoints[i+3][1])
		
		ac.glEnd()
	#ac.glEnd()

	outlineLength = len(outline)
	for i in range(0,outlineLength-1,2):
		ac.glColor4f(0,0,0,alpha)
		ac.glBegin(0)
		ac.glVertex2f(outline[i][0],outline[i][1])
		ac.glVertex2f(outline[i+1][0],outline[i+1][1])
		ac.glEnd()


	for i in range(0,circlePointsLength-2,2):
		ac.glColor4f(0,0,0,alpha)
		ac.glBegin(0)
		ac.glVertex2f(circlePoints[i][0],circlePoints[i][1])
		ac.glVertex2f(circlePoints[i+2][0],circlePoints[i+2][1])
		ac.glEnd()

	
	#range circle
	#not entirely accurate on alpha levels, but gives a decent indication of the size of the area being shown
	if(configWindowOpen):
		#animation
		auraAnimationSpeed = 0.2
		if(raiseCarAura and carAura < carAuraTarget):
			carAura += auraAnimationSpeed

		if(lowerCarAura and carAura > carAuraTarget):
			carAura -= auraAnimationSpeed

		if(carAura == carAuraTarget):
			raiseCarAura = False
			lowerCarAura = False

		angleAnimationSpeed = 0.5
		#vars kinda wrong here, swapped the buttons round
		if(raiseAngle and angleOfInfluence > angleTarget):
			angleOfInfluence -= angleAnimationSpeed

		if(lowerAngle and angleOfInfluence < angleTarget):
			angleOfInfluence += angleAnimationSpeed

		if(angleOfInfluence == angleTarget):
			raiseAngle = False
			lowerAngle = False

		gridSize = 50

		
		for j in range(0,5):
			#detail = 90#24*2 # because user can increment by 15 - 360/15 =24 --- *** now at 180 so i can do a smooth animation - this is overkill on how many tris are being rendered - but unless i change the method to have steps of the circle, plus one rotated arm, it will have to do - did this
			rangePoints = []
			counter = 0
			detail = 10
			#start at half way up until the angle chose by user
			for degrees in range(180,360-int(angleOfInfluence/2),10): #15 is step of button. should make global var
				
				counter += 10
				#degrees
				#degrees = 0 

				#if i!=0:
				#	fraction = 360 / detail
				#	degrees = fraction * i
				#check if degrees is within the range, angleof influence global var
				#if(degrees < 180 or ( degrees + 360/detail > 360 - (angleOfInfluence/2) ) ):
				#	continue

				#if degrees + 360/10 > 360 - (angleOfInfluence/2):
				#	continue

				angle = math.radians(degrees-90)
				#rotate arm
				qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
				qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

				innerCircleSize = scale*j*(carAura/5) #this is the part that is just judged-size wise

				innerX = (qx * innerCircleSize) + windowWidth/2
				innerY = (qy * innerCircleSize) + windowWidth/2

				outerCircleSize = scale*(j+1)*(carAura/5)#2 + j*gridSize*carAura

				outerX = (qx * outerCircleSize) + windowWidth/2
				outerY = (qy * outerCircleSize) + windowWidth/2
				
				#force first alpha to be invisible so we have an empty circle round player car - forced to do this so circle doesn't overlap config options
				#labels and buttons are drawn first it seems, anything i call here overlaps them, looks like a cool 'design' anyway - don't tell anyone :p
				alpha = 1- 1
				if j> 0:
					alpha =1 - (j)/10

					##overall opacity
				alpha -= 1 - overallOpacity

				rangePoints.append((innerX,innerY,degrees,alpha))
				rangePoints.append((outerX,outerY,degrees,alpha))

			#check to see if there is any angle left over, w have been building in steps - create final arm
			if 360-(angleOfInfluence/2) > counter:
				degrees = 360 - angleOfInfluence/2
				#we have some left over to draw
				angle = math.radians(degrees-90)
				#rotate arm
				qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
				qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

				innerCircleSize = scale*j*(carAura/5)

				innerX = (qx * innerCircleSize) + windowWidth/2
				innerY = (qy * innerCircleSize) + windowWidth/2

				outerCircleSize = scale*(j+1)*(carAura/5)

				outerX = (qx * outerCircleSize) + windowWidth/2
				outerY = (qy * outerCircleSize) + windowWidth/2
				
				#force first alpha to be invisible so we have an empty circle round player car - forced to do this so circle doesn't overlap config options
				#labels and buttons are drawn first it seems, anything i call here overlaps them, looks like a cool 'design' anyway - don't tell anyone :p
				alpha = 1 - 1
				if j > 0:
					alpha =1 - (j)/10

				##overall opacity
				alpha -= 1 - overallOpacity

				rangePoints.append((innerX,innerY,degrees,alpha))
				rangePoints.append((outerX,outerY,degrees,alpha))

			#loop list
			#rangePoints.append(rangePoints[0])
			#rangePoints.append(rangePoints[1])

			j = 5
			for i in range(0,len(rangePoints)-2,2):

				if i != 0:
					#every time we go round a circle, add to j
					if i == detail*2: 
						j += 1

				# ac.console(str(rangePoints[i][1]))
				degrees = rangePoints[i][2]
				
				

				alpha = rangePoints[i][3]
				ac.glColor4f(0,133/255,133/255,alpha)
				
				ac.glBegin(2)
				#if(rangePoints[i][0] > 101):
				#	ac.glColor4f(0,133/255,133/255,0.0) #remove above? - overlapping config options if i leave on

				ac.glVertex2f(rangePoints[i][0],rangePoints[i][1])
				ac.glVertex2f(rangePoints[i+2][0],rangePoints[i+2][1])
				ac.glVertex2f(rangePoints[i+1][0],rangePoints[i+1][1])
				
				ac.glVertex2f(rangePoints[i+2][0],rangePoints[i+2][1])
				ac.glVertex2f(rangePoints[i+3][0],rangePoints[i+3][1])
				ac.glVertex2f(rangePoints[i+1][0],rangePoints[i+1][1])

				ac.glEnd()
	#stuff being drawn but hidden with alpha?

	#rear cut visual
	if(configWindowOpen):
		ac.glColor4f(189/255,0,0,1)
		x = windowWidth*.5 -(scale*5 * (carAura/5))*1
		y = windowWidth*.5 + scale*5 * (carAura/5) -( rearCutOffDistance * scale) + scale*2 # + scale for spacer
		width =  (scale*5 * (carAura/5)) + scale
		height= scale *1

		ac.glQuad(x,y,width,height)

	

def buildCarList():

	global tempCarList,carTypes

	#ac.log("Building Car List")

	# we use two lists, one that is currently being rendered carList, and aone which is being analysed to see if we ahve all data available - tempCarList
	#if buildCarList() is called (this function) - then we have been told to create a new templist, once this templist  have finished analysing, it will be copied to main CarList for rendering
	#clear temp list
	tempCarList = []

	#build car list - get amount of cars in session
	carAmount = ac.getCarsCount()

	#iterate through these cars
	for carId in range(0, carAmount):
		#ac.log("Build List - " + str(carId))
		#model type
		carType = str(ac.getCarName(carId))

		#check to see if we have data for this car
		readFromFile = True
		for i in range(0,len(carTypes)):
				if carType == carTypes[i].carType:
					#ac.log("Build Car List - reading from carTypes list - 229 "+ str(carType) + " - Cartype" + str(carId) + " - ID")
					#great!, we have already worked this info out, enter it in to our temp list
					#clear distance - we will work out each car's distance below, we are just importing a template here
					#distance = 0
					tempCarList.append(CarAndInfo(carId,carType,carTypes[i].distance,carTypes[i].vertices,carTypes[i].rectangleVertices,carTypes[i].faces,carTypes[i].normals,carTypes[i].boundary,carTypes[i].boundarySimple,carTypes[i].radsToPlayer,carTypes[i].alpha,carTypes[i].blueCounter,carTypes[i].makeBlue,carTypes[i].offset))
					#once we are out this loop, tell loop to move to next car
					readFromFile = False
					#break
					
		if readFromFile == False:
			#we have the info, skip the rest, we can now just check next car		
			continue

		#if we have not entered data in to our variable, look to see if file is in my documents
		#get user directory
		homeDirectory = os.path.expanduser("~")
		path = os.path.join(homeDirectory,"Documents","Assetto Corsa","apps","carRadar",carType)#,"carInfo.txt")
		
		#check if car data already exists		
		if os.path.exists(path):
			#good, read the info from file in my docs
			#ac.log("Build Car List - reading from My Docs - 253 "+ str(carType) + " - Cartype" + str(carId) + " - ID")			
			distance = 0
			vertices = getVerticesFromFile(os.path.join(path,'vertices.txt'))
			rectangleVertices = []
			faces = getFacesFromFile(os.path.join(path,'faces.txt'))
			normals = getNormalsFromFile(os.path.join(path,'normals.txt'))
			#will work out later
			boundary = []
			boundarySimple = []
			radsToPlayer = 0
			alpha = 0
			blueCounter = 0
			makeBlue = False
			offset = ()
			tempCarList.append(CarAndInfo(carId,carType,distance,vertices,rectangleVertices,faces,normals,boundary,boundarySimple,radsToPlayer,alpha,blueCounter,makeBlue,offset))
			#add this to the global variable to minimise reading from HDD - carTypes list keeps hold of any car that has been in the session
			#next time it tries to get info for this car, it can read from the variable instead of hdd
			#do not need duplicates
			if carType not in carTypes:				
				carTypes.append(CarAndInfo(carId,carType,distance,vertices,rectangleVertices,faces,normals,boundary,boundarySimple,radsToPlayer,alpha,blueCounter,makeBlue,offset))

			continue


		#if we get here,we need to look at model info and compute vertices etc
		#if we enter 0 data in to our car info list, Update() will send this car type to be analysed
		#doing it this way allows Update() to keep trying until converter info is available
		#ac.log("No data available, entering empty - 272 "+ str(carType) + " - Cartype" + str(carId) + " - ID")
		distance = 0
		vertices = []
		rectangleVertices = []
		faces = []
		normals = []
		boundary = []
		boundarySimple = []
		radsToPlayer = 0
		alpha = 0
		blueCounter = 0
		makeBlue = False
		offset = ()
		tempCarList.append(CarAndInfo(carId,carType,distance,vertices,rectangleVertices,faces,normals,boundary,boundarySimple,radsToPlayer,alpha,blueCounter,makeBlue,offset))

def goGoCarRadar(deltaT):
	global carList,tempCarList,appWindow,elapsed,timeStart,appWindow,filesToRemove,border,borderRadius,converterAvailable,carTypesToConvert,converterWait,converterWaitCount,drawPlayerCar,drawOutlineOfCars,drawMeshOfCars,configWindowOpen,indicatorFlagMode,drawRadarBackground
	
	ac.setBackgroundOpacity(appWindow, 0)

	drawConfig()
	#ac.log(str(time.clock()) + 'clock')

	secondsToHide = 2
	### app title hide
	if timeStart != 0:
		t = time.clock() - timeStart
		#ac.console(str(t) + ' time - start')
		if(t > secondsToHide):
			ac.setTitle(appWindow,"")
			#reset timer
			timeStart = 0
			#draw border
			border = False			
			#reset border size
			borderRadius = 0
			#when border is not active, hide clickable config button
			ac.setVisible(configButton,0)
	if border == True:
		borderRadius = drawBorder(borderRadius)


	#########################################################REMOVE?
	##can change to using time.clock if we want
	elapsed += 1
	#ac.log(str(elapsed))
	#around every 30 seconds, rebuild car list - causing a cpu spike atm
	if elapsed == 1000: #5000 5000 is around 30 seconds - 200 is every 2 seconds or so.. extreme test! -seems happy
		#buildCarList()
		elapsed = 0

	#if waiting converter, keep track since we started waiting on it - flags set inside loop below
	if converterWait == True:
		converterWaitCount += 1

	#check if car info is available, if not, compute
	for car in tempCarList:
		#if vertices length is zero, it means we haven't figured out anything yet
		l = len(car.vertices)
		if l == 0:
			#ac.log("Working on "+ str(car.carType) + " - Cartype" + str(car.carId) + " - ID")
			#check to see if we have data for this car
			readFromFile = True
			for i in range(0,len(carTypes)):
					if car.carType == carTypes[i].carType:
						#ac.log("Update - reading from carTypes list - 229 "+ str(car.carType) + " - Cartype" + str(car.carId) + " - ID")
						#great!, we have already worked this info out, enter it in to our temp list						
						car.vertices = carTypes[i].vertices
						car.faces = carTypes[i].faces
						car.normals = carTypes[i].normals
						#once we are out this loop, tell loop to move to next car
						readFromFile = False
						#break - crashes if try to leave loop early? Only a tiny optimisation i was trying 
						
			if readFromFile == False:
				#we have the info, skip, we can check next car
				#ac.log("Update - moving to next car")
				continue

			#first check if we have computed the data for this car before	- saved to My Docs		
			dataAvailable = False

			#get user directory			
			homeDirectory = os.path.expanduser("~")
			carTypeDir = os.path.join(homeDirectory,"Documents","Assetto Corsa","apps","carRadar",car.carType)
			#check if we have dropped file before
			filename = 'vertices.txt'
			carInfoFile = os.path.join(carTypeDir, filename)
			
			#check if info file exists
			dataAvailable = os.path.isfile(carInfoFile)
			
			if dataAvailable:
				#ac.log("reading from file in update - 330 "+ str(car.carType) + " - Cartype" + str(car.carId) + " - ID")
				#if available, read the files and enter data in to carList - never gets here?
				car.distance = 0 # computed later
				car.vertices = getVerticesFromFile(os.path.join(carTypeDir,'vertices.txt'))
				car.rectangleVertices = []
				car.faces = getFacesFromFile(os.path.join(carTypeDir,'faces.txt'))
				car.normals = getNormalsFromFile(os.path.join(carTypeDir,'normals.txt'))
				car.boundary = []
				car.alpha = 0	
				car.blueCounter = 0
				car.makeBlue = False
				car.offset = ()
				#fill in car types list so next time a car/player wants to use this model's data, we can just check the variable instead of reading from hdd everytime
				if(car not in carTypes):
					carTypes.append(CarAndInfo(car.carId,car.carType,car.distance,car.vertices,car.rectangleVertices,car.faces,car.normals,car.boundary,car.boundarySimple,car.radsToPlayer,car.alpha,car.blueCounter,car.makeBlue,car.offset))
				#we are finished with this car, skip to next
				continue

			if not dataAvailable:
				#if there is no file written, it means we need to do some hard labour

				#we only need to run the converter once for each car type
				#create a list of unique car types for the converter to ..convert
				#adding to a list so we can work through it at our leisure
				#do not add duplicates
				if car.carType not in carTypesToConvert:
					#ac.log("adding to carTypesToConvertList "+ str(car.carType) + " - Cartype" + str(car.carId) + " - ID")
					carTypesToConvert.append(car.carType)
					#there is no way the converter can complete its task by the next line below - so we can skip to the next car/update
					continue

				#if we get here it means the car type has been sent off for conversion - check if it is complete
				#the only way I can think of checking this is if the file has been dropped by the converter yet - performance seems ok
				
				objFileLocation = 'content/cars/'+ car.carType + '/collider.obj'
				completed = os.path.isfile(objFileLocation)

				if not completed:
					#wait for next frame - A little patience
					#ac.log("file not ready, continuing - line 361 "+ str(car.carType) + " - Cartype" + str(car.carId) + " - ID")
					continue

				#if we are here it means the file has been completed! Let's take what we need from it and leave
				#ac.log("here")
				if completed:

					#Let file finish writing, trying to access too early can cause crash					
					if converterWaitCount <= 10:
						#start wait
						converterWait = True
						#ac.log(str(converterWaitCount) + " converterWait Count")
						#this will make counter +1 every frame/update					
						#and wait 
						continue
					elif converterWaitCount > 10:
						#reset
						converterWait = False
						converterWaitCount = 0

					#and proceed below



					#ac.log("data completed-gathering from .obj")
					#parse text in obj file
					objFile = open(objFileLocation,"r")
					text = objFile.readlines()


					#create a list to add co-ords to
					points = []
					#read file - obj store vertices after a 'v' prefix e.g v -0.6598932 0.4230636 0.188266
					for line in text:
						if line.startswith('v '): #note v and then a space - we don't want 'vn' getting involved from the file
						#split in to x,y,z - will still have v prefix
						# use a space to split (" ")
							lineList = line.split(" ")                    
							#remove the "v"
							del lineList[0]
							#the [z] element has \n at the end of the line, (a new line symbol) -remove ('\n' is treated as one character)
							#remove last character from string
							lineList[2] = lineList[2][:-1]												
							#convert to a string
							string =  ' '.join(lineList)
							#add this list, to a list
							points.append(string)					
					

					#save info to a file, so we don't need to run these calculations for each car of this type
					#we just read the file next time
					#ac.log("Checking car type dir exists")
					if not os.path.exists(carTypeDir):
						#ac.log("Making Car type Dir")
						os.makedirs(carTypeDir)



					#save these vertices to a file - planning to use them to render collider on map	
					filename = "vertices.txt"
					dirAndFilename = os.path.join(carTypeDir, filename)
					#ac.log(dirAndFilename)

					#ac.log("writing vertices file")
					#write to file and to list at the same time
					vertices = []
					verticesFile = open(dirAndFilename, "w")
					for p in points:
					    #force a new line each time - having to add \n here, 				    
						verticesFile.write(str(p)+"\n")
						vertices.append(p)
					verticesFile.close()

					#write faces file - the way i write these files could be a little more standardised, but it is working, and parsing files wasn't something I just learned with any great gusto
					#ac.log("writing faces file")
					#objFile = open(file,"r")
					#text = f.readlines()
					#create a list to add co-ords to
					faces = []
					#and a file to save to 
					filename = "faces.txt"
					dirAndFilename = os.path.join(carTypeDir, filename)
					facesFile = open(dirAndFilename, "w")
					#read file - obj store vertices after a 'v' prefix e.g v -0.6598932 0.4230636 0.188266
					for line in text:
						if line.startswith('f '):
					#split in to x,y,z - will still have v prefix
					# use a space to split (" ")
							lineList = line.split(" ")														
							#grab characters until we hit a '/'', and then just the first number before the split, data = 1/1/1, out = 1
							x= lineList[1].split('/')[0]
							y= lineList[2].split('/')[0]
							z= lineList[3].split('/')[0]
							#convert to a string
							face = (x,y,z)
							#add this list, to a list
							faces.append(face)
							#write to file
							facesFile.write(x + ' ' + y + ' ' + z +"\n")
				    #stop writing
					facesFile.close()

					#write normals file - used to decide if we ned to render triangle
					#ac.log("writing normals file")
					#f = open(file,"r")
					#text = f.readlines()
					#create a list to add co-ords to
					normals = []
					#and a file to save to 
					filename = "normals.txt"
					dirAndFilename = os.path.join(carTypeDir, filename)
					normalsFile = open(dirAndFilename, "w")
					#read file - obj store vertices after a 'v' prefix e.g v -0.6598932 0.4230636 0.188266
					for line in text:
						if line.startswith('vn '):

					#split in to x,y,z - will still have v prefix
					# use a space to split (" ")
							lineList = line.split(" ")
							#only get y normal
							y = lineList[2]
							#add this list, to a list
							normals.append(y)

							#write to file
							normalsFile.write(y +"\n")
				    #stop writing
					normalsFile.close()

					#close object file
					objFile.close()

					#remove car type from list now we have gathered data for it
					#ac.log("removing car type from list to convert")
					carTypesToConvert.remove(car.carType)

					#add this file's location to a list to remove at shutdown
					filesToRemove.append(objFileLocation)
					#included material file is not needed
					mtlFileLocation = 'content/cars/'+ car.carType + '/collider.mtl'
					filesToRemove.append(mtlFileLocation)
					
					#we ahve finished with the converter, et flag to open
					converterAvailable = True


	#convert any car types that we haven't done so previously
	#bottleneck protection, only convert one car per at a time - converter available flag reset when writing to MyDocs File
	carTypesToConvertLength = len(carTypesToConvert)	
	if converterAvailable and carTypesToConvertLength > 0:
		#point to folder if no info found in My Docs
		location = 'content/cars/'+ carTypesToConvert[0] + '/collider.kn5'
		#this will drop .obj in car folder - goGoCarRadar will pick this up and send info to docs			
		convertKn5(location)		
		#ac.log("sending to converter " + str(carTypesToConvert[0]) + " - Cartype")

		converterAvailable = False


	
	#render
	#make sure all cars in list's data has been read before sending any to render - necessary? makes debug tidy at least
	finishedCars = 0

	for i in range(0,len(tempCarList)):
		#check we have data for all cars
		if len(tempCarList[i].vertices) != 0:
			finishedCars = finishedCars + 1


	if finishedCars == len(tempCarList):
		carList = tempCarList
	else:
		return
	
	#work out distance to player
	distanceThreshold = carAura
	pwpX,pwpY,pwpZ = ac.getCarState(ac.getFocusedCar(),acsys.CS.WorldPosition)

	renderQueue = []
	#work out which cars will be rendered, save in list. we need to sort order by distance before rendering
	for car in carList:
		if ac.isConnected(car.carId) == 1:# <CAR_ID> must be the car ID, 0 for the player’s car This function returns 1 if the car is currently connected -
			#can skip our car

			if car.carId != ac.getFocusedCar():				
				wpX,wpY,wpZ = ac.getCarState(car.carId,acsys.CS.WorldPosition)
				differenceX = wpX - pwpX	
				differenceY = wpY - pwpY
				differenceZ = wpZ - pwpZ
				distance = math.sqrt(math.pow(differenceX,2) + math.pow(differenceY,2) + math.pow(differenceZ,2))


				#ESOTIC CODE - Thanks to Esotic from Race Department forums!
				if abs(differenceY) > 5.0: ##what number? HWhat is the smallest bridge - need to have it quite high to avoid major elevation changes. corkscrew lacuna etc
	            #    #if the car is on a different 'plane' of track then exclude them
					car.distance = distanceThreshold * 2.0
				else:
					car.distance = distance
			
			#also, let's ignore cars in the pit too (only if focused car isn't in)- force the distance to beyond threshold
			# was finding it annoying seeing my own car flash up if a car is parked in pit lane
			if ac.isCarInPitline(car.carId) == 1 and ac.isCarInPitline( ac.getFocusedCar() ) == 0:
				car.distance = distanceThreshold * 2
	

	for car in carList:
		#renderCarFactored(car)
		#player car / car camera is on
		if car.carId == ac.getFocusedCar():
			if ac.isConnected(car.carId) == 1:
				#check if any cars are near by checking all distances to player car
				closestDistance = float('inf')
				for car2 in carList:
				##	#if car distance is 0, then it is our car, we dont need to work out the distance from our car to our car
				##car we are checking also needs to be connected
					if car2.carId != ac.getFocusedCar() and ac.isConnected(car2.carId) == 1:
						if car2.distance < closestDistance:
							closestDistance = car2.distance			
				


				#give the closest distance to player car too, we can use it to for alpha - match nearest car's alpha
				car.distance = closestDistance			
				#render player car if a car is within the threshold
				if drawPlayerCar:
					if (closestDistance < distanceThreshold) or (border == True) or (configWindowOpen == True):
						##render now? first? last?
						renderCarFactored(car)

		#all other cars
		else:#		elif car.carId > 0:
			if ac.isConnected(car.carId) == 1 and ac.isConnected(ac.getFocusedCar()):# <CAR_ID> must be the car ID, 0 for the player’s car This function returns 1 if the car is currently connected - disconnect check? #
				if(car.distance < distanceThreshold):				
					#renderCarFactored(car)##add to list
					renderQueue.append(car)
				else:
					car.alpha = 0 #reset this to stop confusion car can escape the range bubble and have its alpha still set at 1

	##sort list by distance
	sortedQueue = sorted(renderQueue, key=lambda car: car.distance) 
	##now we want to reverse so the closest is rendered last, this way any proximity flags rendered are overwritten by a closer car
	sortedQueue.reverse()

	#draw all proximity flags first, the cars then will rest on top
	if(indicatorFlagMode):
		for car in sortedQueue:
			proximityFlag(car)

	for car in sortedQueue:
		renderCarFactored(car)

def findOffset(car):
	global carColours,windowWidth,scale
	#models aren't always centered around the origin for some reason - find the distance and direction from the center/origin of the model and the true origin (0,0,0)
	#find centre by getting average
	averageX = 0		
	averageZ = 0
	#add to vertices and create new list		
	verticesWithOffset = []

	if len(car.offset) == 0: 
			
		for i in range(0,len(car.vertices)):
			averageX += car.vertices[i][0]
			#averageY += vertices[i][1]
			averageZ += car.vertices[i][1]

		averageX/=len(car.vertices)
		#averageY/=len(vertices)
		averageZ/=len(car.vertices)

		offset = (averageX,averageZ)
		car.offset = offset

		for i in range(0,len(car.vertices)):		
			v0 = car.vertices[i][0] - (averageX)
			v1 = car.vertices[i][1] - (averageZ)
			verticesWithOffset.append((v0,v1))	

	#I still dont have a fix if the model is at an angle, how do I get the angle? The two furthest away vertices for each other could be the long axis - It is only the ford mustang that seems to have this problem I think. 
	
	return verticesWithOffset

def getLengthFromFile(carInfoFile):
	#read length directly from file				
		f = open(carInfoFile,'r')
		text = f.readlines()
		for line in text:
			if line.startswith('length'):
				lineList = line.split(" ")
				return float(lineList[1])
				
def getRearZFromFile(carInfoFile):
	#read length directly from file				
		f = open(carInfoFile,'r')
		text = f.readlines()
		for line in text:
			if line.startswith('rearZ'):
				lineList = line.split(" ")
				return float(lineList[1])

def getFrontZFromFile(carInfoFile):
	#read length directly from file				
		f = open(carInfoFile,'r')
		text = f.readlines()
		for line in text:
			if line.startswith('frontZ'):
				lineList = line.split(" ")
				return float(lineList[1])

def getVerticesFromFile(verticesFile):
	#read each line in vertices file, and grab the x and z, enter in to a list (x,y)
	vertices = []
	f = open(verticesFile,'r')
	text = f.readlines()
	for line in text:			
		if line.strip():# skip empty lines (last one)
			lineList = line.split(" ")
			x = float(lineList[0])
			z = float(lineList[2])
			vertices.append((x,z))
		
	return vertices

def getNormalsFromFile(normalsFile):
	#read each line in vertices file, and grab the x and z, enter in to a list (x,y)
	normals = []
	f = open(normalsFile,'r')
	text = f.readlines()
	for line in text:			
		if line.strip():# skip empty lines (last one)
			#lineList = line.split(" ")
			#x = float(lineList[0])
			n = float(line)
			normals.append(n)
		
	return normals

def getFacesFromFile(facesFile):
	

	#a file telling us which vertices are linked to each other to make faces
	faces = []
	f = open(facesFile,'r')
	text = f.readlines()
	
	for line in text:
		if line.strip():#ignore empty lines
			lineList = line.split(" ")
			x = int(lineList[0])
			y = int(lineList[1])
			z = int(lineList[2])

			#indexes in obj for faces start at 1, not 0, fix for our use
			x -= 1
			y -= 1
			z -= 1

			faces.append((x,y,z))

	return faces

def renderCarFactored(car):
	global highPerformanceOnClicked

	##work out alpha
	car.alpha = alphaAtDistance(car,car.distance)	
	
	#work out rotations
	#get angle 	
	car.radsToPlayer = angleToPlayer(car)
	
	degrees = math.degrees(car.radsToPlayer)
	
	#rotate to face upwards on gui
	globalRot = rotationAroundPlayerCar()	
	
	#rotate around own axis
	localRot = rotationAroundThisCar(car)

	#now we know our alpha, draw the background - alpha should be worked out before render call, yes
	#only draw on player car
	if car.carId == ac.getFocusedCar():
		drawBackground(car.alpha)

	#get offset/add if we havent done so already
	if len(car.offset) == 0: 
		car.vertices = findOffset(car)

	if highPerformanceOnClicked == False:
		rotatedPositions = rotateByRads(globalRot,localRot,car.vertices,car)	
		drawRotatedVertices(car.vertices,rotatedPositions,car.faces,car.normals,car.distance,car,degrees)
	else:
		##get length and width to create a rectangle
		if(len(car.rectangleVertices) == 0):
			lowestX = 0
			highestX= 0
			lowestZ = 0
			highestZ = 0
			verticesLength = len(car.vertices)
			#ac.console(str(verticesLength))
			for i in range(0,verticesLength):
			#	#width
				if(car.vertices[i][0] < lowestX):
					lowestX = car.vertices[i][0]
				if(car.vertices[i][0] > highestX):
					highestX = car.vertices[i][0]
				#length
				if(car.vertices[i][1] < lowestZ):
					lowestZ = car.vertices[i][1]
				if(car.vertices[i][1] > highestZ):
					highestZ = car.vertices[i][1]

			rectangleVertices = []
			##top right 
			rectangleVertices.append((highestX,highestZ))
			#top left
			rectangleVertices.append((lowestX,highestZ))
			#bottom left
			rectangleVertices.append((lowestX,lowestZ))
			#bottom right
			rectangleVertices.append((highestX,lowestZ))

			car.rectangleVertices = rectangleVertices
		##send to rotateByRads
		rotatedPositions = rotateByRads(globalRot,localRot,car.rectangleVertices,car)	
		faces = []
		faces.append((0,1,2))
		faces.append((2,3,0))
		normals = []

		drawRotatedVertices(car.rectangleVertices,rotatedPositions,faces,normals,car.distance,car,degrees)


	 #sort thissss	

def angleToPlayer(car):
	global windowWidth,scale
	#player world position	
	fx1,fy1,fz1 = ac.getCarState(ac.getFocusedCar(),acsys.CS.TyreContactPoint,acsys.WHEELS.FL)
	fx2,fy2,fz2 = ac.getCarState(ac.getFocusedCar(),acsys.CS.TyreContactPoint,acsys.WHEELS.FR)
	
	#point betweeen wheels is both added together, and halved
	pbwX = (fx1 + fx2) / 2
	pbwZ = (fz1 + fz2) / 2
	#remove world pos to get fwd facing vector
	wpX,wpY,wpZ = ac.getCarState(ac.getFocusedCar(),acsys.CS.WorldPosition)
	pbwX = pbwX - wpX
	pbwZ = pbwZ - wpZ
	#get angle between fwd facing vector from car and up on gui

	#vector from player to other
	owpX,owpY,owpZ = ac.getCarState(car.carId,acsys.CS.WorldPosition)
	relX = owpX - wpX
	relZ = owpZ - wpZ

	#angle between fwd facing vector and towards player car
	rads = math.atan2(relZ,relX) - math.atan2(pbwZ,pbwX)

	#get angle to player from origin to up
	#if(ac.getFocusedCar() != car.carId):
	#	ac.console(str(math.degrees(rads)))
	
	return rads

def angleToPlayerFromFrontOfCar(car):
	global windowWidth,scale
	#player world position	
	fx1,fy1,fz1 = ac.getCarState(ac.getFocusedCar(),acsys.CS.TyreContactPoint,acsys.WHEELS.FL)
	fx2,fy2,fz2 = ac.getCarState(ac.getFocusedCar(),acsys.CS.TyreContactPoint,acsys.WHEELS.FR)
	
	#point betweeen wheels is both added together, and halved
	pbwX = (fx1 + fx2) / 2
	pbwZ = (fz1 + fz2) / 2	

	#remove world pos to get fwd facing vector
	wpX,wpY,wpZ = ac.getCarState(ac.getFocusedCar(),acsys.CS.WorldPosition)
	pbwX = pbwX - wpX
	pbwZ = pbwZ - wpZ
	#get angle between fwd facing vector from car and up on gui
	

	#normalize fwd vector
	addition = (pbwX * pbwX) + (pbwZ * pbwZ)
	magnitude = math.sqrt(addition)
	unitVectorX  = ( pbwX / magnitude)
	unitVectorY  = ( pbwZ / magnitude)

	##other car length , probs should be saving this
	lowestX = 0
	highestX= 0
	lowestZ = 0
	highestZ = 0
	verticesLength = len(car.vertices)
	#ac.console(str(verticesLength))
	for i in range(0,verticesLength):
	#	#width
		if(car.vertices[i][0] < lowestX):
			lowestX = car.vertices[i][0]
		if(car.vertices[i][0] > highestX):
			highestX = car.vertices[i][0]
		#length
		if(car.vertices[i][1] < lowestZ):
			lowestZ = car.vertices[i][1]
		if(car.vertices[i][1] > highestZ):
			highestZ = car.vertices[i][1]



	#add unit vector * car length/2 to other car pos
	owpX,owpY,owpZ = ac.getCarState(car.carId,acsys.CS.WorldPosition)
	owpX += unitVectorX * highestZ
	owpZ += unitVectorY * highestZ

	#vector from player to other
	
	relX = owpX - wpX
	relZ = owpZ - wpZ

	#angle between fwd facing vector and towards player car
	rads = math.atan2(relZ,relX) - math.atan2(pbwZ,pbwX)
	
	return rads

def angleToPoint(car,point):
	global windowWidth,scale
	#player world position

	#point betweeen wheels is both added together, and halved
	pbwX = point[0]
	pbwZ = point[1]
	#remove world pos to get fwd facing vector
	wpX,wpY,wpZ = ac.getCarState(ac.getFocusedCar(),acsys.CS.WorldPosition)
	pbwX = pbwX - wpX
	pbwZ = pbwZ - wpZ
	#get angle between fwd facing vector from car and up on gui

	#vector from player to other
	owpX,owpY,owpZ = ac.getCarState(car.carId,acsys.CS.WorldPosition)
	relX = owpX - wpX
	relZ = owpZ - wpZ

	#angle between fwd facing vector and towards player car
	rads = math.atan2(relZ,relX) - math.atan2(pbwZ,pbwX)

	#get angle to player from origin to up
	#if(ac.getFocusedCar() != car.carId):
	#	ac.console(str(math.degrees(rads)))
	
	return rads

def rotationAroundPlayerCar():

	fx1,fy1,fz1 = ac.getCarState(ac.getFocusedCar(),acsys.CS.TyreContactPoint,acsys.WHEELS.FL)
	fx2,fy2,fz2 = ac.getCarState(ac.getFocusedCar(),acsys.CS.TyreContactPoint,acsys.WHEELS.FR)
	
	#point betweeen wheels is both added together, and halved
	pbwX = (fx1 + fx2) / 2
	pbwZ = (fz1 + fz2) / 2
	#remove world position from this to make it a directional vector from the center of the car to the wheels
	#player world position
	wpX,wpY,wpZ = ac.getCarState(ac.getFocusedCar(),acsys.CS.WorldPosition)

	pbwX -= wpX
	pbwZ -= wpZ
	#find angle from player car to gui Up
	rads = math.atan2(pbwX,pbwZ)
	#ac.log(str(rads) + "f")       
	return rads

def rotationAroundThisCar(car):

	fx1,fy1,fz1 = ac.getCarState(car.carId,acsys.CS.TyreContactPoint,acsys.WHEELS.FL)
	fx2,fy2,fz2 = ac.getCarState(car.carId,acsys.CS.TyreContactPoint,acsys.WHEELS.FR)
	#point betweeen wheels is both added together, and halved
	pbwX = (fx1 + fx2) / 2
	pbwZ = (fz1 + fz2) / 2
	#remove world pos
	wpX,wpY,wpZ = ac.getCarState(car.carId,acsys.CS.WorldPosition)
	pbwX-= wpX
	pbwZ-= wpZ

	#angle between right and this car's direction 
	# - parameters for atan2 are swapped here and then result is spun by 90 degrees
	#not entirely sure why I can't use the same way as above to get angle - if you realise, let me know please :D
	rads = math.atan2(pbwZ, pbwX)
	#spin
	angle = math.degrees(rads) - 90 # -90 or +90?
	rads = math.radians(angle)
	#ac.log(str(rads) + "f") 
	return rads

def rotateByRads(rads,rads2,points,car):
	global windowWidth, scale

	ca = math.cos(rads)
	sa = math.sin(rads)

	ca2 = math.cos(rads2)
	sa2 = math.sin(rads2)

	#work out direction player car - best place for this? - probably, unless I split the for loop below in to two seperate functions - cba

	#player world position
	pwpX,pwpY,pwpZ = ac.getCarState(ac.getFocusedCar(),acsys.CS.WorldPosition)
	#this car world position
	wpX,wpY,wpZ = ac.getCarState(car.carId,acsys.CS.WorldPosition)

	relativeX = (wpX - pwpX)
	relativeZ = (wpZ - pwpZ)

	#list we will return
	positions = []

	for p in points: #[0,1,2,3] # for(int i = 0; i < 4; i++) in c#			
		#local rotation around car axis
		
		fx = (p[0])
		fz = (p[1])
		
		#rotate positions around this car's axis
		rotatedPlayerVectorX2 = (ca2 * fx - sa2 * fz)
		rotatedPlayerVectorY2 = (sa2 * fx + ca2 * fz)

		fx = rotatedPlayerVectorX2
		fz = rotatedPlayerVectorY2

		#global rotation around center of gui
		
		#add distance from player car		
		fx+=relativeX
		fz+=relativeZ
		#rotate around player car's axis / center of gui
		rotatedPlayerVectorX = (ca * fx - sa * fz)
		rotatedPlayerVectorY = (sa * fx + ca * fz)
		#scale for gui
		rotatedPlayerVectorX *= scale
		rotatedPlayerVectorY *= scale

		## add to center of gui ( 1/2 window size)
		posX = windowWidth *0.5 - rotatedPlayerVectorX # sort center remove width/2?
		posY = windowWidth *0.5 - rotatedPlayerVectorY
		
		positions.append((posX,posY))

	return positions

def proximityFlag(car):
	##draw a triangle over the other car's position
	global proxRange,fadeDistance,carAura,proxSolid,flagWidth,flagLength

	#if car is far off to the side, dont draw, could be at other side of hairpin
	if car.distance > 10:
		return

	if ac.getFocusedCar() == car.carId:
		return
	##work out if need to draw
	radsFromFront = angleToPlayerFromFrontOfCar(car)
	
	#being worked out twice, could save to "car"-meh
	rads = rotationAroundPlayerCar()
	#rotate to face upwards on gui
	globalRot = rotationAroundPlayerCar()	
	#rotate around own axis
	localRot = rotationAroundThisCar(car)

	points = []
	lowestX = 0
	highestX= 0
	lowestZ = 0
	highestZ = 0
	verticesLength = len(car.vertices)
	#other car
	for i in range(0,verticesLength):
	#	#width
		if(car.vertices[i][0] < lowestX):
			lowestX = car.vertices[i][0]
		if(car.vertices[i][0] > highestX):
			highestX = car.vertices[i][0]
		#length
		if(car.vertices[i][1] < lowestZ):
			lowestZ = car.vertices[i][1]
		if(car.vertices[i][1] > highestZ):
			highestZ = car.vertices[i][1]

	#player car
	playerCarVertices = []
	playerOffset = (0,0)
	playerCar = 0#car
	for i in range(0,len(carList)):
		if carList[i].carId == ac.getFocusedCar():
			playerCarVertices = carList[i].vertices
			playerCar = carList[i]

	lowestZPlayer = 0
	highestZPlayer = 0
	lowestXPlayer = 0
	highestXPlayer = 0
	##this is being worked out twice?, optimisation possible here
	for i in range(0,len(playerCarVertices)):
	#	#width
		if(playerCarVertices[i][0] < lowestXPlayer):
			lowestXPlayer = playerCarVertices[i][0]
		if(playerCarVertices[i][0] > highestXPlayer):
			highestXPlayer = playerCarVertices[i][0]
		#length
		if(playerCarVertices[i][1] < lowestZPlayer):
			lowestZPlayer = playerCarVertices[i][1]
		if(playerCarVertices[i][1] > highestZPlayer):
			highestZPlayer = playerCarVertices[i][1]

	#create array for other car, front is first
	points.append((0,highestZ))
	points.append((0,lowestZ))
	points.append((0,highestX))
	points.append((0,lowestX))

	playerPoints = []
	playerPoints.append((0,highestZPlayer))
	playerPoints.append((0,lowestZPlayer))
	playerPoints.append((0,highestXPlayer))
	playerPoints.append((0,lowestXPlayer))

	rotated = rotateByRads(globalRot,localRot,points,car)

	globalRot = rotationAroundPlayerCar()	
	#rotate around own axis
	localRot = rotationAroundThisCar(playerCar)
	rotatedPlayerPoints = rotateByRads(globalRot,localRot,playerPoints,playerCar)
	#draw to front of car
	#ac.glBegin(1)
	#ac.glColor4f(1,1,1,1)
	#ac.glVertex2f(rotatedPlayerPoints[0][0],rotatedPlayerPoints[0][1])#player car
	#ac.glVertex2f(rotated[1][0],rotated[1][1])#other
	#ac.glColor4f(0,0,0,1)
	#ac.glVertex2f(rotatedPlayerPoints[1][0],rotatedPlayerPoints[1][1])#player car
	#ac.glVertex2f(rotated[0][0],rotated[0][1])#other
	#ac.glEnd()
	#to front left

	#ac.console(str(rotated[0][1] - windowWidth/2))
	#check height on gui, don't render if car is beyond or before player car length
	if (rotated[1][1] < rotatedPlayerPoints[0][1]) or (rotated[0][1] > rotatedPlayerPoints[1][1]):
		return

	#check = rotated[2][0] - rotatedPlayerPoints[2][0]
	#check2 = highestXPlayer*2
	#ac.console(str(check) + " check")
	#ac.console(str(check2) + " check2")
	

	ca = math.cos(rads)
	sa = math.sin(rads)

	#ca2 = math.cos(rads2)
	#sa2 = math.sin(rads2)

	#work out direction player car - best place for this? - probably, unless I split the for loop below in to two seperate functions - cba

	#player world position
	pwpX,pwpY,pwpZ = ac.getCarState(ac.getFocusedCar(),acsys.CS.WorldPosition)
	#this car world position
	wpX,wpY,wpZ = ac.getCarState(car.carId,acsys.CS.WorldPosition)

	relativeX = (wpX - pwpX)
	relativeZ = (wpZ - pwpZ)
	
	#add distance from player car		
	fx=relativeX
	fz=relativeZ
	#rotate around player car's axis / center of gui
	rotatedPlayerVectorX = (ca * fx - sa * fz)
	rotatedPlayerVectorY = (sa * fx + ca * fz)
	#scale for gui
	rotatedPlayerVectorX *= scale
	rotatedPlayerVectorY *= scale

	## add to center of gui ( 1/2 window size)
	posX = windowWidth *0.5 - rotatedPlayerVectorX # sort center remove width/2?
	posY = windowWidth *0.5 - rotatedPlayerVectorY

	##now we have the direction, create a triangle around this
	##normalized directional vector
	centre = (windowWidth/2,windowWidth/2)

	directionalX = posX - centre[0]
	directionalY = posY - centre[1]
	addition = (directionalX * directionalX) + (directionalY * directionalY)
	magnitude = math.sqrt(addition)
	unitVectorX  = ( directionalX / magnitude)
	unitVectorY  = ( directionalY / magnitude)
	
	redWarningDistance = 10
	startDistance = car.distance

	##how wide the arc is
	#minWidth = 1
	spread = ((car.distance)) + flagWidth;

	##how extravagant the "explosion"of the arc is when it gets close to car. Also extends end distance of red arc
	pop = 3
	endDistance = car.distance + highestZPlayer + startDistance#10?..

	##if prox fade edgealpha =0
	##if prox solid, edge and this = 1
	edgeAlpha = 0#thisAlpha#or zero?
	
	if proxSolid:
		endDistance /= 2

	if(car.distance < redWarningDistance):
		startDistance = car.distance
		endDistance+= ((redWarningDistance - car.distance)*pop*0.5)*flagLength
		#push arc to get attention
		spread += ((redWarningDistance - car.distance)*pop)
		#endDistance += redWarningDistance-car.distance
	
	startPos = (centre[0],centre[1])
	endPos = (centre[0] + unitVectorX*scale*endDistance,centre[1] + unitVectorY*scale*endDistance)

	##now create a wedge shape by rotating "arm"

	#Rotate a point counterclockwise by a given angle around a given origin.
	#The angle should be given in radians.
	#centre of app window
	#ox, oy = origin
	px = unitVectorX
	py = unitVectorY

	#1stpoint is (0,0)
	ox = 0
	oy = 0

	##overall opacity slider influence
	thisAlpha = alphaAtDistance(car,car.distance*2)
	thisAlpha -= 1 - overallOpacity

	#red
	r = 1
	#capped = car.distance#doing this to stop a pink happening when super close
	##if(capped < 3):
	##	capped = 3
	#green - needs to rise smoothly
	g = math.tanh((car.distance/((highestXPlayer*0.5) + (highestX*0.5))/4) - 1)
	#blue - controls how orange it is mid distance -  needs to go from 1, to 0.5 back to 1
	b = 0 #math.tanh(g*(g*2)) #math.tanh(g)#..meh, was trying to get orange for longer. couldnt do it without it going pink
	#ac.console("R " + str(r) + " G " + str(g) + " B " + str(b))
	
	#simple?
	lines = False
	points = []
	i =- spread
	fraction = 3##1 or 2 or 3 option , low med high quality

	while i < spread + 0.1:#inaccuracy..

		#topleft to bottom left		
		#degrees
		degrees = i

		#radians
		#ac.log(str(degrees) + ' degrees')
		angle = math.radians(degrees)
		#ac.log(str(angle) + ' rads')
		
		#rotated unit vector
		qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
		qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

		##add to startpos
		nearest = (startPos[0] + (qx*scale*startDistance),startPos[1] + (qy*scale*startDistance))
		furthest = (startPos[0] + (qx*scale*endDistance),startPos[1] + (qy*scale*endDistance))

		##draw
		
		if lines:
			ac.glBegin(0)
			ac.glColor4f(r,g,b,thisAlpha)
			ac.glVertex2f(nearest[0],nearest[1])
			ac.glColor4f(r,g,b,0)
			ac.glVertex2f(furthest[0],furthest[1])
			ac.glEnd()
		else:
			#tris
			points.append((nearest[0],nearest[1]))
			points.append((furthest[0],furthest[1]))		

		i+=spread/fraction

	##there may be a slight bit left over , fill it in

	if proxSolid:
		edgeAlpha = 1
		thisAlpha = 1

	for i in range(0,len(points)-3,2):
		
		ac.glBegin(2)

		ac.glColor4f(r,g,b,thisAlpha)
		ac.glVertex2f(points[i][0],points[i][1])
		ac.glColor4f(r,g,b,thisAlpha)
		ac.glVertex2f(points[i+2][0],points[i+2][1])		
		ac.glColor4f(r,g,b,edgeAlpha)
		ac.glVertex2f(points[i+1][0],points[i+1][1])		

		ac.glColor4f(r,g,b,edgeAlpha)
		ac.glVertex2f(points[i+1][0],points[i+1][1])
		ac.glColor4f(r,g,b,thisAlpha)
		ac.glVertex2f(points[i+2][0],points[i+2][1])
		ac.glColor4f(r,g,b,edgeAlpha)
		ac.glVertex2f(points[i+3][0],points[i+3][1])

		ac.glEnd()

def alphaAtDistance(car,distance):
	global angleOfInfluence,fadeDistance,fadeTime,border,configWindowOpen,carAura, rearCutOffDistance
	if car.carId != ac.getFocusedCar():
		#This function gives a smooth curve from 0 to 1
		#	tanh	Hyperbolic tangent (tanh) of a value or expression	
		# distance at which cars start to fade (kinda) - after they have got passed car Aura's distance - car Aura is like a deadzone		
		fadeDistance = 5

		#we will use this value if fade mode is off( nothing outside carAura or "distance" is sent here)
		alphaToReturn = 1

		#fade mode		
		#player world position
		pwpX,pwpY,pwpZ = ac.getCarState(ac.getFocusedCar(),acsys.CS.WorldPosition)
		#this car world position
		wpX,wpY,wpZ = ac.getCarState(car.carId,acsys.CS.WorldPosition)

		relativeX = (wpX - pwpX)
		relativeZ = (wpZ - pwpZ)
		
		globalRot = rotationAroundPlayerCar()
		ca = math.cos(globalRot)
		sa = math.sin(globalRot)		
		rotatedPlayerVectorY2 = (sa * relativeX + ca * relativeZ)
		
		# rear end distance cutoff
		if(rotatedPlayerVectorY2 <  -(carAura - rearCutOffDistance)):			
			inValue =  distance/(carAura -rearCutOffDistance) # After all these years I still don't understand why I need * 2						
			curveSpeed = 20 # this value changes how aggressively it fades out
			endFraction = 1.15 # this value changes when it starts to fade out (very sensitive)
			x = inValue
			z = curveSpeed
			b = endFraction						
			result = (math.tanh((z*x) - (z/b)) + 1)/2			
			#graph returns from 0 to 1, but we need the inverse
			return 1 - result

		degrees = math.fabs(math.degrees(car.radsToPlayer))
		if(degrees < angleOfInfluence/2 or degrees > 360 - (angleOfInfluence/2)):
			if fadeTime == 10:
				diff = degrees - angleOfInfluence*0.5
				#to be honest, i just trial and errored this until it worked, no master plan on it
				#the idea behind it is if  the angle to the target car and the player's angle choice is small, then fade out
				#trickin the player/focused car in to thinkning the car is further away so we can fade it using the same graph below
				if(diff < fadeDistance/2):
					distance -= diff
				if(diff > fadeDistance/2):
					distance += diff

			else:
				#binary mdoe
				alphaToReturn = 0

		#use a smoothing function to create a nice sweep in transitions if fade mode is on
		#if fade mode on
		
		if fadeTime > 1:
			#if fade mdoe, lets' fade out the last tenth of the range
			#so first 9 tenths, should be alpha 1

			##this value is from 0 to 1, with 0 being at player car, and 1 begin edge of range ring
			inValue = (distance)/carAura
			
			#https://www.desmos.com/calculator/wwbo2km0um	-visit here to see graph - you can play around with the sliders - alpha needs to be between 0 and 1
			curveSpeed = 20 # this value changes how aggressively it fades out
			endFraction = 1.15 # this value changes when it starts to fade out (very sensitive, I think maybe a bad idea to expose these vars to users (I will almost def get a request to change these :D))

			x = inValue
			z = curveSpeed
			b = endFraction			
			
			result = (math.tanh((z*x) - (z/b)) + 1)/2			
			#grpah is running from 0 to 1, but we need the inverse
			alphaToReturn = 1- result
		
	else:
		#work out our own car
		#match the highest alpha already drawn on the screen
		highest = 0
		index = 0
		for c in carList:
			if c.carId == ac.getFocusedCar():
				continue

			if c.alpha > highest:
				highest = c.alpha				

		alphaToReturn = highest

	#if user has clicked the window, override this alpha value and display car
	if car.carId == ac.getFocusedCar() and (border or configWindowOpen):
		alphaToReturn		

	return alphaToReturn

def drawRotatedVertices(originalVertices,vertices,faces,normals,distance,car,angleToFocused): #fix
	global border,testRun,boundary,carColours,playerCarMeshColourIndex,border,windowConfigOpen,otherCarMeshColourIndex,playerCarOutlineColourIndex,configWindowOpen,scale,carAura,angleOfInfluence,carList,highPerformanceOnClicked,indicatorMode,proxRange,blueFlags,fadeTime,overallOpacity,indicatorFlagMode,flagWidth,flagLength

	#ac.console(str(highPerformanceOnClicked))

	###move this stuff to seperate functions#########
	
	#alpha = 0
	#work out other car's alpha
	
	#############
	##overall opacity slider influence
	thisAlpha = car.alpha
	thisAlpha -= 1 - overallOpacity
	if car.carId == ac.getFocusedCar():
		if configWindowOpen:
			thisAlpha = 1*overallOpacity



	carBoundaryLength = len(car.boundary)

	renderedIndices = []

	#set colour depending on who we are drawing
	carColour = carColours[otherCarMeshColourIndex]
	ac.glColor4f(carColour[0],carColour[1],carColour[2],thisAlpha)
	if car.carId == ac.getFocusedCar():
		carColour = carColours[playerCarMeshColourIndex]
		ac.glColor4f(carColour[0],carColour[1],carColour[2],thisAlpha)

		#indicator?
	
	r = 0
	g = 0
	b = 0

	if(indicatorMode and car.carId != ac.getFocusedCar()):
		
		#red
		r = 1
		capped = distance#doing this to stop a pink happening when super close
		if(capped < 3):
			capped = 3
		#green - needs to rise smoothly
		#g = math.tanh((capped/proxRange) - 1)
		#blue - controls how orange it is mid distance -  needs to go from 1, to 0.5 back to 1
		#b = math.pow(g,2) #math.tanh(g*(g*2)) #math.tanh(g)#..meh, was trying to get orange for longer. couldnt do it without it going pink
		
		##test
		g=1
		##blue needs to drop twice as fast as the green
		b = math.tanh(((distance/proxRange)*0.33 - 1)*5) #make this smalleras we go
		g = math.tanh(((distance/proxRange)*0.66 - 1)*5)#fade time is 5
		#ac.console(str(proxRange))

		ac.glColor4f(r,g,b,thisAlpha)
		#if(car.makeBlue == False):
		#	car.blueCounter += 1
	#ac.console("R " + str(r) + " G " + str(g) + " B " + str(b))
	#blue flag
	#we are using normalized spline position and lap number to decide whether to show the car as blue
	#unfortunately, the start of the spline and what kunos are using to add to the lap counter don't line up. Thanks.
	#So, when we think we need to change to blue, we will start a small timer, when the timer is finished, we will double check we still want to change
	#this should stop any flickering between states as it gets confused between the start of the spline and the lap number

	#ac.console("Car name = "  + str( ac.getDriverName(car.carId)))
	#ac.console("Laps = " + str(ac.getCarState(car.carId,acsys.CS.LapCount)))
	
	##if bool is set and if race session
	if blueFlags == True and info.graphics.session ==2:#this is in the shared memory file
		if ac.getCarState(car.carId,acsys.CS.LapCount) != 0:
			### Was getting blue cars on the grid after quali if the other car had done more laps than you - This stops it happening- bit of a mucky solution - Not sure why it was happeniong - both car's lap counts should be zero (and are in the console):()
			if ac.getCarState(car.carId,acsys.CS.LapCount) > ac.getCarState(ac.getFocusedCar(),acsys.CS.LapCount):

				#this nested if statemnt keeps a blue car blue just after the line until player cross finish line - if following a blue
				if ac.getCarState(car.carId,acsys.CS.LapCount) - ac.getCarState(ac.getFocusedCar(),acsys.CS.LapCount) >= 2:
					if ac.getCarState(car.carId, acsys.CS.NormalizedSplinePosition) < 0.1 and ac.getCarState(ac.getFocusedCar(), acsys.CS.NormalizedSplinePosition) > 0.9:			
							#ac.glColor4f(0,0,1,car.alpha)
							#car.makeBlue = True
						if car.makeBlue == False:
							car.blueCounter += 1

				elif ac.getCarState(car.carId,acsys.CS.LapCount) - ac.getCarState(ac.getFocusedCar(),acsys.CS.LapCount) == 1:
					if ac.getCarState(car.carId, acsys.CS.NormalizedSplinePosition) < 0.1 and ac.getCarState(ac.getFocusedCar(), acsys.CS.NormalizedSplinePosition) > 0.9:			
						#ac.glColor4f(r,g,b,car.alpha)
						if car.makeBlue == True:
							car.blueCounter += 1
						#pass
					else:
						#ac.glColor4f(0,0,1,car.alpha)
						if car.makeBlue == False:
							car.blueCounter += 1
				

			elif ac.getCarState(car.carId,acsys.CS.LapCount) == ac.getCarState(ac.getFocusedCar(),acsys.CS.LapCount):
				#this nested if statemnt keeps a blue car blue just after the line until player cross finish line
				if ac.getCarState(car.carId, acsys.CS.NormalizedSplinePosition) > 0.9:
					if ac.getCarState(ac.getFocusedCar(), acsys.CS.NormalizedSplinePosition) < 0.1:			
						#ac.glColor4f(0,0,1,car.alpha)
						if car.makeBlue == False:
							car.blueCounter += 1
						pass
				else:
					if car.makeBlue == True:
							car.blueCounter += 1

			

			if(car.blueCounter >= 20):
				
				if car.makeBlue == False:
					car.makeBlue = True
					car.blueCounter = 0

				elif car.makeBlue == True:
					#ac.glColor4f(r,g,b,car.alpha)
					car.makeBlue = False
					car.blueCounter = 0

		#when bug testing, tried out helicorsa's old method - Blue cars can trun normal for second when passing over of the start/finish line with you as they share lap count momentarily
		#isRaceSession = True
		#if isRaceSession and ac.getCarState(car.carId,acsys.CS.LapCount) > ac.getCarState(ac.getFocusedCar(),acsys.CS.LapCount) and  ac.getCarState(car.carId, acsys.CS.NormalizedSplinePosition) <  ac.getCarState(ac.getFocusedCar(), acsys.CS.NormalizedSplinePosition) and  ac.getCarState(ac.getFocusedCar(), acsys.CS.NormalizedSplinePosition) -  ac.getCarState(car.carId, acsys.CS.NormalizedSplinePosition)< 0.05:

			if(car.makeBlue == True):
				ac.glColor4f(0,0,1,thisAlpha)
	

	trianglesToDraw = []
	#use faces list to represent the vertices/positions in an arranged format
	for i in range(0,len(faces)):
		
		face = faces[i]

		#ac.log(str(face))
		
		a = face[0]		
		b = face[1]		
		c = face[2]		

		vA = vertices[a]
		vB = vertices[b]
		vC = vertices[c]
		
		vA0 = vA[0]
		vA1 = vA[1]


		vB0 = vB[0]
		vB1 = vB[1]

		vC0 = vC[0]
		vC1 = vC[1]
		


		#left or right side?
		#x value
		
		
		#only render triangles with face-normals facing downwards - this will give us the simplest shape without having to simplify/decimate the mesh at all
		#if we render all triangles, it is too slow, that's why we need to dinf a way to reduce draw calls
		#if we wanted to make more this more efficient, we could do this check before writing the info files, so that the files only contain the downwards facing triangles/vertices - I'd like tp keep all vertices in file in cae i need them later
		

		if(highPerformanceOnClicked == False):
			
			#vertice normals
			normalA = normals[a]
			normalB = normals[b]
			normalC = normals[c]


			if normalA > 0:
				continue
			if normalB > 0:
				continue
			if normalC > 0:
				continue

		
		#save triangles that we render to a list - this will be used to work out the outline
		
		if carBoundaryLength == 0 and highPerformanceOnClicked == False:
			renderedIndices.append((a,b,c))

		if len(car.boundarySimple) == 0 and highPerformanceOnClicked == True:
			renderedIndices.append((a,b,c))

		if(drawMeshOfCars):

			#ac.glBegin(2)#2 for tris
			#add tri
			#colour side?
			#if originalVertices[a][0] > 0:
			#	ac.glColor3f(0,0,0)
			#else:
			#	ac.glColor3f(1,0,0)		
			trianglesToDraw.append((vA0,vA1))
			#ac.glVertex2f(vA0,vA1)		
			#flip triangle, we are effectively drawing the underside of the car upside down - so that it faces skywards ;)

			#if originalVertices[c][0] > 0:
			#	ac.glColor3f(0,0,0)
			#else:
			#	ac.glColor3f(1,0,0)
			trianglesToDraw.append((vC0,vC1))
			#ac.glVertex2f(vC0,vC1)

			#if originalVertices[b][0] > 0:
			#	ac.glColor3f(0,0,0)
			#else:
			#	ac.glColor3f(1,0,0)
			trianglesToDraw.append((vB0,vB1))
			#ac.glVertex2f(vB0,vB1)
			#ac.glEnd()

	
	
	#ac.console(str(len(trianglesToDraw)))
	
	
	counterRender = 0
	for i in range(0,len(trianglesToDraw)-2,3):

		wireframe = False

		if wireframe:
			
			ac.glColor4f(0,0,0,1)
			ac.glBegin(0)
			ac.glVertex2f(trianglesToDraw[i][0],trianglesToDraw[i][1])
			ac.glVertex2f(trianglesToDraw[i+1][0],trianglesToDraw[i+1][1])

			ac.glVertex2f(trianglesToDraw[i+1][0],trianglesToDraw[i+1][1])		
			ac.glVertex2f(trianglesToDraw[i+2][0],trianglesToDraw[i+2][1])

			ac.glVertex2f(trianglesToDraw[i+2][0],trianglesToDraw[i+2][1])		
			ac.glVertex2f(trianglesToDraw[i][0],trianglesToDraw[i][1])
			ac.glColor4f(carColour[0],carColour[1],carColour[2],thisAlpha)

			ac.glEnd()

		ac.glBegin(2)
		ac.glVertex2f(trianglesToDraw[i][0],trianglesToDraw[i][1])
		ac.glVertex2f(trianglesToDraw[i+1][0],trianglesToDraw[i+1][1])		
		ac.glVertex2f(trianglesToDraw[i+2][0],trianglesToDraw[i+2][1])		

		#ac.glVertex2f(trianglesToDraw[i+4][0],trianglesToDraw[i+4][1])
		#ac.glVertex2f(trianglesToDraw[i+5][0],trianglesToDraw[i+5][1])		
		#ac.glVertex2f(trianglesToDraw[i+6][0],trianglesToDraw[i+6][1])		

		ac.glEnd()

		counterRender += 1
		if(counterRender == 3):
		#	ac.glEnd()
		#	ac.glBegin(2)
			counterRender = 0
	

	#if we haven't found edges yet, do so and save in car's info class
	if(highPerformanceOnClicked == False):
		if carBoundaryLength == 0:# and highPerformanceOnClicked == False:
			#works out boundary for this car and saves info to its own class - to make more efficient could save edges to carTypes list and read from there instead
			#ac.console("Working out boundary for " + str(car.carId))
			edges = GetEdges2(renderedIndices)	
			car.boundary = FindBoundary(edges)

	elif(highPerformanceOnClicked == True):
		if len(car.boundarySimple) == 0:
			#ac.console("rendered indices count " + str(len(renderedIndices)))
			edges = GetEdges2(renderedIndices)
			#ac.console("edges count " + str(len(edges)))
			car.boundarySimple = FindBoundary(edges)

	#draw outline
	if drawOutlineOfCars:
		#dont draw if outline is the same colour. saves processing
		if (car.carId == ac.getFocusedCar() and (playerCarMeshColourIndex != playerCarOutlineColourIndex)) or (car.carId != ac.getFocusedCar() and (otherCarMeshColourIndex != otherCarOutlineColourIndex)):

			boundary = car.boundary
			if(highPerformanceOnClicked):
				boundary = car.boundarySimple

			for edge in boundary:
				#draw lines
				outlineColour = carColours[playerCarOutlineColourIndex]
				ac.glColor4f(carColours[otherCarOutlineColourIndex][0],carColours[otherCarOutlineColourIndex][1],carColours[otherCarOutlineColourIndex][2],thisAlpha)
				if car.carId == ac.getFocusedCar():
					ac.glColor4f(carColours[playerCarOutlineColourIndex][0],carColours[playerCarOutlineColourIndex][1],carColours[playerCarOutlineColourIndex][2],thisAlpha)

				ac.glBegin(0)
				ac.glVertex2f(vertices[edge.v1][0],vertices[edge.v1][1])
				ac.glVertex2f(vertices[edge.v2][0],vertices[edge.v2][1])		
				ac.glEnd()

	

	#draw config "other" car, so use can see what colour they are setting opponent car to - should move this section of code to own function
	if configWindowOpen:
		if car.carId == ac.getFocusedCar():

			offsetX = 2 * scale
			offsetY = .5 * scale
			ca = math.cos(math.radians(10))
			sa = math.sin(math.radians(10))
		
			rV = []
			#rotate so it looks nice -sry variable names are not very readable
			for i in range(0,len(vertices)):
				
				rX = (ca * vertices[i][0] - sa * vertices[i][1])
				rY = (sa * vertices[i][0] + ca * vertices[i][1])
				rV.append((rX,rY))


			#draw proximity flag first if options is set to true
			if (indicatorFlagMode):

				points = []
				spread = flagWidth + 10
				i =- spread
				fraction = 3##1 or 2 or 3 option , low med high quality
				startPos = (windowWidth/2,windowWidth/2)
				
				while i < spread + 0.1:#inaccuracy..

					#topleft to bottom left		
					#degrees
					degrees = i
					#radians
					#ac.log(str(degrees) + ' degrees')
					angle = math.radians(degrees)
					
					#
					#draw line from centre of gui to config car
					ca = math.cos(math.radians(i + 60))
					sa = math.sin(math.radians(i + 60))

					rX = (ca * 0 - sa * 1)
					rY = (sa * 0 + ca * 1)
					##add to startpos
					startDistance = 2
					endDistance = 10
					if(proxSolid == False):
						endDistance*=2

					nearest = (startPos[0] + (rX*scale*startDistance),startPos[1] + (rY*scale*startDistance))
					furthest = (startPos[0] + (rX*scale*endDistance)*(flagLength+.3),startPos[1] + (rY*scale*endDistance)*(flagLength+.3))

					
					#tris
					points.append((nearest[0],nearest[1]))
					points.append((furthest[0],furthest[1]))		

					lines = False
					if lines:
						ac.glBegin(0)
						ac.glColor4f(r,g,b,thisAlpha)
						ac.glVertex2f(nearest[0],nearest[1])
						ac.glColor4f(r,g,b,1)
						ac.glVertex2f(furthest[0],furthest[1])
						ac.glEnd()

					i+=spread/fraction

				##there may be a slight bit left over , fill it in
				edgeAlpha = 0
				if proxSolid:
					edgeAlpha = 1
					thisAlpha = 1

				r = 1
				g = 128/255
				b = 0 
					
				for i in range(0,len(points)-3,2):
					
					ac.glBegin(2)
					
					ac.glColor4f(r,g,b,thisAlpha)
					ac.glVertex2f(points[i][0],points[i][1])
					ac.glColor4f(r,g,b,thisAlpha)
					ac.glVertex2f(points[i+2][0],points[i+2][1])		
					ac.glColor4f(r,g,b,edgeAlpha)
					ac.glVertex2f(points[i+1][0],points[i+1][1])		

					ac.glColor4f(r,g,b,edgeAlpha)
					ac.glVertex2f(points[i+1][0],points[i+1][1])
					ac.glColor4f(r,g,b,thisAlpha)
					ac.glVertex2f(points[i+2][0],points[i+2][1])
					ac.glColor4f(r,g,b,edgeAlpha)
					ac.glVertex2f(points[i+3][0],points[i+3][1])

					ac.glEnd()

			for i in range(0,len(faces)):
				
			#for face in faces:		
			#set colour depending on who we are drawing
				carColour = carColours[otherCarMeshColourIndex]
				ac.glColor4f(carColour[0],carColour[1],carColour[2],1)

				if(indicatorMode):
					#force car orangey red to indicate mode is on
					if(proxRange == 3):
						#lowest
						ac.glColor4f(255/255,1,1,thisAlpha)

					if(proxRange == 4):
						#med
						ac.glColor4f(255/255,180/255,0.5,thisAlpha)

					if(proxRange == 5):
						#high
						ac.glColor4f(255/255,.5,.2,thisAlpha)
					if(proxRange == 6):
						#high
						ac.glColor4f(255/255,0.25,0.1,thisAlpha)

					##test
					r=1					
					##blue needs to drop twice as fast as the green
					b = math.tanh((5/proxRange) - 1)
					g = math.tanh((5/proxRange) - 1)*3 #make this bigger as we go ////WHY 5
					ac.glColor4f(r,g,b,thisAlpha)

				face = faces[i]
				a = face[0]		
				b = face[1]		
				c = face[2]		

				vA = rV[a]
				vB = rV[b]
				vC = rV[c]

				vA0 = vA[0]
				vA1 = vA[1]

				vB0 = vB[0]
				vB1 = vB[1]		

				vC0 = vC[0]
				vC1 = vC[1]

				if(highPerformanceOnClicked == False):
					#vertice normals
					normalA = normals[a]
					normalB = normals[b]
					normalC = normals[c]


					if normalA > 0:
						continue
					if normalB > 0:
						continue
					if normalC > 0:
						continue

				if(drawMeshOfCars):

					
					ac.glBegin(2)
					ac.glVertex2f(vA0 - offsetX,vA1 + offsetY)		
					ac.glVertex2f(vC0- offsetX,vC1 + offsetY)
					ac.glVertex2f(vB0- offsetX,vB1 + offsetY)
					a = ac.glEnd()
			

			#draw outline
			if drawOutlineOfCars:
				if  (otherCarMeshColourIndex != otherCarOutlineColourIndex):
					boundary = car.boundary
			
					if(highPerformanceOnClicked):
						boundary = car.boundarySimple

					for edge in boundary:
						#draw lines
						outlineColour = carColours[playerCarOutlineColourIndex]
						ac.glColor4f(carColours[otherCarOutlineColourIndex][0],carColours[otherCarOutlineColourIndex][1],carColours[otherCarOutlineColourIndex][2],thisAlpha)
						ac.glBegin(0)
						ac.glVertex2f(rV[edge.v1][0] - offsetX,rV[edge.v1][1] + offsetY)
						ac.glVertex2f(rV[edge.v2][0] - offsetX,rV[edge.v2][1] + offsetY)		
						ac.glEnd()

def drawRotatedRectangle(positions):


	ac.glBegin(2)#2 for tris
	#add 3 vertices
	ac.glVertex2f((positions[0][0]),(positions[0][1]))#front left
	ac.glVertex2f((positions[2][0]),(positions[2][1]))#rear right		
	ac.glVertex2f((positions[1][0]),(positions[1][1]))#front right
	#next tri
	ac.glVertex2f((positions[0][0]),(positions[0][1]))#front left
	ac.glVertex2f((positions[3][0]),(positions[3][1]))#rear left
	ac.glVertex2f((positions[2][0]),(positions[2][1]))#rear right
	
	a = ac.glEnd()


def convertKn5(location):

    #ac.log("converting")

    SW_HIDE = 0
    info = subprocess.STARTUPINFO()
    info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = SW_HIDE
    #ac.log(str(location))
    #ac.log("opening subprocess")
    command = ["apps/python/carRadar/dist/kn5conv.exe" , "-obj", location]
    p =subprocess.Popen(command, startupinfo=info)
    #p.kill()needed?

def acShutdown():
	global filesToRemove,playerCarMeshColourIndex,playerCarOutlineColourIndex,otherCarMeshColourIndex,otherCarOutlineColourIndex,carAuraTarget,angleTarget,highPerformanceOnClicked,indicatorMode,proxRange,blueFlags,fadeTime,overallOpacity,indicatorFlagMode,proxSolid,flagWidth,backgroundColourIndex,backgroundShape,flagLength,rearCutOffDistance

	for file in filesToRemove:
		os.remove(file)

	
	#save config
	homeDirectory = os.path.expanduser("~")
	dir = os.path.join(homeDirectory,"Documents","Assetto Corsa","apps","carRadar")
	#check if we have dropped file before
	filename = 'config.txt'
	configFileLocation = os.path.join(dir, filename)

	configFile = open(configFileLocation, "r+")
	#empty contents
	configFile.truncate()
	#write last used values
	configFile.write("scale " + str(scale)+'\n')
	configFile.write("playerColour " + str(playerCarMeshColourIndex)+'\n')
	configFile.write("playerOutline " + str(playerCarOutlineColourIndex)+'\n')
	configFile.write("otherColour " + str(otherCarMeshColourIndex)+'\n')
	configFile.write("otherOutline " + str(otherCarOutlineColourIndex)+'\n')
	configFile.write("range " + str(carAuraTarget)+'\n')
	configFile.write("angle " + str(angleTarget)+'\n')
	if(highPerformanceOnClicked == False):
		configFile.write("simpleMode " + str(0)+'\n')
	else:
		configFile.write("simpleMode " + str(1)+'\n')

	if(indicatorMode == False):
		configFile.write("proximityMode " + str(0)+'\n')
	else:
		configFile.write("proximityMode " + str(1)+'\n')

	configFile.write("proxRange " + str(proxRange)+'\n')

	if(blueFlags == False):
		configFile.write("blueFlags " + str(0)+'\n')
	else:
		configFile.write("blueFlags " + str(1)+'\n')

	if(fadeTime == 1):
		configFile.write("fadeTime " + str(1)+'\n')
	else:
		configFile.write("fadeTime " + str(10)+'\n')

	configFile.write("overallOpacity " + str(overallOpacity)+'\n')	

	if(indicatorFlagMode == False):
		configFile.write("indicatorFlagMode " + str(0)+'\n')
	else:
		configFile.write("indicatorFlagMode " + str(1)+'\n')

	if(proxSolid == False):
		configFile.write("proxSolid " + str(0)+'\n')
	else:
		configFile.write("proxSolid " + str(1)+'\n')

	configFile.write("flagWidth " + str(flagWidth)+'\n')

	configFile.write("backgroundColourIndex " + str(backgroundColourIndex)+'\n')

	configFile.write("backgroundShape " + str(backgroundShape)+ '\n')

	configFile.write("flagLength " + str(flagLength)+ '\n')

	configFile.write("rearCutOffDistance " + str(rearCutOffDistance)+ '\n')

	configFile.close()
	
class CarAndInfo():
	def __init__(self, carId, carType,distance,vertices,rectangleVertices,faces,normals,boundary,boundarySimple,radsToPlayer,alpha,blueCounter,makeBlue,offset):
		self.carId = carId
		self.carType = carType
		self.distance = distance
		self.vertices = vertices
		self.rectangleVertices = rectangleVertices
		self.faces = faces
		self.normals = normals
		self.boundary = boundary
		self.boundarySimple = boundarySimple
		self.radsToPlayer = radsToPlayer
		self.alpha = alpha		
		self.blueCounter = blueCounter
		self.makeBlue = makeBlue
		self.offset = offset		

class Edge():
	def __init__(self,v1,v2):

		self.v1 = v1
		self.v2 = v2

def GetEdges(aIndices):

	result = []
	for i in range(0,len(aIndices),3):

		v1 = aIndices[i]
		v2 = aIndices[i + 1]
		v3 = aIndices[i + 2]
		result.append(Edge(v1, v2, i))
		result.append(Edge(v2, v3, i))
		result.append(Edge(v3, v1, i))

	return result;

def GetEdges2(faces):
	#pass faces list to this and it creates a list of edges of each triangle
	result = []
	for i in range(0,len(faces)):

		v1 = faces[i][0]
		v2 = faces[i][1]
		v3 = faces[i][2]
		result.append(Edge(v1, v2))
		result.append(Edge(v2, v3))
		result.append(Edge(v3, v1))

	return result;

def FindBoundary(aEdges):
     
	#copy list
	result = list(aEdges)
	i = len(result) - 1	
	removed = 0
	while i > 0:
		#ac.log('i ' + str(i))
		j = i - 1
		while j >= 0:
			#ac.log('j ' + str(j))
			if (result[i].v1 == result[j].v2 and result[i].v2 == result[j].v1):
				removed += 1
				del result[i]
				del result[j]
				i-=1
				break
			j -= 1
		i-=1


	#ac.log(str(removed*2) + ' removed')
	#ac.log(str(len(result)))

	return result;
    
