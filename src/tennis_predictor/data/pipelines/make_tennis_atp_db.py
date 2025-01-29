import os
import shutil
import subprocess

from tennis_predictor.config.data import (
    PATH_BACKTRACK,
    SQLITE_SCRIPT_PATH,
    TENNIS_ATP_DB_NAME,
    TENNIS_ATP_EXTERNAL_FOLDER,
    TENNIS_ATP_INTERIM_FOLDER,
)


def move_and_run_script() -> None:
    # Change directory
    os.chdir(TENNIS_ATP_EXTERNAL_FOLDER)
    # Run the shell script
    subprocess.run([SQLITE_SCRIPT_PATH], check=True)
    # Change directory
    os.chdir(PATH_BACKTRACK)
    # Move the database file
    shutil.move(
        TENNIS_ATP_EXTERNAL_FOLDER + TENNIS_ATP_DB_NAME,
        TENNIS_ATP_INTERIM_FOLDER + TENNIS_ATP_DB_NAME,
    )


if __name__ == "__main__":
    move_and_run_script()
