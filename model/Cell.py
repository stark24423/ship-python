class Cell:
    def __init__(self, x=0, y=0):
        self._AT = 1000000  # infinit number
        self._block = 0
        self._vis = 0
        self._x = x
        self._y = y

    # AT 的 getter
    @property
    def AT(self):
        return self._AT

    # AT 的 setter
    @AT.setter
    def AT(self, value):
        if value < 0:
            raise ValueError("AT cannot be negative")
        self._AT = value

    # block 的 getter
    @property
    def block(self):
        return self._block

    # block 的 setter
    @block.setter
    def block(self, value):
        if not isinstance(value, int):
            raise ValueError("block must be an integer")
        self._block = value

    # vis 的 getter
    @property
    def vis(self):
        return self._vis

    # vis 的 setter
    @vis.setter
    def vis(self, value):
        if value < 0:
            raise ValueError("vis cannot be negative")
        self._vis = value

    # x 的 getter
    @property
    def x(self):
        return self._x

    # x 的 setter
    @x.setter
    def x(self, value):
        if not isinstance(value, int):
            raise ValueError("x must be an integer")
        self._x = value

    # y 的 getter
    @property
    def y(self):
        return self._y

    # y 的 setter
    @y.setter
    def y(self, value):
        if not isinstance(value, int):
            raise ValueError("y must be an integer")
        self._y = value

        # Add comparison method for heapq
    def __lt__(self, other):
        return self.AT < other.AT
