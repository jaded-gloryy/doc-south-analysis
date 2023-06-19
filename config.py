from os import environ
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "TOC_FILEPATH": environ["TOC_FILEPATH"],
    "CGD_FILEPATH": environ["CGD_FILEPATH"],
    "DATA_FOR_CLASSIFIER": environ["DATA_FOR_CLASSIFIER"],
    # "": environ[""]
}