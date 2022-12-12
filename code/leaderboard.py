import os

import pandas as pd
import requests


def get_leaderboard() -> pd.DataFrame:
    session = requests.Session()
    resp = session.get(
        "https://adventofcode.com/2022/leaderboard/private/view/2794065.json",
        cookies={
            "session": "53616c7465645f5fc7474e7a041824d2413204d7045456f02229806434eedbda6c8fa8a45a7ae6307fd6c10cafe3b0978ddd787a1ec0b15456fad2a037a92462"
        },
    )
    resp_json = resp.json()

    # resp_json = {
    #     "members": {
    #         "2794065": {
    #             "completion_day_level": {
    #                 "5": {
    #                     "2": {"star_index": 38395, "get_star_ts": 1670623111},
    #                     "1": {"get_star_ts": 1670622828, "star_index": 37882},
    #                 },
    #                 "3": {
    #                     "2": {"get_star_ts": 1670616196, "star_index": 24533},
    #                     "1": {"get_star_ts": 1670615771, "star_index": 23674},
    #                 },
    #                 "7": {
    #                     "2": {"star_index": 221484, "get_star_ts": 1670712611},
    #                     "1": {"get_star_ts": 1670711115, "star_index": 218736},
    #                 },
    #                 "6": {
    #                     "1": {"get_star_ts": 1670624012, "star_index": 40049},
    #                     "2": {"get_star_ts": 1670624099, "star_index": 40205},
    #                 },
    #                 "2": {
    #                     "2": {"star_index": 20760, "get_star_ts": 1670614297},
    #                     "1": {"get_star_ts": 1670613727, "star_index": 19588},
    #                 },
    #                 "8": {
    #                     "2": {"get_star_ts": 1670786685, "star_index": 359352},
    #                     "1": {"star_index": 356718, "get_star_ts": 1670785512},
    #                 },
    #                 "1": {
    #                     "1": {"star_index": 0, "get_star_ts": 1670604278},
    #                     "2": {"star_index": 850, "get_star_ts": 1670604634},
    #                 },
    #                 "4": {
    #                     "2": {"star_index": 26903, "get_star_ts": 1670617333},
    #                     "1": {"star_index": 26166, "get_star_ts": 1670616987},
    #                 },
    #             },
    #             "last_star_ts": 1670786685,
    #             "name": "wilsonconley",
    #             "local_score": 16,
    #             "stars": 16,
    #             "id": 2794065,
    #             "global_score": 0,
    #         }
    #     },
    #     "event": "2022",
    #     "owner_id": 2794065,
    # }

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
    df = get_leaderboard()
    write_table_to_md(df)
