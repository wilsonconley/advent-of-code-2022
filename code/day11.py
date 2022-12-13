from __future__ import annotations

import math
import sys
import tempfile
import typing as t
from dataclasses import dataclass

from yaml import safe_load


@dataclass
class Item:
    worry_level: int


@dataclass
class Monkey:
    items: list[Item]
    operation: str
    test_param: int  # assume "divisible by"
    on_true: int  # destination monkey index
    on_false: int  # destination monkey index
    count: int = 0

    def eval_operation(self, old: int) -> int:  # pylint: disable=[unused-argument]
        # "old" is name of variable in operation string
        return eval(self.operation)  # type: ignore[no-any-return] # pylint: disable=[eval-used]

    def test(self, level: int) -> bool:
        return level % self.test_param == 0

    def inspect(self, item: Item, lcm: t.Optional[int] = None) -> None:
        item.worry_level = self.eval_operation(item.worry_level)
        if lcm is None:
            item.worry_level = int(item.worry_level / 3)
        else:
            # to keep level manageable, modulo by the LCM
            item.worry_level = item.worry_level % lcm

        self.count += 1

    def throw(self, item: Item, monkeys: dict[int, Monkey]) -> None:
        self.items.remove(item)
        if self.test(item.worry_level):
            monkeys[self.on_true].items.append(item)
        else:
            monkeys[self.on_false].items.append(item)

    def check_items(
        self, monkeys: dict[int, Monkey], lcm: t.Optional[int] = None
    ) -> None:
        for item in list(self.items):
            self.inspect(item, lcm)
            self.throw(item, monkeys)


def parse_input(filename: str) -> dict[int, Monkey]:
    with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as tmp_file:
        with open(filename, "r", encoding="utf-8") as file:
            # Pre-process for yaml load
            for line in file:
                if "If true" in line or "If false" in line:
                    tmp_file.write(line[2:])
                else:
                    tmp_file.write(line)
        tmp_file.seek(0)
        input_dict: dict[str, dict[str, str]] = safe_load(tmp_file)

    # Create Monkeys
    monkeys: dict[int, Monkey] = {}
    for name, attr in input_dict.items():
        start_items = (
            attr["Starting items"]
            if isinstance(attr["Starting items"], str)
            else str(attr["Starting items"])
        )
        items = [Item(int(x)) for x in start_items.split(", ")]
        operation = attr["Operation"].strip("new = ")
        monkeys[int(name.split()[-1])] = Monkey(
            items,
            operation,
            *[int(attr[x].split()[-1]) for x in ["Test", "If true", "If false"]],
        )
    return monkeys


def monkey_business(monkeys: dict[int, Monkey]) -> int:
    total = 1
    for x in sorted([monkeys[x].count for x in monkeys])[-2:]:
        total *= x
    return total


def print_monkeys(monkeys: dict[int, Monkey]) -> None:
    for monkey in monkeys:
        print(f"Monkey {monkey}: ", end="")
        for item in monkeys[monkey].items:
            print(f"{item.worry_level}, ", end="")
        print("")


def part_one(filename: str, debug: bool) -> None:
    monkeys = parse_input(filename)

    # Inspect items for 20 rounds
    for _ in range(0, 20):
        for monkey in monkeys.values():
            monkey.check_items(monkeys)
        if debug:
            print_monkeys(monkeys)

    print(f"Part 1: monkey business = {monkey_business(monkeys)}")


def part_two(filename: str, debug: bool) -> None:
    monkeys = parse_input(filename)

    # get LCM
    lcm = math.lcm(*[monkey.test_param for monkey in monkeys.values()])

    # Inspect items for 10000 rounds
    for round_ in range(1, 10001):
        for monkey in monkeys.values():
            monkey.check_items(monkeys, lcm=lcm)
        if debug and round_ % 1000 == 0:
            print(f"== After round {round_} ==")
            for name, monkey in monkeys.items():
                print(f"Monkey {name} inspected items {monkey.count} times.")

    print(f"Part 2: monkey business = {monkey_business(monkeys)}")


def main() -> None:
    debug = sys.argv[1].lower() == "debug" if len(sys.argv) > 1 else False
    if debug:
        filename = "inputs/examples/day11"
    else:
        filename = "inputs/day11"
    part_one(filename, debug)
    part_two(filename, debug)


if __name__ == "__main__":
    main()
