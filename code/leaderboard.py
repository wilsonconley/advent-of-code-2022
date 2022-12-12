import os

import pandas as pd  # type: ignore[import]
import requests


def get_leaderboard() -> pd.DataFrame:
    session = requests.Session()
    resp = session.get(
        "https://adventofcode.com/2022/leaderboard/private/view/2794065.json",
        cookies={
            "session": "53616c7465645f5fc7474e7a041824d2413204d7045456f02229806434eedbda6c8fa8a45a7ae6307fd6c10cafe3b0978ddd787a1ec0b15456fad2a037a92462"  # pylint: disable=line-too-long
        },
    )
    resp_json = resp.json()

    columns = ["name"] + [str(x) for x in range(1, 26)] + ["stars"]
    table_dict: dict[str, list[str]] = {}
    for col in columns:
        table_dict[col] = []

    for _, user in resp_json["members"].items():
        table_dict["name"].append(user["name"])
        for day in range(1, 26):
            num_star = len(user["completion_day_level"].get(str(day), {}).keys())
            star_str = "*" * num_star + " " * (2 - num_star)
            table_dict[str(day)].append(star_str)
        table_dict["stars"].append(user["stars"])

    df = pd.DataFrame(table_dict)
    df.index += 1

    return df


def write_table_to_md(df: pd.DataFrame) -> None:
    output = str(df)
    with open("README.md", "r", encoding="utf-8") as file_in:
        with open("tmp.md", "w", encoding="utf-8") as file_out:
            overwrite = False
            for line in file_in:
                if not overwrite:
                    file_out.write(line)
                    if "```leaderboard" in line:
                        overwrite = True
                else:
                    if line.strip() == "```":
                        overwrite = False
                        file_out.write(output + "\n")
                        file_out.write(line)

    os.unlink("README.md")
    os.rename("tmp.md", "README.md")


if __name__ == "__main__":
    leaderboard = get_leaderboard()
    write_table_to_md(leaderboard)
