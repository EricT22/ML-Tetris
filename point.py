class Point:
    def __init__(self, x, y) -> None:
        self.x: int = x
        self.y: int = y
    
    def getX(self):
        return self.x
    
    def setX(self, x):
        self.x = x

    def getY(self):
        return self.y
    
    def setY(self, y):
        self.y = y
