import subprocess
import os

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game.py")
command = f'start /MAX cmd /k python "{script_path}"'
subprocess.run(command, shell=True)
