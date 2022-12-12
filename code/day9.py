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
class Knot(Point):
    def follow(self, head: Point) -> None:
        # Assumes head only moves 1 space at a time
        if self.x - head.x > 1:
            self.x -= 1
            # account for diagonal
            if self.y - head.y >= 1:
                self.y -= 1
            elif head.y - self.y >= 1:
                self.y += 1
        elif head.x - self.x > 1:
            self.x += 1
            # account for diagonal
            if self.y - head.y >= 1:
                self.y -= 1
            elif head.y - self.y >= 1:
                self.y += 1
        if self.y - head.y > 1:
            self.y -= 1
            # account for diagonal
            if self.x - head.x >= 1:
                self.x -= 1
            elif head.x - self.x >= 1:
                self.x += 1
        elif head.y - self.y > 1:
            self.y += 1
            # account for diagonal
            if self.x - head.x >= 1:
                self.x -= 1
            elif head.x - self.x >= 1:
                self.x += 1


@dataclass
class Tail(Knot):
    visited: set[Point]

    def follow(self, head: Point) -> None:
        super().follow(head)
        self.visited.add(Point(self.x, self.y))


def part_one() -> None:
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


def part_two(debug: bool = False) -> None:
    head = Point(0, 0)
    tail = Tail(0, 0, set())
    knots = [Knot(0, 0) for _ in range(0, 8)] + [tail]
    with open("inputs/day9", "r", encoding="utf-8") as file:
        for line in file:
            direction, distance = line.split()
            for count in range(0, int(distance)):
                if debug:
                    print(f"== {line.strip()} == ({count})")
                    print_debug(head, knots)
                # Move 1 space at a time
                head.move(direction)
                for idx, knot in enumerate(knots):
                    if idx == 0:
                        knot.follow(head)
                    else:
                        knot.follow(knots[idx - 1])

    print(f"Part 2 = {len(tail.visited)}")


def print_debug(head: Point, knots: list[Knot]) -> None:
    all_knots = [head] + knots
    size = 20
    for row in range(size, -size, -1):
        for col in range(-size, size):
            char = "."
            for count, knot in enumerate(all_knots):
                if Point(col, row) == knot:
                    char = str(count)
                    break
            if char == "." and (row, col) == (0, 0):
                char = "S"
            print(f"{char} ", end="")
        print("")


if __name__ == "__main__":
    part_one()
    part_two()
