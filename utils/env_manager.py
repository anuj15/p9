from dotenv import *


def get_env(key):
    load_dotenv()
    return dotenv_values()[key]
