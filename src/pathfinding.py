from collections import deque

def getPath(start, end):
    return Path()

class Path:
    def __init__(self):
        self.left = deque()
        self.floor = deque()
        
        def hasNext(self):
            pass # not sure how best to do
        
        def next(self):
            return self.left.popleft(), self.floor.popleft()

