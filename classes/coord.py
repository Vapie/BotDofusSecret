class Coord:
    x: int
    y: int
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def distance(self, coord) -> int:
        count = 0
        count += abs(self.x-coord.x)
        count += abs(self.y-coord.y)
        return count

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False





