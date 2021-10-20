import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from tkinter import *

from jsonHandler import getJsonObject
import jsonHandler
import jsonObject
from PIL import ImageTk, Image

import json
import _thread


class Simulator(Node):
    
    def __init__(self):
        super().__init__('Simulator')
        self.publisher_ = self.create_publisher(String, 'sim_to_map', 10)
        self.subscription = self.create_subscription(
            String,
            'map_to_sim',
            self.listener_callback,
            10)
        self.subscription
        _thread.start_new_thread(rclpy.spin, (self,))
        msg = String()
        msg.data = "start"
        self.publisher_.publish(msg)
        self.move = False
        self.click = False 
        self.x = 0
        self.y = 0
        self.xActor = 0
        self.yActor = 0
        self.object: jsonObject.Json = None
        while(self.object is None):
            continue
        self.increment = 6
        self.root = Tk()
        self.root.title("Task 1")
        self.root.configure(background='black')
        self.canvas_width = self.object.x
        self.canvas_height = self.object.y
        self.w: Canvas = Canvas(self.root, 
                    width=self.canvas_width+10,
                    height=self.canvas_height+10)
                    
        self.w.bind("<Button-1>", lambda event: callback(event, self))
        self.root.bind("<Left>", lambda event: moveActor(event, self))
        self.root.bind("<Right>", lambda event: moveActor(event, self))
        self.root.bind("<Up>", lambda event: moveActor(event, self))
        self.root.bind("<Down>", lambda event: moveActor(event, self))
        self.w.pack()

        checkered(self,self.w,self.object.sizeOfTile, self.increment)
        self.xActor, self.yActor = getCoordinatesOfActor(self, self.object.actor["x"], self.object.actor["y"],self.object.sizeOfTile)
        self.img= (Image.open("actor.png"))
        self.actorSize = 25
        self.resized_image= self.img.resize((self.actorSize,self.actorSize), Image.ANTIALIAS)
        self.new_image= ImageTk.PhotoImage(self.resized_image)
        self.actor = self.w.create_image(self.xActor, self.yActor, image=self.new_image)
        
        mainloop()

    def listener_callback(self, msg):
        dict = json.loads(msg.data)
        object1 = jsonObject.Json(**dict)
        self.object = object1
        print("update")
        if self.move:
            self.w.move(self.actor, self.x, self.y)
            self.move = False
        if self.click:
            renderMapTiles(self)
            self.w.tag_raise(self.actor)
            self.click = False
            self.root.update()

def main(args=None):
    rclpy.init(args=args)
    
    simulator = Simulator()
    #_thread.start_new_thread()
    #_thread.start_new_thread(rclpy.spin, (simulator, ))
    
    rclpy.spin(simulator)

    simulator.destroy_node()
    rclpy.shutdown()

def checkered(self, canvas, line_distance, increment):

    canvas.create_line(increment, increment, increment, self.canvas_height+increment, fill="#000000")
    canvas.create_line(increment, increment, self.canvas_width+increment, increment, fill="#000000")
    canvas.create_line(self.canvas_width+increment, increment, self.canvas_width+increment, self.canvas_height+increment, fill="#000000")
    canvas.create_line(increment, self.canvas_height+increment, self.canvas_width+increment, self.canvas_height+increment, fill="#000000")

    # vertical lines at an interval of "line_distance" pixel
    for x in range(line_distance,self.canvas_width,line_distance):
        canvas.create_line(x+increment, 0+increment, x+increment, self.canvas_height+increment, fill="#000000")
    # horizontal lines at an interval of "line_distance" pixel
    for y in range(line_distance,self.canvas_height,line_distance):
        canvas.create_line(0+increment, y+increment, self.canvas_width+increment, y+increment, fill="#000000")
    
    renderMapTiles(self)

def callback(event, self):
    xTile, yTile = getTile(self, event.x, event.y)
    #x, y = getCoordinates(self, xTile, yTile)
    if(self.object.map[xTile][yTile] == 0):
        #self.w.create_rectangle(x, y, x+self.object.sizeOfTile, y+self.object.sizeOfTile, fill="#7f8280")
        self.object.map[xTile][yTile] = 1
    else:
        #self.w.create_rectangle(x, y, x+self.object.sizeOfTile, y+self.object.sizeOfTile, fill="#ffffff")
        self.object.map[xTile][yTile] = 0
        self.click = True
    publishMessage(self)

def getTile(self, x, y):
    xTile = int((x - self.increment) / self.object.sizeOfTile)
    yTile = int((y - self.increment) / self.object.sizeOfTile)
    return xTile, yTile, 

def getCoordinates(self, x, y):
    return ((x * self.object.sizeOfTile) + self.increment),((y * self.object.sizeOfTile) + self.increment)

def getCoordinatesOfActor(self,x, y, size):
    return ((x * self.object.sizeOfTile) + self.increment + int(size/2)),((y * self.object.sizeOfTile) + self.increment + int(size/2))

def renderMapTiles(self):
    for i in range(len(self.object.map)):
        for j in range(len(self.object.map[0])):
            x, y = getCoordinates(self, i, j)
            if(self.object.map[i][j] == 1):
                self.w.create_rectangle(x, y, x+self.object.sizeOfTile, y+self.object.sizeOfTile, fill="#7f8280")
            else:
                self.w.create_rectangle(x, y, x+self.object.sizeOfTile, y+self.object.sizeOfTile, fill="#ffffff")

def moveActor(event, self):
    self.x = 0
    self.y = 0
    if(event.keysym == "Right" and self.object.actor["x"] < len(self.object.map)-1
    and self.object.map[self.object.actor["x"]+1][self.object.actor["y"]] != 1):
        self.object.actor["x"] = self.object.actor["x"] + 1
        self.x = self.x + 40
    elif(event.keysym == "Left" and self.object.actor["x"] > 0
    and self.object.map[self.object.actor["x"]-1][self.object.actor["y"]] != 1):
        self.object.actor["x"] = self.object.actor["x"] - 1
        self.x = self.x - 40
    elif(event.keysym == "Up" and self.object.actor["y"] > 0
    and self.object.map[self.object.actor["x"]][self.object.actor["y"]-1] != 1):
        self.object.actor["y"] = self.object.actor["y"] - 1
        self.y = self.y - 40
    elif(event.keysym == "Down" and self.object.actor["y"] < len(self.object.map[0])-1
    and self.object.map[self.object.actor["x"]][self.object.actor["y"]+1] != 1):
        self.object.actor["y"] = self.object.actor["y"] + 1
        self.y = self.y + 40
    
    self.xActor, self.yActor = getCoordinatesOfActor(self,self.object.actor["x"], self.object.actor["y"],self.object.sizeOfTile)
    self.move = True
    publishMessage(self)

def publishMessage(self):
    msg = String()
    data = json.dumps(jsonHandler.createJsonObject(self.object.x, self.object.y, self.object.sizeOfTile, self.object.actor["x"], self.object.actor["y"],self.object.map))
    msg.data = "{}".format(data)
    self.publisher_.publish(msg)

if __name__ == '__main__':
    main()

