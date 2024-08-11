from moviepy.editor import *
import io
import sys
import math
import PySimpleGUI  as sg
import ctypes, platform
import os
import time

"""
Writen by Rafał Piątek.
TODO #1: Code is quite junky sometimes. There are some comments inside code written in Polish. 

"""


#DPI Awarness for better UI scaling for high resolution screens.
if int(platform.release()) >= 8:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)




def CheckVideo(VideoPath):
 
    def ifFrameBlack(img,height_marks=5,width_marks=5):
        """
        This function takes image array, and checks grid of pixels (determaind by height_marks & width_marks).
        If every pixel of that grid is black (value [0,0,0]) it means that most likely whole frame is black.
        Returns bool -> False if NOT black pixel were detected. True if ALL pixels are pure black.

        Parameters
        -----
        img: VideoFileFrame pixel array (moviepy library)
            Image frame from a viedo or photo.

        height_marks: int (optional)
            How many verical pixels should be skipped. Must be > 0.
            (more info above)

        widrh_marks: int (optional)
            How many horizontal pixels should be skipped. Must be > 0.
            (more info above)

        Raises/Asserts
        -----
        img: Asserts check if it's really 2D array and if it really is long enough.

        height_marks/width_marks: Asserts check if ints are greater than zero

        
        """
        assert len(img)>1, "img lenght is too short"
        assert len(img[0])>1,"img is not a 2D array"
        
        assert height_step>0, "height_step is not > 0"
        assert width_step>0,  "width_step is not > 0"

        height=len(img)   #powinno wynieść 1080 dla FHD
        width=len(img[0]) #powinno wynieść 1920 dla FHD
        height_step=math.floor(height/height_marks)
        width_step=math.floor(width/width_marks)

        for hPix in range(height_marks):
            for wPix in range(width_marks):
                pix=img[hPix*height_step][wPix*width_step]

                if not (pix[0]==0 and pix[1]==0 and pix[2]==0):
                    return False

        return True

    try:
        #próbuje otworzyć film
        video=VideoFileClip(VideoPath)

        frameRate=video.fps
        videoLenght=video.duration

        #lista wszystkich klatek
        allframes=math.floor(videoLenght*frameRate)

    except:
        raise NotImplementedError("Error while opening video")

    output=[] #lista końcowa z info o czarnych klatkach

    #dla każdej klatki filmu
    for frame in range(allframes):

        img=io.BytesIO() #pojemnik BytesIO (zeby wszystko było w RAMie a nie na SSD duuh...)
        img=video.get_frame(frame)

        yield ["frame",frame,allframes] #generator do sprawdzenia dowolnej klatki czy jest czarna

        if ifFrameBlack(img): #dla czarnej klatki
            yield ["progress",
                   "Klatka {} jest czarna, {}:{} z {}:{}".format(frame, math.floor(math.floor(frame / frameRate) / 60),
                                                               math.floor(frame / frameRate) % 60,
                                                               math.floor(math.floor(allframes / frameRate) / 60),
                                                               math.floor(allframes / frameRate) % 60)]
            output.append("Czarna klatka w {}:{} (MIN:SEK)".format(math.floor(math.floor(frame/frameRate)/60),math.floor(frame/frameRate)%60))
        else: #dla nie czarnej klatki
            yield ["progress",
                   "Klatka {} nie jest czarna, {}:{} z {}:{}".format(frame, math.floor(math.floor(frame / frameRate) / 60),
                                                                 math.floor(frame / frameRate) % 60,
                                                                 math.floor(math.floor(allframes / frameRate) / 60),
                                                                 math.floor(allframes / frameRate) % 60)]
    yield ["end",output]


def UI_runner():

    sg.theme("DarkGrey14") #set UI theme to DarkGrey. It just looks nice ^^

    #wybieranie pliku
    layout=[[sg.In() ,sg.FileBrowse(button_text='Wybierz plik',file_types=(("Plik Video", "*.mp4"),))]]
    window=sg.Window("Znajdowanie czarnych klatek, wybierz plik", layout, keep_on_top=True)

    while True:
        event, values = window.read(timeout=1000)
        if os.path.isfile(values[0]):
            videopath=values[0]
            break
    window.close()

    print("Wybrano plik {}".format(videopath))

    #Analizowanie pliku
    layout = [[sg.Text('Rozpoczynanie analizy pliku',size=(80, 2),key='text')],
              [sg.ProgressBar(1, orientation='h', size=(80, 40), key='progress')],
              ]


    window = sg.Window('Analizowanie filmu', layout,).Finalize()
    progress_bar = window.FindElement('progress')

    for pr in CheckVideo(videopath):
        #This loop updates UI for every video selected before while processing

        if(pr[0]=="progress"):
            window['text'].update(pr[1])

        if(pr[0]=="frame"):
            progress_bar.UpdateBar(pr[1], pr[2])

        if(pr[0]=="end"):
            if len(pr[1])<1:
                out=["Film nie ma czarnych klatek :)"]
            else:
                out=pr[1]
            break


    window.close()

    finalout=""
    for ele in out:
        finalout+=ele


    #Wyświetlenie pliku
    layout = [[sg.Text(finalout,size=(80, len(out)),key='text2')]
              ]
    window = sg.Window('Analizowanie filmu', layout).Finalize()


    #Program loop (so it won't close after just one video processing)
    while True:
        event, values = window.read(timeout=1000)
        print(event)
        if event==None:
            window.close()
            break


if __name__ == '__main__':
    UI_runner()




