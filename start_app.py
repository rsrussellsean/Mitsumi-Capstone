import os
import subprocess

def main():
    command = "streamlit run object_detection.py"
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    main()
