class CRT:
    width = 40
    height = 6
    screen: list[str]

    def __init__(self) -> None:
        self.screen = []

    def display(self) -> None:
        for row in range(0, self.height):
            for col in range(0, self.width):
                print(self.screen[row * self.width + col], end="")
            print("")


class CPU:
    commands: list[str]
    cycle_count: int = 0
    x: int = 1
    interesting_signal: dict[int, int]
    crt: CRT

    def __init__(self, commands: list[str]) -> None:
        self.commands = commands
        self.crt = CRT()

        # calc signal at these cycle intervals
        self.interesting_signal = {
            20: 0,
            60: 0,
            100: 0,
            140: 0,
            180: 0,
            220: 0,
        }

    def cycle(self) -> None:
        # crt
        if self.cycle_count <= self.crt.height * self.crt.width:
            if self.x - 1 <= self.cycle_count % 40 <= self.x + 1:
                self.crt.screen.append("#")
            else:
                self.crt.screen.append(".")

        # increment cycle count
        self.cycle_count += 1

        # interesting signal
        if self.cycle_count in self.interesting_signal:
            self.interesting_signal[self.cycle_count] = self.cycle_count * self.x

    def run(self) -> None:
        while self.commands:
            cmd = self.commands.pop()
            if cmd == "noop":
                self.cycle()
            else:
                self.cycle()
                self.cycle()
                self.x += int(cmd.split()[1])


def main() -> None:
    cmds = []
    with open("inputs/day10", "r", encoding="utf-8") as file:
        for line in file:
            cmds.append(line.strip())

    cpu = CPU(cmds[::-1])  # reverse order to put on top of stack
    cpu.run()

    print(f"part 1 = {sum(x for x in cpu.interesting_signal.values())}")

    print("part 2 = ")
    cpu.crt.display()


if __name__ == "__main__":
    main()
