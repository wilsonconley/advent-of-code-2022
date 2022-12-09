def part_one() -> None:
    sacks: list[tuple[str, str]] = []
    with open("inputs/day3") as file:
        for line in file:
            contents = line.strip()
            half = int(len(contents) / 2)
            sacks.append((contents[0:half], contents[half:]))
    common = [[x for x in sack[0] if x in sack[1]][0] for sack in sacks]
    score = calc_score(common)
    print(f"Part 1: score = {score}")


def calc_score(common: list[str]) -> int:
    score = 0
    for c in common:
        if c >= "a" and c <= "z":
            score += ord(c) - ord("a") + 1
        else:
            score += ord(c) - ord("A") + 27
    return score


def part_two() -> None:
    groups: list[tuple[str, str, str]] = []
    with open("inputs/day3") as file:
        tmp: list[str] = []
        for line in file:
            tmp.append(line.strip())
            if len(tmp) == 3:
                groups.append(tuple(tmp))
                tmp = []
    common = [
        [x for x in group[0] if x in group[1] and x in group[2]][0] for group in groups
    ]
    score = calc_score(common)
    print(f"Part 2: score = {score}")


if __name__ == "__main__":
    part_one()
    part_two()
