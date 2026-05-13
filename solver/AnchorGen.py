import numpy as np

class Anchor:
    def __init__(self,position,type):
        self.position = position
        self.type = type
        self.score = self.score_calc()

    def radius(self):
        if self.type == 'seal':
            return 2.5
        if self.type == 'rock':
            return 6
        if self.type == 'destroyed':
            return 0
        
    def destroy(self):
        if self.type == 'seal':
            self.type = 'destroyed'
        elif self.type == 'rock':
            self.type = 'seal'
        self.score = self.score_calc()

    def score_calc(self):
        if self.type == 'seal':
            return 1.0
        if self.type == 'rock':
            return 1.3
        if self.type == 'destroyed':
            return 0.0
        return 0.0

class Vector:
    def __init__(self,a,v): # vectors in the form a + v*t, expressing an infinitely long line in the direction of v, starting at a
        self.a = a
        self.v = v

    def distance_to_point(self,point):
        # distance from point to line defined by vector
        return np.linalg.norm(np.cross(self.v, self.a - point)) / np.linalg.norm(self.v)
    
def center_dist(anchor1, anchor2):
    return np.sqrt((anchor1.position[0] - anchor2.position[0])**2 + (anchor1.position[1] - anchor2.position[1])**2)

def generate_anchors_rand():
    anchors = []
    anchors.append(Anchor(np.array([0,0]),'rock'))
    while len(anchors) < 9:
        x = np.random.uniform(-35,35)
        y = np.random.uniform(-35,35)
        temp_type = 'rock' if len(anchors) <= 3 else 'seal'
        temp_anchor = Anchor(np.array([x,y]), temp_type)
        if all(center_dist(temp_anchor, anchor) > 10 for anchor in anchors):
            anchors.append(temp_anchor)
    return anchors

def generate_anchors_grid(spread=20,random_deviation=6):
    anchors = []
    anchors.append(Anchor(np.array([0,0]),'rock'))
    coords = [np.array([spread,spread]), np.array([spread,0]), np.array([spread,-spread]), np.array([0,spread]), np.array([0,-spread]), np.array([-spread,spread]), np.array([-spread,0]), np.array([-spread,-spread])]
    i = 0
    rocks = np.random.choice(len(coords), size=3, replace=False)
    for x, y in coords:
        if i in rocks:
            anchors.append(Anchor(np.array([x+np.random.uniform(-random_deviation,random_deviation), y+np.random.uniform(-random_deviation,random_deviation)]), 'rock'))
        else:
            anchors.append(Anchor(np.array([x+np.random.uniform(-random_deviation,random_deviation), y+np.random.uniform(-random_deviation,random_deviation)]), 'seal'))
        i += 1
    return anchors