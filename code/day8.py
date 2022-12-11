class Score:
    left: int = 0
    right: int = 0
    up: int = 0
    down: int = 0

    def total(self) -> int:
        return self.left * self.right * self.up * self.down


def main() -> None:
    grid: list[list[int]] = []  # grid[r][c]
    with open("inputs/day8", "r", encoding="utf-8") as file:
        for line in file:
            grid.append([])
            for char in line.strip():
                grid[-1].append(int(char))

    part_one(grid)
    part_two(grid)


def part_one(grid: list[list[int]]) -> None:
    # part 1
    num_visibile = 0
    for row_index, row in enumerate(grid):
        for col, tree in enumerate(row):
            # Outside trees always visible
            if (
                row_index == 0
                or row_index == len(grid) - 1
                or col == 0
                or col == len(row) - 1
            ):
                num_visibile += 1
                continue

            # Check left visibility
            if tree > max(row[0:col]):
                num_visibile += 1
                continue

            # Check right visibility
            if tree > max(row[col + 1 :]):
                num_visibile += 1
                continue

            # Check top visibility
            if tree > max(r[col] for i, r in enumerate(grid) if i < row_index):
                num_visibile += 1
                continue

            # Check bottom visibility
            if tree > max(r[col] for i, r in enumerate(grid) if i > row_index):
                num_visibile += 1
                continue

    print(f"Part 1 = {num_visibile}")


def part_two(grid: list[list[int]]) -> None:
    # part 2
    max_score = 0
    for row_index, row in enumerate(grid):
        for col, tree in enumerate(row):
            score = Score()

            # Outside trees have score of 0
            if (
                row_index == 0
                or row_index == len(grid) - 1
                or col == 0
                or col == len(row) - 1
            ):
                continue

            # Check left score
            offset = 1
            while row[col - offset] < tree and col - offset > 0:
                score.left += 1
                offset += 1
            score.left += 1  # blocking tree counts for score

            # Check right score
            offset = 1
            while row[col + offset] < tree and col + offset < len(row) - 1:
                score.right += 1
                offset += 1
            score.right += 1  # blocking tree counts for score

            # Check up score
            offset = 1
            while grid[row_index - offset][col] < tree and row_index - offset > 0:
                score.up += 1
                offset += 1
            score.up += 1  # blocking tree counts for score

            # Check down score
            offset = 1
            while (
                grid[row_index + offset][col] < tree
                and row_index + offset < len(grid) - 1
            ):
                score.down += 1
                offset += 1
            score.down += 1  # blocking tree counts for score

            max_score = max(max_score, score.total())

    print(f"Part 2 = {max_score}")


if __name__ == "__main__":
    main()
