def main() -> None:
    full_overlap = 0
    any_overlap = 0
    with open("inputs/day4", "r", encoding="utf-8") as file:
        for line in file:
            contents = line.strip()
            elf_one, elf_two = contents.split(",")
            one_min, one_max = [int(x) for x in elf_one.split("-")]
            two_min, two_max = [int(x) for x in elf_two.split("-")]
            if (one_min >= two_min and one_max <= two_max) or (
                two_min >= one_min and two_max <= one_max
            ):
                full_overlap += 1
            if ((two_min <= one_min <= two_max) or (two_min <= one_max <= two_max)) or (
                (one_min <= two_min <= one_max) or (one_min <= two_max <= one_max)
            ):
                any_overlap += 1
    print(f"Num full_overlap pairs = {full_overlap}")
    print(f"Num any_overlap pairs = {any_overlap}")


if __name__ == "__main__":
    main()
