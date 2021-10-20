import json
from tkinter import *
from tkinter import constants

from numpy.lib.type_check import imag
from jsonHandler import getJsonObject
import jsonObject
from PIL import ImageTk, Image

def init():     

    mainloop()
    
def checkered(canvas, line_distance, increment):

    canvas.create_line(increment, increment, increment, canvas_height+increment, fill="#000000")
    canvas.create_line(increment, increment, canvas_width+increment, increment, fill="#000000")
    canvas.create_line(canvas_width+increment, increment, canvas_width+increment, canvas_height+increment, fill="#000000")
    canvas.create_line(increment, canvas_height+increment, canvas_width+increment, canvas_height+increment, fill="#000000")

    # vertical lines at an interval of "line_distance" pixel
    for x in range(line_distance,canvas_width,line_distance):
        canvas.create_line(x+increment, 0+increment, x+increment, canvas_height+increment, fill="#000000")
    # horizontal lines at an interval of "line_distance" pixel
    for y in range(line_distance,canvas_height,line_distance):
        canvas.create_line(0+increment, y+increment, canvas_width+increment, y+increment, fill="#000000")
    
    renderMapTiles()

def callback(event):
    xTile, yTile = getTile(event.x, event.y)
    x, y = getCoordinates(xTile, yTile)
    if(object.map[xTile][yTile] == 0):
        w.create_rectangle(x, y, x+object.sizeOfTile, y+object.sizeOfTile, fill="#7f8280")
        object.map[xTile][yTile] = 1
    else:
        w.create_rectangle(x, y, x+object.sizeOfTile, y+object.sizeOfTile, fill="#ffffff")
        object.map[xTile][yTile] = 0

    root.update()

def getTile(x, y):
    xTile = int((x - increment) / object.sizeOfTile)
    yTile = int((y - increment) / object.sizeOfTile)
    return xTile, yTile, 

def getCoordinates(x, y):
    return ((x * object.sizeOfTile) + increment),((y * object.sizeOfTile) + increment)

def getCoordinatesOfActor(x, y, size):
    return ((x * object.sizeOfTile) + increment + int(size/2)),((y * object.sizeOfTile) + increment + int(size/2))

def renderMapTiles():
    for i in range(len(object.map)):
        for j in range(len(object.map[0])):
            x, y = getCoordinates(i, j)
            if(object.map[i][j] == 1):
                w.create_rectangle(x, y, x+object.sizeOfTile, y+object.sizeOfTile, fill="#7f8280")
            else:
                w.create_rectangle(x, y, x+object.sizeOfTile, y+object.sizeOfTile, fill="#ffffff")

def moveActor(event):
    x = 0
    y = 0
    if(event.keysym == "Right" and object.actor["x"] < len(object.map)-1
    and object.map[object.actor["x"]+1][object.actor["y"]] != 1):
        object.actor["x"] = object.actor["x"] + 1
        x = x + 40
    elif(event.keysym == "Left" and object.actor["x"] > 0
    and object.map[object.actor["x"]-1][object.actor["y"]] != 1):
        object.actor["x"] = object.actor["x"] - 1
        x = x - 40
    elif(event.keysym == "Up" and object.actor["y"] > 0
    and object.map[object.actor["x"]][object.actor["y"]-1] != 1):
        object.actor["y"] = object.actor["y"] - 1
        y = y - 40
    elif(event.keysym == "Down" and object.actor["y"] < len(object.map[0])-1
    and object.map[object.actor["x"]][object.actor["y"]+1] != 1):
        object.actor["y"] = object.actor["y"] + 1
        y = y + 40
    
    xActor, yActor = getCoordinatesOfActor(object.actor["x"], object.actor["y"],object.sizeOfTile)
    w.move(actor, x, y)
    w.tag_raise(actor)

xActor = 0
yActor = 0
object: jsonObject.Json = getJsonObject("zadanie1.json")
increment = 6
root = Tk()
root.title("Zadanie 1")
root.configure(background='black')
canvas_width = object.x
canvas_height = object.y
w: Canvas = Canvas(root, 
            width=canvas_width+10,
            height=canvas_height+10)
            
w.bind("<Button-1>", callback)
root.bind("<Left>", lambda event: moveActor(event))
root.bind("<Right>", lambda event: moveActor(event))
root.bind("<Up>", lambda event: moveActor(event))
root.bind("<Down>", lambda event: moveActor(event))
w.pack()

checkered(w,object.sizeOfTile, increment)
xActor, yActor = getCoordinatesOfActor(object.actor["x"], object.actor["y"],object.sizeOfTile)
img= (Image.open("actor.png"))
actorSize = 25
resized_image= img.resize((actorSize,actorSize), Image.ANTIALIAS)
new_image= ImageTk.PhotoImage(resized_image)
actor = w.create_image(xActor, yActor, image=new_image)


#mainloop()