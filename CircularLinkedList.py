class CircularLinkedList:
    """
    Class representing a Circular Doubly Linked List used to store Lines
    This is not a complete Circular Doubly Linked List as it only contains methods that are
    useful to implementation of Qix game (It only has insert to end method).
    If more methods are required, it will be added.
    """
    def __init__(self):
        self.list = []
        self.head = None
        self.tail = None

    def insert_end(self, line) -> None:
        """
        Inserts the given element to the end of the list.
        :param line: Element to be inserted to the list
        :return: None
        """
        if self.head is None:
            self.head = line
            self.tail = line
        else:
            self.tail.set_next(line)
            line.set_prev(self.tail)
            self.tail = line
        self.tail.set_next(self.head)
        self.head.set_prev(self.tail)

    def print_list(self) -> None:
        """
        prints the CLL from head to tail.
        :return: None
        """
        cur = self.head
        while cur is not None:
            print(cur.data)
            cur = cur.next
