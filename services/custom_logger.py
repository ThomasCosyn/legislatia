import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler("log_python.log")
handler.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter(
    "%(asctime)s - %(pathname)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(handler)
logger.addHandler(console_handler)


class bcolors:
    ANSWER = "\033[93m"  # YELLOW
    SOURCE = "\033[94m"  # BLUE
    RESET = "\033[0m"  # RESET COLOR
    RED = "\033[31m"
    GREEN = "\033[32m"
