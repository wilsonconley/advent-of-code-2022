def main() -> None:
    msg = ""
    with open("inputs/day6", "r", encoding="utf-8") as file:
        for line in file:
            msg = line.strip()

    count = 3
    while count < len(msg):
        marker = msg[count - 4 : count]
        if len(set(marker)) == 4:
            print(f"start of packet = {count}")
            break
        count += 1

    count = 13
    while count < len(msg):
        marker = msg[count - 14 : count]
        if len(set(marker)) == 14:
            print(f"start of packet = {count}")
            break
        count += 1


if __name__ == "__main__":
    main()
