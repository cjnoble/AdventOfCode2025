import os

def new_day(day:int):

    day_str = f"{day:02d}"

    day_path = f"day_{day_str}.py"
    if not os.path.exists(day_path):
        with open(f"day_template.py", "r") as f_template:
            with open(day_path, "a") as f:
                day = f_template.readlines()
                day[21] = f"    DAY = \"{day_str}\"\n"
                f.writelines(day)

    test_path = f"day_{day_str}_test.py"
    if not os.path.exists(test_path):
        with open(f"test_template.py", "r") as f_template:
            with open( test_path, "a") as f:
                test = f_template.readlines()
                
                test[1] = f"import day_{day_str} as day\n"
                test[3] = f"DAY = \"{day_str}\"\n"

                f.writelines(test)

if __name__ == "__main__":

    DAY = 2
    new_day(DAY)