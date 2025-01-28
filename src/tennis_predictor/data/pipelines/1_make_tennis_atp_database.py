import os
import shutil
import subprocess

PATH_TENNIS_ATP = "./data/bronze/tennis_atp/"
PATH_DB_SCRIPT = "./examples/SQLite/convert_sqlite.sh"
PATH_BACKTRACK = "../../.."
DB_NAME = "atpdatabase.db"
PATH_OUTPUT = "./data/silver/tennis_atp/"


def move_and_run_script() -> None:
    # Change directory
    os.chdir(PATH_TENNIS_ATP)
    # Run the shell script
    subprocess.run([PATH_DB_SCRIPT], check=True)
    # Change directory
    os.chdir(PATH_BACKTRACK)
    # Move the database file
    shutil.move(PATH_TENNIS_ATP + DB_NAME, PATH_OUTPUT + DB_NAME)


if __name__ == "__main__":
    move_and_run_script()
