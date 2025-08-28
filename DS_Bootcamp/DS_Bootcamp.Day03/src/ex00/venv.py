import os

def get_name_of_VirtualEnv():
    path = os.environ.get("VIRTUAL_ENV")

    if path:
        return path
    return None

if __name__ == "__main__":
    name = os.path.basename(get_name_of_VirtualEnv())

    if name:
        print(f"Your current virtual env is {name}")
    else:
        print("The virtual environment does not exist or is not activated.")