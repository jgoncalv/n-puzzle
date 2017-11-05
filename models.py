class Node:
    def __init__(self, name):
        self.grid = name
        self.h = 0
        self.g = 0
        self.f = self.g + self.h
        self.parent = ""
    
    def update(self, g, h, isBFS):
        self.h = h
        self.g = g
        if isBFS:
            self.f = 0 + self.h
        else:
            self.f = self.g + self.h

    def __str__(self):
        return self.grid