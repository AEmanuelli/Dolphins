from __future__ import print_function
import cv2
import numpy as np
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import tkinter as tk
import moviepy.editor as mp
from moviepy.editor import *
import matplotlib.pyplot as plot
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def juxtapose_images(video_path, image_list, instant_list, output_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    image_index = 0
    for i in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        ret, frame = cap.read()
        if ret:
            if image_index < len(instant_list) and i == (instant_list[image_index] - 1):
                # Si l'instant correspond à l'un des instants spécifiés, juxtapose l'image au centre de la frame
                img_path = image_list[image_index]
                img = cv2.imread(img_path)
                x_offset = int((frame_width - img.shape[1]) / 2)
                y_offset = int((frame_height - img.shape[0]) / 2)
                frame[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img
                image_index += 1
            else:
                # Si l'instant ne correspond pas à un instant spécifié, écrire la frame d'origine dans la nouvelle vidéo
                out.write(frame)
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()



video_path = '/home/alexis/Desktop/output.mp4'
image =  "/home/alexis/Documents/GitHub/Dolphins/DNN_whistle_detection/images_/Exp_01_Feb_2024_1145_channel_0.wav-5.2.jpg"
images = [
    image, image
]
instants = [1, 4]  # Instants en secondes pour chaque image
output_path = '/home/alexis/Desktop/test/final_output_with_images.mp4'



class DolphinVideo:

    def __init__(self, path_to_video):
        # initialize the root window
        self.window = tk.Tk()
        self.window.title("Video_Player")
        self.window.geometry("1100x700")
        self.frame_number=0
        self.picture_label = tk.Label(self.window,  relief=tk.RIDGE)
        self.picture_label.grid(row=0, column=0)
        self.spectro=tk.Label(self.window, relief=tk.RIDGE)
        self.spectro.grid(row=1, column=0)
        
        menubar = Menu(self.window)
        self.window.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.open_file)
        menubar.add_cascade(label="File", menu=fileMenu)
        
        self.but_play=tk.Button(self.window, text="Play",width=12,height=1,borderwidth=0,command=self.toggle1, relief="raised", state="normal", bg="red", activebackground="red", repeatdelay=1)
        self.but_play.grid(row=3, column=3)
        
        self.delay = 15   # ms

        self.window.mainloop()


    def open_file(self):
        self.pause = False
        self.filename  = filedialog.askopenfilename(title="Select file", filetypes=(("MP4 files", "*.mp4"),("WMV files", "*.wmv"), ("AVI files", "*.avi")))
        print(self.filename)
        
        my_clip = VideoFileClip(self.filename)
        self.audio=my_clip.audio.to_soundarray()
        self.audio_length=len(self.audio)
        print(self.audio_length)
           
        self.cap = cv2.VideoCapture(self.filename)
        self.total_frames=int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(self.total_frames)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        print(self.fps)
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 1)
        sucess, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        self.imgtk = ImageTk. PhotoImage(image=img)
        self.picture_label.config(image=self.imgtk)
        
        # slider
        self.btn_frame=Scale(self.window, from_=0, to=self.total_frames, length=700, tickinterval=0, orient=HORIZONTAL, command=self.frame_video)
        self.btn_frame.grid(row=2, column=0, columnspan=2)
        
        # SPECTROGRAM
        self.fig = Figure(figsize=(14, 2), dpi=96)
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.audio[:,1])
        self.line,=self.ax.plot([0,0],[-1,1],'c') 
        self.ax.plot([1000, 1000],[-1, 1],'r-',lw=2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().grid(row=1,column=0)
        self.canvas.draw()


    def play_video(self):
        if self.pause:
            self.frame_number=self.frame_number-1
        else:
            self.btn_frame.set(self.frame_number)
            self.window.after(2, self.play_video) 
            self.frame_number = self.frame_number + 1
            
    def frame_video(self, event):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(event))
        sucess, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        self.imgtk = ImageTk.PhotoImage(image=img)
        self.picture_label.config(image=self.imgtk)
        self.frame_number=int(event)
        self.line.set_xdata([self.frame_number*1472,self.frame_number*1472])
        self.canvas.draw_artist(self.line)
        self.canvas.blit(self.fig.bbox)
        self.canvas.flush_events()
        self.ax.clear()
        
    def toggle1(self):
        if self.but_play.config('text')[-1] =='Pause':
            self.but_play.config(text='Play', bg="green",activebackground="green",textvariable=0)
            self.pause = False 
        else:
            self.pause = True  
            self.but_play.config(text='Pause', bg="red",activebackground="red",textvariable=1)

    def add_images_to_video(self, image_paths, instants, output_path):
        video = VideoFileClip(self.filename)
        img_clips = [ImageClip(img_path).set_duration(0.1) for img_path in image_paths]
        for img_clip, instant in zip(img_clips, instants):
            img_clip = img_clip.set_start(instant).set_position(('center', 'center'))
            video = video.set_audio(self.audio)
            video = CompositeVideoClip([video, img_clip])
        video.write_videofile(output_path, codec='libx264', fps=video.fps)

# Create an instance of DolphinVideo
ph = DolphinVideo(video_path)
# Add images to the video
image_paths = images
instants = [5, 10]  # Instants en secondes
ph.add_images_to_video(image_paths, instants, output_path)
