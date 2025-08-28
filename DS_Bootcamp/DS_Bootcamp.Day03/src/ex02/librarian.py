import os

class Wrong_venv(Exception):
    pass

def check_env():
    path = os.environ.get("VIRTUAL_ENV")
    name_env = os.path.basename(path)
    if name_env != "pasquald":
        raise Wrong_venv("Wrong virtual environment")
    
def main():
    try:
        check_env()
        os.system("pip install beautifulsoup4 pytest")
        os.system("pip freeze")
        os.system("pip freeze > requirements.txt")
        

    except Wrong_venv as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

