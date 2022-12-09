class Elf:
    items: list[int]
    total: int = 0

    def __init__(self, items: list[int]) -> None:
        self.items = items
        self.total = sum(items)


def main() -> None:
    elves: list[Elf] = []
    items: list[int] = []
    with open("inputs/day1", "r", encoding="utf-8") as file:
        for line in file:
            line_ = line.strip()
            if line_:
                items.append(int(line_))
            else:
                elves.append(Elf(items))
                items = []
    print("max is: " + str(max([elf.total for elf in elves])))
    print("top 3: " + str(sum(sorted([elf.total for elf in elves], reverse=True)[:3])))


if __name__ == "__main__":
    main()
