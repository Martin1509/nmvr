from math import pow, atan2, sqrt, degrees

def euclidean_distance(goal, pose):
    return sqrt(pow((goal[0] - pose[0]), 2) +
                pow((goal[1] - pose[1]), 2))

def linear_vel(goal, pose, constant=0.02):
    return constant * euclidean_distance(goal, pose)

def steering_angle(goal, pose):
    return degrees(atan2(goal[1] - pose[1], goal[0] - pose[0]))

def angular_vel(goal, pose, theta = 0, constant=0.1):
    return constant * (steering_angle(goal, pose) - theta)