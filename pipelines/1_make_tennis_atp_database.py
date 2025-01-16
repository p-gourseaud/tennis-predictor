import os
import subprocess
import shutil

def move_and_run_script():
    # Change directory
    os.chdir('./data/bronze/tennis_atp/')
    
    # Run the shell script
    subprocess.run(['./examples/SQLite/convert_sqlite.sh'], check=True)
    
    # Move the database file
    shutil.move('atpdatabase.db', '../../silver/tennis_atp/atpdatabase.db')

if __name__ == "__main__":
    move_and_run_script()