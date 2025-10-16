import os


TEMP_PATH = os.path.join(os.path.dirname(__file__), "temp")
BUILD_PATH = os.path.join(os.path.dirname(__file__), "build")
SAY_PATH = os.path.join(BUILD_PATH, "say.exe")


def system(shell_command: str) -> None:
    result = os.system(shell_command)

    if result != 0: raise Exception(f"{result}\nfailed to run command")


def say(input: str) -> None:
    system(f"{SAY_PATH} \"{input}\"")


def say_from_path(in_path: str, out_path: str) -> None:
    # yes this is still necessary
    if os.path.exists(out_path):
        os.remove(out_path)

    system(f"{SAY_PATH} -w {out_path} < {in_path}")


def say_to_path(input: str, out_path: str) -> None:
    # write to file to bypass window's max command prompt length of 8191
    if len(input) >= 500:
        print("having to use file :/")
        in_path = os.path.join(TEMP_PATH, "temp.txt")
        with open(in_path, "w") as file: file.write(input)
        say_from_path(in_path, out_path)
        return

    # yes this is necessary
    if os.path.exists(out_path):
        os.remove(out_path)

    system(f"{SAY_PATH} -w {out_path} \"{input}\"")

