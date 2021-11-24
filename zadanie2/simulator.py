import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from tkinter import *

from jsonHandler import getJsonObject
import jsonHandler
import jsonObject
import PRegulator
from PIL import ImageTk, Image
from datetime import datetime

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
        self.start = False
        self.goal = [-1, -1, -1, -1]
        self.x = 0
        self.y = 0
        self.xActor = 0
        self.yActor = 0
        self.object: jsonObject.Json = None
        while(self.object is None):
            continue
        self.lastRotation = 0
        self.increment = 6
        self.root = Tk()
        self.root.title("Task 1")
        self.root.configure(background='black')
        self.canvas_width = self.object.x
        self.canvas_height = self.object.y
        self.w: Canvas = Canvas(self.root, 
                    width=self.canvas_width+10,
                    height=self.canvas_height+10+180)
                    
        self.w.bind("<Button-1>", lambda event: callback(event, self, True))
        self.w.bind("<Button-3>", lambda event: callback(event, self, False))
        self.root.bind("<Left>", lambda event: moveActorKey(event, self))
        self.root.bind("<Right>", lambda event: moveActorKey(event, self))
        self.root.bind("<Up>", lambda event: moveActorKey(event, self))
        self.root.bind("<Down>", lambda event: moveActorKey(event, self))
        self.w.pack()

        checkered(self,self.w,self.object.sizeOfTile, self.increment)
        # self.xActor, self.yActor = getCoordinatesOfActor(self, self.object.actor["x"], self.object.actor["y"],self.object.sizeOfTile)
        self.img= (Image.open("actor.png"))
        self.actorSize = 25
        self.resized_image= self.img.resize((self.actorSize,self.actorSize), Image.ANTIALIAS)
        self.new_image= ImageTk.PhotoImage(self.resized_image.rotate(90))
        self.actor = self.w.create_image(self.object.actor["realX"], self.object.actor["realY"], image=self.new_image)
        rotateActor(self, self.object.rotation)
        self.start = True
        
        mainloop()

    def listener_callback(self, msg):
        dict = json.loads(msg.data)
        object1 = jsonObject.Json(**dict)
        self.object = object1
        print("update {}".format(datetime.now().strftime("%H:%M:%S")))
        if self.start:
            if self.move:
                self.w.move(self.actor, self.x, self.y)
                self.move = False
            if self.click:
                renderMapTiles(self)
                self.w.tag_raise(self.actor)
                self.click = False
                self.root.update()
            if self.lastRotation != self.object.rotation:
                rotateActor(self, self.object.rotation)
        
        print("realX: {}  realY: {}".format(self.xActor, self.yActor))
        print(self.goal)

def main(args=None):
    rclpy.init(args=args)
    
    simulator = Simulator()
    
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
    more = 5
    speedLabel = Label(self.root, text='Speed')
    speedLabel.config(font=('helvetica', 10))
    speedLabel.place(x= 5, y= self.canvas_height+10 + more)
    self.speedEntry = Entry(self.root)
    self.speedEntry.place(x=80, y = self.canvas_height+10)

    rotationLabel = Label(self.root, text='Rotation')
    rotationLabel.config(font=('helvetica', 10))
    rotationLabel.place(x= 5, y= self.canvas_height+40 + more)
    self.rotationEntry = Entry(self.root)
    self.rotationEntry.place(x=80, y = self.canvas_height+40)

    startLabel = Label(self.root, text='start x:y')
    startLabel.config(font=('helvetica', 10))
    startLabel.place(x= 5, y= self.canvas_height+70 + more)
    self.startEntry = Entry(self.root)
    self.startEntry.place(x=80, y = self.canvas_height+70)

    goalLabel = Label(self.root, text='goal x:y')
    goalLabel.config(font=('helvetica', 10))
    goalLabel.place(x= 5, y= self.canvas_height+100 + more)
    self.goalEntry = Entry(self.root)
    self.goalEntry.place(x=80, y = self.canvas_height+100)

    button = Button(text='Set parameters', command=lambda : buttonHandler(self), bg='gray', fg='black', font=('helvetica', 10, 'bold'), highlightbackground=('black'))
    button.place(x= 5, y=self.canvas_height+130)

    navigateButton = Button(text='Navigate to goal', command=lambda : navigateHandler(self), bg='gray', fg='black', font=('helvetica', 10, 'bold'), highlightbackground=('black'))
    navigateButton.place(x= 5, y=self.canvas_height+160)

def callback(event, self, left):
    if self.canvas_height < event.y:
        return
    if left:
        xTile, yTile = getTile(self, event.x, event.y)
        if(self.object.map[xTile][yTile] == 0):
            self.object.map[xTile][yTile] = 1
        else:
            self.object.map[xTile][yTile] = 0
    else:
        tile = getTile(self, event.x, event.y)
        self.goal[0] = tile[0]
        self.goal[1] = tile[1]
        self.goal[2] = event.x
        self.goal[3] = event.y

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
            if(self.goal[0] == i and self.goal[1] == j):
                self.w.create_rectangle(x, y, x+self.object.sizeOfTile, y+self.object.sizeOfTile, fill="#FF0000")
            elif(self.object.map[i][j] == 1):
                self.w.create_rectangle(x, y, x+self.object.sizeOfTile, y+self.object.sizeOfTile, fill="#7f8280")
            else:
                self.w.create_rectangle(x, y, x+self.object.sizeOfTile, y+self.object.sizeOfTile, fill="#ffffff")

def moveActorKey(event, self):
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
    self.object.actor["realX"] = self.xActor
    self.object.actro["realY"] = self.yActor
    self.move = True
    publishMessage(self)

def publishMessage(self):
    msg = String()
    data = json.dumps(jsonHandler.createJsonObject(self.object.x, self.object.y, self.object.sizeOfTile, self.object.actor["x"], self.object.actor["y"],self.object.actor["realX"], self.object.actor["realY"], self.object.map, self.object.speed, self.object.rotation))
    msg.data = "{}".format(data)
    self.publisher_.publish(msg)

def rotateActor(self, angle):
    self.new_image = ImageTk.PhotoImage(self.resized_image.rotate(angle+90))
    self.actor = self.w.create_image(self.xActor, self.yActor, image=self.new_image)
    self.lastRotation = angle

def buttonHandler(self):
    print("speed: {} and rotation: {} goal: {}".format(self.speedEntry.get(), self.rotationEntry.get(), self.goalEntry.get()))
    if self.speedEntry.get() == "0" or self.speedEntry.get().isdigit():
        self.object.speed = int(self.speedEntry.get())
    if self.rotationEntry.get() == "0" or self.rotationEntry.get().isdigit():
        self.object.rotation = int(self.rotationEntry.get())
    xy = getXY(self, self.goalEntry.get())
    if xy != None:
        self.goal = xy
    self.click = True
    publishMessage(self)

def navigateHandler(self):
    navGoal = [self.goal[2], self.goal[3]]
    navPose = [self.xActor, self.yActor]

    print(navGoal)
    print(navPose)
    
    distance = PRegulator.euclidean_distance(navGoal, navPose)
    linear = PRegulator.linear_vel(navGoal, navPose)
    angular = PRegulator.angular_vel(navGoal, navPose, self.object.rotation)

    print("dis: {}, lin: {}, ang: {}".format(distance, linear, angular))

def getXY(self, message):
    if ":" in message:
        string = message.split(":")
        coordinates = getTile(self, int(string[0]), int(string[1]))
        return [coordinates[0], coordinates[1], int(string[0]), int(string[1])]
    return None

if __name__ == '__main__':
    main()