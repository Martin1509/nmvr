from math import pow, atan2, sqrt, degrees
import math

def euclidean_distance(goal, pose):
    return sqrt(pow((goal[0] - pose[0]), 2) +
                pow((goal[1] - pose[1]), 2))

def linear_vel(goal, pose, constant=1):
    return constant * euclidean_distance(goal, pose)

def steering_angle(goal, pose):
    return atan2(goal[1] - pose[1], goal[0] - pose[0])

def angular_vel(goal, pose, theta = 0, constant=10):
    steer = steering_angle(goal, pose) # kde mam byt natoceny
    return constant * changePiToRange(steer - theta)

def changePiToRange(angle):
    while angle > math.pi:
        angle -= 2.0 * math.pi
    while angle < -math.pi:
        angle += 2.0 * math.pi
    return angle