#This class is for setting up UI only
from Tkinter import * #Python ui lib

class UiControllerModule:
	
	def _init_(self):
		self.root = Tk()#ROOT is the whole window
		self.topFrame = Frame(root)
		self.topFrame.pack(side=TOP)
		self.downFrame = Frame(root)
		self.downFrame.pack(side=BOTTOM)
		#Down Row for info about navigation

		self.leftFrame = Frame(topFrame)
		self.leftFrame.pack(side=LEFT)
		#Left Column for info about the current location

		self.middleFrame = Frame(topFrame)
		self.middleFrame.pack(side=LEFT)
		#Middle Column for a controller to be implemented with twist

		self.rightFrame = Frame(topFrame)
		self.rightFrame.pack(side=LEFT)

		self.rightButtonList = []

		self.midButtonList = []

		#Right Column for Adding nav goal

		self.setupDownRow()

		self.setupLeftColumn()

		self.directionKeyCallbacks = [self.directionButtonCallbackPlaceholder] * 9

		self.setupLeftColumn(directionKeyCallbacks)
		#This is a list of all callbacks for 9 buttons on the controller, 
		#this number 9 shouldn't be changed
		#The functions in the list is meant to be changed, but has to have two parameters
		#self and an integer
		#Each func in the list corresponds to one button
		#0 1 2
		#3 4 5
		#6 7 8
		
		root.bind("<Key>", self.keyPressed)
		root.bind('<KeyRelease>',self.keyReleased)

		

		

	def setupDownRow(self):
		navi_info = Label(
			downFrame, text="No Navigation Started.",
			font=("Helvetica", 16),anchor=W, 
			justify=LEFT)
		navi_info.pack()

	def setupLeftColumn(self):
		locationIndicator = Label(
			leftFrame, 
			text="location: x:--\ny:--\norientation: z: --\nw: --",
			font=("Helvetica", 16),
			anchor=W, justify=LEFT)#Show Location
		twistIndicator = Label(
			leftFrame, text="-", 
			font=("Helvetica", 16),anchor=W, 
			justify=LEFT)#Show twist
		locationIndicator.pack()
		twistIndicator.pack(side=BOTTOM)

	def setupMidColum(self):
		midUpFrame=Frame(middleFrame)
		midUpFrame.pack(side=TOP)
		midMidFrame=Frame(middleFrame)
		midMidFrame.pack(side=TOP)
		midBotFrame=Frame(middleFrame)
		midBotFrame.pack(side=TOP)
		tempFrame = None
		#Set up all 9 direction buttons
		directionButList = []
		for ind in range(0,8):
			if ind < 3:
				tempFrame = midUpFrame
			elif ind < 6:
				tempFrame = midMidFrame
			elif ind < 9:
				tempFrame = midBotFrame
			tempButton = Button(tempFrame,text="", 
				fg="red",
				command=lambda:self.directionKeyCallbacks[ind]())
			tempButton.pack(side=LEFT)
			directionButList.append(tempButton)
		self.midButtonList = directionButList

	#The defualt call back for all direction button is just printing "Nothing"
	def directionButtonCallbackPlaceholder(self):
		print("Nothing")

	#this allows other to add a new button with a callback 
	def addRightColumnButton(self,button_text, button_callback):
		if len(rightButtonList) < 11:
			new_button = Button(rightFrame,text=button_text,
				fg="black",command=button_callback)
			new_button .pack()
			rightButtonList.append(new_button)
			print("\nAdd a new button :"+ button_text + 
				"\n  this is the button number "+str(current_number_button))
		else:
			print("There are 10 buttons already, which is the maximum.")
	


	def disableAllRightButtons(self):
		for but in rightButtonList:
			but["state"] = 'disable'

	def enableAllRightButtons(self):
		for but in rightButtonList:
			but["state"] = 'normal'

	def keyReleased(self,event):
		print("will do something")

	def keyPressed(self,event):
		print "pressed", repr(event.char)
		if event.char == "w":
			self.pressMidButton(1)
		elif event.char == "a":
			self.pressMidButton(3)
		elif event.char == "s":
			self.pressMidButton(4)
		elif event.char == "d":
			self.pressMidButton(5)
		elif event.char == "x":
			self.pressMidButton(7)
		elif event.char == "1":
			pressRightButton(0)
		elif event.char == "2":
			pressRightButton(1)
		elif event.char == "3":
			pressRightButton(2)
		elif event.char == "4":
			pressRightButton(3)
		elif event.char == "\x1b":
			root.destroy()
			print("Exit.")

	def pressMidButton(self,index):
		self.disableAllRightButtons()
		self.midButtonList[index]["relief"] = "sunken"
		self.midButtonList[index].invoke()
		self.midButtonList[index]["state"] = 'disable'

	def pressRightButton(self,index):
		if index < len(self.rightButtonList):
			if self.rightButtonList[0]["state"] != 'disable':
				self.rightButtonList[0]["relief"] = "sunken"
				self.rightButtonList[0].invoke()
				self.disableAllLocationButton()
		else:
			print("There only "+len(rightButtonList)
				+" buttons, number "+index+" doesn't exist.")

	def spin(self):
		self.root.mainloop()
	


	
