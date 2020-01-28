from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import tkinter as tk


class Window(Frame):
    #global variables

	imagesize=350 #defines size of the two displayed images
	

    # Define settings upon initialization.
	def __init__(self, master=None):
		Frame.__init__(self, master)                 
		self.master = master
		self.init_window()
		
		#arguments:
		self.offsetx=0		# X-Offset in Picture
		self.offsety=0		# Y-Offset in Picture
		self.oResx=0		# Original Resolution
		self.oResy=0		# Original Resolution
		self.outResx=0		# Output Resolution
		self.outResy=0		# Output Resolution
		self.canSel=[0]*3	#need to clear canvas selection rectangle
		
		
		#self.browse_files() #Autostart 

    #Creation of init_window
	def init_window(self):
        # ---------------- Title + Initialisazion -----------------------
        # changing the title of our master widget      
		self.master.title("E+H Image Assembler")
        # allowing the widget to take the full space of the root window
		self.pack(fill=BOTH, expand=1)		
		
		#----------------- Big Canvas ----------------------
		self.canv=tk.Canvas(self,width=890,height=630, background="white")
		self.canv.place(x=140, y=40)
		self.canv.bind("<Button-1>",self.selectPicture)
		#----------------- Settings right ------------------
		label= Label(text="Settings:")
		label.place(x=1040, y=40)
		
		label= Label(text="Folder:")
		label.place(x=1040, y=70)
		self.folderlabel= Label(text="choose path")
		self.folderlabel.place(x=1110, y=70)
		
		label= Label(text="Pictures:")
		label.place(x=1040, y=90)
		self.numPiclabel= Label(text="")
		self.numPiclabel.place(x=1110, y=90)
		
		label= Label(text="Resolution:")
		label.place(x=1040, y=110)
		self.reslabel=Label(text="")
		self.reslabel.place(x=1110, y=110)
		
		
		

		label= Label(self,text="Offset X:")
		label.place(x=1040, y=170)
		self.offx = StringVar()
		self.offx.set(0)
		self.offsetxlabel=Label(self, textvariable = self.offx)
		self.offsetxlabel.place(x=1110, y=170)
		
		label= Label(text="Offset Y:")
		label.place(x=1040, y=190)
		self.offy = StringVar()
		self.offy.set(0)
		self.offsetylabel=Label(self, textvariable = self.offy)
		self.offsetylabel.place(x=1110, y=190)
		
		label= Label(text="Output res:")
		label.place(x=1040, y=210)
		self.outres=Label(text="")
		self.outres.place(x=1110, y=210)
		
		label= Label(text="redundanz:")
		label.place(x=1040, y=230)
		self.redundanz=Label(text="")
		self.redundanz.place(x=1110, y=230)
		
        #-------------------- Buttons -------------------------------
		# Browse ----------------------------------
		self.nextButton = Button(self, text="Browse",command=self.devTry, state=NORMAL)
		self.nextButton.place(x=1110, y=130)
		#----------------------------------------------------------------
		# Offset ------------------------------------
		self.offsetButton = Button(self, text="Get Offset",command=self.create_window, state=DISABLED)
		self.offsetButton.place(x=1110, y=250)
		#----------------------------------------------------------------
		# process folder ------------------------------------
		self.folderButton = Button(self, text="Process Folder",command=self.create_all_picture, state=DISABLED)
		self.folderButton.place(x=1110, y=680)	
		# Next ------------------------------------
		self.fileButton = Button(self, text="Process File",command=self.create_one_picture, state=DISABLED)
		self.fileButton.place(x=1200, y=680)	

		
		#------------------- Progressbar --------------------------------
		label=Label(text="Progress: ")
		label.place(x=1040, y=290)
		self.progresstext=Label(self)
		self.progresstext.place(x=1110, y=290)
		self.progress= Progressbar(root, orient=HORIZONTAL, length = 230, mode='determinate')
		self.progress.place(x=1040, y=310)
		self.progress['value']=0
		
		
		#------------------- SpinBoxes Top and left ---------------------------------------
		max=10 #Max Values of Spinboxes
		
		#top Spin Box
		buttonSubtract = Button(self,text="-",command=lambda: self.changeAllCol(-1))
		buttonSubtract.place(x=370,y=10, width=20, height=20)
		self.formCol = Spinbox(self,from_=1,to=max,state=DISABLED)
		self.formCol.set(5)
		self.formCol.place(x=400, y=10, width=50,height=20)
		buttonadd = Button(self,text="+",command=lambda: self.changeAllCol(1))
		buttonadd.place(x=460,y=10, width=20, height=20)
		
		labelOffset = Label(self,text="Offset:")
		labelOffset.place(x=10, y=10)
		labelCols = Label(self,text="Columns:")
		labelCols.place(x=80, y=10)
		
		#create Side Spin Boxes
		self.formOffs=[""]
		self.formCols=[]
		for i in range(0,9):
			self.formOffs.append("")
			self.formOffs[i] = Spinbox(self,from_=0,to=max, command=self.place_Pictures)
			self.formOffs[i].set(0)
			self.formOffs[i].place(x=10, y=60+70*i, width=50,height=20)
			self.formCols.append("")
			self.formCols[i] = Spinbox(self,from_=1,to=max, command=self.place_Pictures)
			self.formCols[i].set(5)
			self.formCols[i].place(x=80, y=60+70*i, width=50,height=20)
		

	def selectPicture(self,event):
		self.selPic=[0]*3;
		
		row=int(event.y/(self.images.thumbSizeY+10))
		column=int(event.x/(self.images.thumbSizeX+10))
		print("row|column",row,column)
		for i in range(0,row):
			colInRow=int(self.formCols[i].get())
			self.selPic[0]=self.selPic[0]+colInRow
		print("tilnow:",self.selPic)
		if row%2: # row backwards
			colInRow=int(self.formCols[row].get())
			#save picture Numbers
			
			self.selPic[2]=self.selPic[0]+colInRow+column
			self.selPic[0]=self.selPic[0]+(colInRow-(column+1))
			self.selPic[1]=self.selPic[0]+1
			print("îf")
		else:#row forwards
			colInRow=int(self.formCols[row].get())
			self.selPic[2]=self.selPic[0]+colInRow+(int(self.formCols[row+1].get())-(column+1))
			self.selPic[0]=self.selPic[0]+column
			self.selPic[1]=self.selPic[0]-1
			print("else")
			print("colInRow:",colInRow)
		print("picture0",self.selPic[0])
		print("picture1",self.selPic[1])
		print("picture2",self.selPic[2])
		
		#delete last selection
		self.canv.delete(self.canSel[0])
		self.canv.delete(self.canSel[1])
		self.canv.delete(self.canSel[2])
		
		#draw rectangle
		x=self.images.thumbSizeX	
		y=self.images.thumbSizeY
		posx=column*(x+10)
		posy=row*(y+10)
		self.canSel[0] =self.canv.create_rectangle(posx-5, posy-5, posx+x+5, posy+y+5,outline='red')
		self.canSel[1] =self.canv.create_rectangle(posx-x-15, posy-5, posx-5, posy+y+5,outline='red')
		self.canSel[2] =self.canv.create_rectangle(posx-5, posy+y+5, posx+x+5, posy+2*y+15,outline='red')
		
		#activate next step (choose Offset)
		self.offsetButton['state']=NORMAL
	
		


	def create_window(self):
		#create new Window
		window = tk.Toplevel(root)
		geometry="960x720"
		window.geometry(geometry)
		
		imagesize=350 #scale for Imagesize(height)
		imagesizey=int((imagesize*self.images.pictures[0].width())/self.images.pictures[0].height())
		self.lastcross1x=0
		self.lastcross1y=0
		self.lastcross2x=0
		self.lastcross2y=0
		self.lastcross3x=0
		self.lastcross3y=0	


		
		#create window UI
		self.canvas1=Canvas(window,width=imagesizey, height=imagesize)
		self.canvas1.place(x=5,y=10)		
		self.canvas2=Canvas(window,width=imagesizey, height=imagesize)
		self.canvas2.place(x=imagesizey+10,y=10)		
		self.canvas3=Canvas(window,width=imagesizey, height=imagesize)
		self.canvas3.place(x=imagesizey+10,y=imagesize+15)
		
		#---------- Info Image 1
		tmp=Label(window,text="Image1:")
		tmp.place(x=10,y=imagesize+30)
		self.img1x = StringVar()
		self.img1x.set(0)
		window.label1x = Label(window, textvariable = self.img1x)
		window.label1x.place(x=70, y=imagesize+30)
		
		self.img1y = StringVar()
		self.img1y.set(0)
		label1y = Label(window, textvariable = self.img1y)
		label1y.place(x=100, y=imagesize+30)		

		#---------- Info Image 2
		tmp=Label(window,text="Image2:")
		tmp.place(x=10,y=imagesize+50)
		self.img2x = StringVar()
		self.img2x.set(0)
		label2x = Label(window, textvariable = self.img2x)
		label2x.place(x=70, y=imagesize+50)
		
		self.img2y = StringVar()
		self.img2y.set(0)
		label2y = Label(window, textvariable = self.img2y)
		label2y.place(x=100, y=imagesize+50)		

		#---------- Info Image 3
		tmp=Label(window,text="Image3:")
		tmp.place(x=10,y=imagesize+70)
		self.img3x = StringVar()
		self.img3x.set(0)
		label3x = Label(window, textvariable = self.img3x)
		label3x.place(x=70, y=imagesize+70)
		
		self.img3y = StringVar()
		self.img3y.set(0)
		label3y = Label(window, textvariable = self.img3y)
		label3y.place(x=100, y=imagesize+70)		
		
		#---------- Info Offset x
		tmp=Label(window,text="Offset X:")
		tmp.place(x=10,y=imagesize+100)

		self.offsetbox = Spinbox(window,from_=0,to=500, command=lambda:self.activateButton(None))
		self.offsetbox.place(x=70, y=imagesize+100,width=50,height=20)
		self.offsetbox.bind("<Key>",self.activateButton)
		
		#---------- Info Offset y
		tmp=Label(window,text="Offset Y:")
		tmp.place(x=10,y=imagesize+120)

		self.offsetboy = Spinbox(window,from_=0,to=500, command=lambda:self.activateButton(None))
		self.offsetboy.place(x=70, y=imagesize+120,width=50,height=20)
		self.offsetboy.bind("<Key>",self.activateButton)
		
		#---------- Button OK
		tmp=Button(window,text="OK",command=window.destroy)
		tmp.place(x=10, y=imagesize+160)

		
		#get clicked Pictures
		
		image=Image.open(self.images.files[self.selPic[1]])
		image=image.crop((800,600,1600,1200))	#lower right hand side 
		image=image.resize((imagesizey,imagesize), Image.ANTIALIAS)
		self.image1 = ImageTk.PhotoImage(image)
		self.canvas1.create_image(0,0,anchor=NW,image=self.image1)
		#mouseclick eventhandler
		self.canvas1.bind("<Button-1>",self.printcoords)
		
		image=Image.open(self.images.files[self.selPic[0]])
		image=image.crop((0,600,800,1200))	#lower left hand side
		image=image.resize((imagesizey,imagesize), Image.ANTIALIAS)
		self.image2 = ImageTk.PhotoImage(image)		
		self.canvas2.create_image(0,0,anchor=NW,image=self.image2)
		#mouseclick eventhandler
		self.canvas2.bind("<Button-1>",self.printcoords2)
		
		image=Image.open(self.images.files[self.selPic[2]])
		image=image.crop((0,0,800,600))	#upper left hand side
		image=image.resize((imagesizey,imagesize), Image.ANTIALIAS)
		self.image3 = ImageTk.PhotoImage(image)				
		self.canvas3.create_image(0,0,anchor=NW,image=self.image3)
		#mouseclick eventhandler
		self.canvas3.bind("<Button-1>",self.printcoords3)
		
	
	def calculateOffset(self):
		#get shrinked sizes
		x1=int(self.img1x.get())
		x2=int(self.img2x.get())
		x3=int(self.img3x.get())
		y1=int(self.img1y.get())
		y2=int(self.img2y.get())
		y3=int(self.img3y.get())
		#original sizes
		if x1 > 0 and x2 > 0 and x3 > 0:
			x1=int((800*x1)/466)
			x2=int((800*x2)/466)
			x3=int((800*x3)/466)
			y1=int((600*y1)/350)
			y2=int((600*y2)/350)
			y3=int((600*y3)/350)
		 
			#calculate offset:
			self.offsetx=int(((800-x1)+x2)/2)
			self.offsety=int(((600-y2)+y3)/2)

			#Set pick window
			self.offsetbox.set(self.offsetx)
			self.offsetboy.set(self.offsety)
			
			#set main Window
			self.offx.set(self.offsetx)
			self.offy.set(self.offsety)
			
			self.activateButton(None)

			
	def activateButton(self,event):
		self.offsetx=int(self.offsetbox.get())
		self.offsety=int(self.offsetboy.get())
		
		if self.offsetx and self.offsety:
			self.offx.set(self.offsetx)
			self.offy.set(self.offsety)
			#activate buttons
			self.folderButton['state']=NORMAL
			self.fileButton['state']=NORMAL
			self.calculateNew()
			
	def calculateNew(self):
		#get max width/height
		cols=0
		rows=9 #max until changed
		count=0
		i=0
		while i<=8:
			thiscol=int(self.formCols[i].get())	# Nr. pictures in Col i
			count=count+thiscol					# count pictures
			if thiscol>cols:
				cols=thiscol
			if count>=self.images.numPics:
				rows=i
			i=i+1

		self.outResx=cols*(self.oResx-2*self.offsetx)
		self.outResy=(rows+1)*(self.oResy-2*self.offsety)
		self.outres['text']=str(self.outResx)+" x"+str(self.outResy)
		sizeo=(self.oResx*self.oResy)*rows*cols
		sizeout=(self.outResx*self.outResy)
		redundancy=int((100*sizeout)/sizeo)
		self.redundanz['text']=str(100-redundancy)+"%"
		
	#function to be called when mouse is clicked on Picture
	def printcoords(self,event):
        #outputting x and y coords to console
		self.img1x.set(event.x)
		self.img1y.set(event.y)
		#clear the old cross (last transaction UID)
		self.canvas1.delete(self.lastcross1x)
		self.canvas1.delete(self.lastcross1y)
		#draw new cross, save transaction UID
		self.lastcross1x= self.canvas1.create_line(event.x-20, event.y, event.x+20, event.y,fill='red')
		self.lastcross1y= self.canvas1.create_line(event.x, event.y-20, event.x, event.y+20,fill='red')
		self.calculateOffset()

	def printcoords2(self,event):
        #outputting x and y coords to console
		self.img2x.set(event.x)
		self.img2y.set(event.y)
		#clear the old cross (last transaction UID)
		self.canvas2.delete(self.lastcross2x)
		self.canvas2.delete(self.lastcross2y)
		#draw new cross, save transaction UID
		self.lastcross2x= self.canvas2.create_line(event.x-20, event.y, event.x+20, event.y,fill='red')
		self.lastcross2y= self.canvas2.create_line(event.x, event.y-20, event.x, event.y+20,fill='red')		
		self.calculateOffset()

	def printcoords3(self,event):
        #outputting x and y coords to console
		self.img3x.set(event.x)
		self.img3y.set(event.y)
		#clear the old cross (last transaction UID)
		self.canvas3.delete(self.lastcross3x)
		self.canvas3.delete(self.lastcross3y)
		#draw new cross, save transaction UID
		self.lastcross3x= self.canvas3.create_line(event.x-20, event.y, event.x+20, event.y,fill='red')
		self.lastcross3y= self.canvas3.create_line(event.x, event.y-20, event.x, event.y+20,fill='red')
		self.calculateOffset()
		
		

	def place_Pictures(self):
		self.canv.delete('all')
		
		cols=int(self.formCol.get())#---------------------------nicht gebraucht?
		imgx=self.images.thumbSizeX
		imgy=self.images.thumbSizeY

		i=0
		row=0
		column=0
		backwardsCount=0
		x=10+imgx #stepsize x
		y=10+imgy #stepsize y
		while i<self.images.numPics and row<9: #no more pictures or no more lines
			#get Offset from SpinBox
			xOff=int(self.formOffs[row].get())	
			
			#draw Image
			if row%2: 	#count backwards
				colInRow=int(self.formCols[row].get())-1
				newi=i+colInRow-backwardsCount
				backwardsCount=backwardsCount+2
				self.canv.create_image((column+xOff)*x , row*y,anchor=NW,image=self.images.thumbnails[newi])
			else:		#count forwards
				self.canv.create_image((column+xOff)*x , row*y,anchor=NW,image=self.images.thumbnails[i])

			#calculate next row/column
			if column >= int(self.formCols[row].get())-1: #check against row length(Spinbox)
				row=row+1
				column=0
				backwardsCount=0
			else:
				column=column+1
			i=i+1
	
	def create_one_picture(self):
		self.progresstext['text']="0/1"	
		root.update_idletasks() 		
		self.create_picture()
		self.progresstext['text']="1/1"
		self.progress['value']=100
		root.update_idletasks() 
		os.startfile(self.images.path)
		
	def create_all_picture(self):
		self.progresstext['text']=""	
		self.progress['value']=0
		root.update_idletasks() 	
		
		directories = []
		path =  filedialog.askdirectory(title = "Select main folder",)
		count=0
		# list directories
		for d in os.listdir(path):
			if os.path.isdir(os.path.join(path, d)):
				directories.append(os.path.join(path, d))
		for d in directories:
			self.images=Pictures()	# create new instance
			self.images.setPath(d) # set new path
			self.images.loadPath()	# read filepaths
			self.create_picture()
			count=count+1
			self.progresstext['text']=str(count)+"/"+str(len(directories))
			self.progress['value']=int((100*count)/len(directories))
			root.update_idletasks() 
		os.startfile(self.images.path)
	def create_picture(self):
		i=0
		row=0
		column=0
		backwardsCount=0
		self.calculateNew() #update output resolution
		im= Image.new('RGB',(self.outResx,self.outResy),0xffffff) 
	
		x=self.oResx-2*self.offsetx #stepsize x
		y=self.oResy-2*self.offsety #stepsize y
		
		while i<self.images.numPics and row<9: #no more pictures or no more lines
			#get Offset from SpinBox
			xOff=int(self.formOffs[row].get())	
			
			#draw Image
			if row%2: 	#count backwards
				colInRow=int(self.formCols[row].get())-1
				newi=i+colInRow-backwardsCount
				backwardsCount=backwardsCount+2
				
				tmp=Image.open(self.images.files[newi])					# open 
				tmp=tmp.crop((self.offsetx,self.offsety,(self.oResx-self.offsetx),(self.oResy-self.offsety)))		# crop off offset
				im.paste(tmp, (((column+xOff)*x),(row*y)) )	# put in big image
				
			else:		#count forwards
				tmp=Image.open(self.images.files[i])					# open 
				tmp=tmp.crop((self.offsetx,self.offsety,(self.oResx-self.offsetx),(self.oResy-self.offsety)))		# crop off offset
				im.paste(tmp,((column)*x,row*y))	# put in big image

			#calculate next row/column
			if column >= int(self.formCols[row].get())-1: #check against row length(Spinbox)
				row=row+1
				column=0
				backwardsCount=0
			else:
				column=column+1
			i=i+1
		
		print("Foldername:",os.path.basename(self.images.path))
		im.save(os.path.join(self.images.path,os.path.basename(self.images.path)+"_fullimage.jpg"))

	## adds or subtract a column on every row
	def changeAllCol(self,direction):
		tmp=int(self.formCol.get())+direction
		if tmp < 1:
			tmp=1
		if tmp > 10:
			tmp=10
		self.formCol.set(tmp)
		
		
		for i in range(0,9):
			tmp=int(self.formCols[i].get())+direction
			if tmp < 1:
				tmp=1
			if tmp > 10:
				tmp=10
			self.formCols[i].set(tmp)
		self.place_Pictures()
		
	def devTry(self):
		self.images= Pictures()
		self.images.choosePath()
		self.images.loadPictures()
		self.images.loadThumbnails()
		self.place_Pictures()
		
		self.folderlabel['text']=self.images.path
		self.numPiclabel['text']=self.images.numPics
		self.oResx=self.images.pictures[0].width()
		self.oResy=self.images.pictures[0].height()
		imagesize=str(self.oResx)+" x"+str(self.oResy)
		self.reslabel['text']=imagesize
		
		#print("height: ",self.images.path)
		



class Pictures():
	def __init__(self, master=None):
		#init arguments
		self.thumbSizeX	= 80		# thumbnail Size
		self.thumbSizeY	= 60		# thumbnail Size
		self.numPics	= 0			# number of pictures in folder
		self.path		= 0			# main Path
		
		self.files		= []		# Image filepaths
		self.thumbnails	= []		# thumbnail images
		self.pictures	= []		# original images
	
	def choosePath(self):
		self.path =  filedialog.askdirectory(title = "Select folder",) #
		self.loadPath()
		
	def setPath(self,path):
		self.path=path
		self.loadPath()

	def loadPath(self):
		self.files = []
		maxFiles=200
		counter=0
		print("processing: ",self.path,"...")
      
		# r=root, d=directories, f = files
		for r, d, f in os.walk(self.path):
			for file in f:
				if '.jpg' in file :
					if not 'fullimage' in file:
						self.files.append(os.path.join(r, file))
						counter=counter+1
				if counter > maxFiles:
					print("Error Max Files reached (",maxFiles,")")
					return
		self.numPics=len(self.files)		
		
	def loadPictures(self):
		# create empty Arrays 
		self.pictures	=[0]*self.numPics
		
		for i in range(0,self.numPics):
			# open Image
			temp = Image.open(self.files[i])
			# save original Image file
			self.pictures[i] = ImageTk.PhotoImage(temp)
			
	def loadThumbnails(self):
		self.thumbnails	=[0]*self.numPics
		for i in range(0,self.numPics):
			# open Image
			temp = Image.open(self.files[i])
			# crop image for Thumbnail
			temp	= temp.resize((self.thumbSizeX, self.thumbSizeY), Image.ANTIALIAS)
			self.thumbnails[i] = ImageTk.PhotoImage(temp)	
			
#print("---------- running..... ----------")
# root window created.		
root = Tk()

#size of the main window
geometry="1280x720"
root.geometry(geometry)
#root.wm_iconbitmap('logo.ico')
#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()  