 from math import pow, atan2, sqrt

def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

def euclidean_distance(self, goal_pose):
    """Euclidean distance between current pose and the goal."""
    return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                pow((goal_pose.y - self.pose.y), 2))

def linear_vel(self, goal_pose, constant=1.5):
    return constant * euclidean_distance(self, goal_pose)

def steering_angle(self, goal_pose):
    return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

def angular_vel(self, goal_pose, constant=6):
    return constant * (steering_angle(self, goal_pose) - self.pose.theta)