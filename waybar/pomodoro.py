import json
from datetime import timedelta, datetime
import subprocess


def parse_date(total_seconds: int) -> timedelta:
    return timedelta(seconds=total_seconds/1000000000)


input_json = subprocess.check_output(["pomo", "st", "--json"]).decode("utf-8").strip()
input_old = subprocess.check_output(["pomo", "st"]).decode("utf-8").strip().split(" ")
_status = json.loads(input_json)

status = ["breaking", "running", "completed", "created", "paused"][_status["state"]]
status_emoji = ["breaking", "🍅", "⬅️", "created", "💤"][_status["state"]]

position = 0

match _status["state"]:
    case 0:
        print("")
    case 1:
        time_raw=input_old[2]
        m, s = list(map(int, time_raw.removesuffix("s").split("m")))

        print("{status_emoji} {time} — {task_name}".format(
            status_emoji=status_emoji,
            task_name=_status["task_message"],
            time=f"{m:02}:{s:02}"
        ))
    case 2:
        d = parse_date(_status["pauseduration"])

        # print(d)
        print("{status_emoji} {time}".format(
            status_emoji=status_emoji,
            time=d,
        ))
    case 4:
        print("{status_emoji} {task_name}".format(
            status_emoji=status_emoji,
            task_name=_status["task_message"],
        ))
    case _:
        print(input_old)
