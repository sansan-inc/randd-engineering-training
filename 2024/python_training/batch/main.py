import sys

import gokart
from dotenv import load_dotenv

import pipeline  # noqa: F401

if __name__ == "__main__":
    load_dotenv()
    gokart.add_config("./conf/param.ini")
    gokart.run(sys.argv[1:])
