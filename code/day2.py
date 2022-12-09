from enum import Enum

shapes: dict[str, str] = {
    "A": "ROCK",
    "B": "PAPER",
    "C": "SCISSORS",
    "X": "ROCK",
    "Y": "PAPER",
    "Z": "SCISSORS",
}

outcomes: dict[tuple[str, str], str] = {
    ("ROCK", "ROCK"): "DRAW",
    ("ROCK", "PAPER"): "WIN",
    ("ROCK", "SCISSORS"): "LOSS",
    ("PAPER", "ROCK"): "LOSS",
    ("PAPER", "PAPER"): "DRAW",
    ("PAPER", "SCISSORS"): "WIN",
    ("SCISSORS", "ROCK"): "WIN",
    ("SCISSORS", "PAPER"): "LOSS",
    ("SCISSORS", "SCISSORS"): "DRAW",
}


class Score(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    LOSS = 0
    DRAW = 3
    WIN = 6


def part_one() -> None:
    guide: list[tuple[str, str]] = []
    with open("inputs/day2") as file:
        for line in file:
            guide.append(tuple([shapes[x] for x in line.strip().split()]))
    score = calculate_score(guide)
    print(f"Part 1: final score = {score}")


def calculate_score(guide: list[tuple[str, str]]) -> int:
    score = 0
    for round in guide:
        score += Score[outcomes[round]].value + Score[round[1]].value
    return score


end_goal: dict[str, str] = {
    "X": "LOSS",
    "Y": "DRAW",
    "Z": "WIN",
}


def part_two() -> None:
    guide: list[tuple[str, str]] = []
    with open("inputs/day2") as file:
        for line in file:
            opp, desired = tuple(line.strip().split())
            opp_shape = shapes[opp]
            desired_outcome = end_goal[desired]
            my_shape = "ERROR"
            for x in outcomes:
                if outcomes[x] == desired_outcome and x[0] == opp_shape:
                    my_shape = x[1]
            guide.append((opp_shape, my_shape))
    score = calculate_score(guide)
    print(f"Part 2: final score = {score}")


if __name__ == "__main__":
    part_one()
    part_two()
