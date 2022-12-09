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
    with open("inputs/day2", "r", encoding="utf-8") as file:
        for line in file:
            x, y = line.strip().split()
            guide.append((shapes[x], shapes[y]))
    score = calculate_score(guide)
    print(f"Part 1: final score = {score}")


def calculate_score(guide: list[tuple[str, str]]) -> int:
    score = 0
    for event in guide:
        score += Score[outcomes[event]].value + Score[event[1]].value
    return score


end_goal: dict[str, str] = {
    "X": "LOSS",
    "Y": "DRAW",
    "Z": "WIN",
}


def part_two() -> None:
    guide: list[tuple[str, str]] = []
    with open("inputs/day2", "r", encoding="utf-8") as file:
        for line in file:
            opp, desired = tuple(line.strip().split())
            opp_shape = shapes[opp]
            desired_outcome = end_goal[desired]
            my_shape = "ERROR"
            for k, v in outcomes.items():
                if v == desired_outcome and k[0] == opp_shape:
                    my_shape = k[1]
            guide.append((opp_shape, my_shape))
    score = calculate_score(guide)
    print(f"Part 2: final score = {score}")


if __name__ == "__main__":
    part_one()
    part_two()
