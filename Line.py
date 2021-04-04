class Line:
    """
    Class representing lines
    """
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

    def set_next(self, line):
        self.next = line

    def set_prev(self, line):
        self.prev = line
