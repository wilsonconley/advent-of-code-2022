def main(part: int) -> None:
    stacks = setup_stacks()
    with open("inputs/day5", "r", encoding="utf-8") as file:
        # Define stacks
        for line in file:
            contents = line.strip()
            if contents:
                if "[" in contents:
                    count = 0
                    while count < len(contents):
                        box = contents[count + 1]
                        if box != " ":
                            stacks[int(count / 4)].insert(0, box)
                        count += 4
            else:
                break

        # Moving instructions
        for line in file:
            instruction = line.split()
            num_box = int(instruction[1])
            src = int(instruction[3]) - 1
            dst = int(instruction[5]) - 1
            if part == 1:
                for _ in range(0, num_box):
                    box = stacks[src].pop()
                    stacks[dst].append(box)
            else:
                boxes: list[str] = []
                for _ in range(0, num_box):
                    boxes.insert(0, stacks[src].pop())
                stacks[dst].extend(boxes)

    print(f"Part {part}: Top stacks = ", end="")
    for stack in stacks:
        print(stack[-1], end="")
    print("")


def setup_stacks() -> list[list[str]]:
    last_line = ""
    with open("inputs/day5", "r", encoding="utf-8") as file:
        for line in file:
            contents = line.strip()
            if not contents:
                break
            last_line = contents

    stacks: list[list[str]] = []
    for _ in last_line.split():
        stacks.append([])

    return stacks


if __name__ == "__main__":
    main(1)
    main(2)
