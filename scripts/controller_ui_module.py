#This class is for setting up UI only
from Tkinter import * #Python ui lib

class UiControllerModule:
	
	def _init_(self)
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
		#Right Column for Adding nav goal

		self.setupDownRow()

		self.setupLeftColumn()

		self.directionKeyCallbacks = [self.directionButtonCallbackPlaceholder] * 9

		self.setupLeftColumn(directionKeyCallbacks)
		#This is a list of all callbacks for 9 buttons on the controller, this number 9 shouldn't be changed
		#The functions in the list is meant to be changed, but has to have two parameters
		#self and an integer
		#Each func in the list corresponds to one button
		#0 1 2
		#3 4 5
		#6 7 8

		self.current_number_button = 0

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
		for ind in range(0,8):
			if ind < 3:
				tempFrame = midUpFrame
			else if ind < 6:
				tempFrame = midMidFrame
			else if ind < 9:
				tempFrame = midBotFrame
			tempButton = Button(tempFrame,text="", 
				fg="red",
				command=lambda:self.directionKeyCallbacks[ind]())
			tempButton.pack(side=LEFT)

	#The defualt call back for all direction button is just printing "Nothing"
	def directionButtonCallbackPlaceholder(self):
		print("Nothing")

	#this allows other to add a new button with a callback 
	def addRightColumnButton(button_text, button_callback)
		if current_number_button < 11:
			new_button = Button(rightFrame,text=button_text, fg="black",command=button_callback)
			new_button .pack()
			self.current_number_button += 1
			print("\nAdd a new button :"+ button_text + 
				"\n  this is the button number "+str(current_number_button))
		else:
			print("There are 10 buttons already, which is the maximum.")
	



	


	
