import cv2
import numpy as np
from skimage import io
from PIL import ImageDraw  
import PIL.Image
import os
from tkinter import messagebox as mg
from tkinter import filedialog as fd
from tkinter import * 
import random

frametimes = 300
width = 10  
file= ""
 
def DrawImage():
	global file, width, frametimes
	try:
		width = int(WidthLInput.get())
		frametimes = int(NLInput.get())
	except:
		mg.showinfo(title= "info", message="You provided an invalid width or frametimes, the defaults will be used instead")
	if(file != ""):

		video = cv2.VideoCapture(file)
		currentframe = 0
		actualframee = 0
		print("capturing frames.... this may take a second")
		while(True): 
			print("frame: " + str(currentframe))
			ret,frame = video.read() 

			if ret: 
				if (actualframee % frametimes == 0):
					name = 'Frames/frame' + str(currentframe) + '.jpg'

					cv2.imwrite(name, frame) 
					currentframe += 1
				actualframee += 1
			else: 
				break
		video.release() 
		cv2.destroyAllWindows()




		height = currentframe

		#imgnw  = Image.new( mode = "RGB", size = (width, height))
		imgnw2  = PIL.Image.new( mode = "RGB", size = (width, height))

		for i in range(currentframe):
			print("loading... drawing line: " + str(i))	
			img = cv2.imread('Frames/frame' + str(i) + '.jpg')

			avg_color_per_row = np.average(img, axis=0)
			avg_color = np.average(avg_color_per_row, axis=0)
			"""
			pixels = np.float32(img.reshape(-1, 3))

			n_colors = 5
			criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
			flags = cv2.KMEANS_RANDOM_CENTERS

			_, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
			_, counts = np.unique(labels, return_counts=True)

			dominant = palette[np.argmax(counts)]


			img1 = ImageDraw.Draw(imgnw)  
			shape = [(0, i), (width, i)]
			img1.line(shape, fill = (np.uint8(dominant[2]), np.uint8(dominant[1]), np.uint8(dominant[0])), width = 0)
			print("dom : " + str((np.uint8(dominant[2]), np.uint8(dominant[1]), np.uint8(dominant[0]))))
			"""
			img1 = ImageDraw.Draw(imgnw2)  
			shape = [(0, i), (width, i)]
			img1.line(shape, fill = (np.uint8(avg_color[2]), np.uint8(avg_color[1]), np.uint8(avg_color[0])), width = 0)



		#imgnw.show()
		splits = file.split("/")
		lastel = splits[-1].split(".")
		val = lastel[0] + " lined image of every " + frametimes + " frame/s"
		imgnw2.save( "results/" + val + ".jpg") 
		imgnw2.show()
		print("done! saved as: " + val)
	else:
		mg.showerror(title="Error", message="You need to select a video!")	

def OpenFile():
	global file
	filetypes = (
        ('video files', '*.mp4'),
        ('All files', '*.*')
    )
	file = fd.askopenfilename(title='Open a file', filetypes=filetypes)
	file = file.replace("\\", "/")
	mg.showinfo(title="selected vid", message="file selected: " + file)



top = Tk()   
top.geometry("500x300")  
top.title("Video to image")
    


# the label for width  
widthL = Label(top, 
                  text = "Width").place(x = 40,
                                           y = 60)  
    
# the label for numberoflines  
NLL = Label(top, 
                      text = "Increments between frames").place(x = 40,
                                               y = 100)  

select_button = Button(top, 
                       text = "select video", command=OpenFile).place(x = 40,
                                              y = 140)
    
submit_button = Button(top, 
                       text = "Submit", command=DrawImage).place(x = 40,
                                              y = 180)
notelabel = Label(top, text="Note, images height will be: (the video time in seconds * framerate) / frametimes ").place(x=40, y=220)                       

WidthLInput = Entry(top, width = 30)
WidthLInput.place(x = 210, y = 60)      
NLInput = Entry(top, width = 30)
NLInput.place(x = 210, y = 100)  

 
top.mainloop() 


