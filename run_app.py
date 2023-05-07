# import os
# import subprocess

# def main():
#     command = "streamlit run object_detection.py"
#     subprocess.run(command, shell=True)
    
# if __name__ == "__main__":
#     main()

import os
import subprocess

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    object_detection_path = os.path.join(current_directory, "object_detection.py")
    command = f"streamlit run {object_detection_path}"
    subprocess.run(command, shell=True)
    
if __name__ == "__main__":
    main()

