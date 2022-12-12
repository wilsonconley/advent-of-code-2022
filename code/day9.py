from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def move(self, direction: str) -> None:
        # Assumes moving 1 space at a time
        if direction == "U":
            self.y += 1
        elif direction == "D":
            self.y -= 1
        elif direction == "L":
            self.x -= 1
        elif direction == "R":
            self.x += 1

    def __hash__(self) -> int:
        return 0

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False


@dataclass
class Tail(Point):
    visited: set[Point]

    def follow(self, head: Point) -> None:
        # Assumes head only moves 1 space at a time
        if self.x - head.x > 1:
            self.x -= 1
            self.y = head.y  # account for diagonal
        elif head.x - self.x > 1:
            self.x += 1
            self.y = head.y  # account for diagonal
        if self.y - head.y > 1:
            self.y -= 1
            self.x = head.x  # account for diagonal
        elif head.y - self.y > 1:
            self.y += 1
            self.x = head.x  # account for diagonal
        self.visited.add(Point(self.x, self.y))


def main() -> None:
    head = Point(0, 0)
    tail = Tail(0, 0, set())
    with open("inputs/day9", "r", encoding="utf-8") as file:
        for line in file:
            direction, distance = line.split()
            for _ in range(0, int(distance)):
                # Move 1 space at a time
                head.move(direction)
                tail.follow(head)
    print(f"Part 1 = {len(tail.visited)}")


if __name__ == "__main__":
    main()
