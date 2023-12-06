import logging
import copy

# CONSTANTS SECTION
# The background is set with 40 plus the number of the color, and the foreground with 30
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# These are the sequences need to get colored ouput
DEFAULT_IMPORTANCE = "Unknown" # not ready for implementation yet
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

COLORS = {
    "WARNING": YELLOW,
    "INFO": WHITE,
    "DEBUG": BLUE,
    "CRITICAL": CYAN,
    "ERROR": RED
}
# END OF CONSTANTS SECTION


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


class ColoredFormatter(logging.Formatter):

    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        # Create a copy of the record before changing it
        record_copy = copy.copy(record)

        levelname = record_copy.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record_copy.levelname = levelname_color

        # Call the parent class's format method with the copied record
        return logging.Formatter.format(self, record_copy)

# for better logging severity within the example log
class ImportanceFormatter(logging.Formatter):
    def format(self, record):
        # Map the level number to an importance value
        level_to_importance = {
            logging.DEBUG: "Low",
            logging.INFO: "Medium",
            logging.WARNING: "High",
            logging.ERROR: "Critical",
            logging.CRITICAL: "Critical"
        }
        importance = level_to_importance.get(record.levelno, "Unknown")

        # Add the importance value to the record
        record.importance = importance

        # Call the parent class's format method
        return super().format(record)


# logger class with multiple destinations, Console Stream (has colors, very cool) and File Stream (example.log)
class ColoredLogger(logging.Logger):
    """A logger that supports colored and importance-level log messages."""

    def __init__(self, name):
        super().__init__(name, logging.DEBUG)

        # Define format strings
        formatCL = "%(asctime)s - [%(levelname)-s] | %(message)s | ($BOLD%(filename)s$RESET:%(lineno)d)"
        formatFH = "%(asctime)s - %(levelname)-s | IMPORTANCE: %(importance)s | %(message)s (%(filename)s: Line Number %(lineno)d)"

        # create formatters
        color_formatter = ColoredFormatter(formatter_message(formatCL, True))
        file_formatter = ImportanceFormatter(formatFH)

        # create console handler and set formatter
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)

        # create file handler and set formatter
        fh = logging.FileHandler("example.log")
        fh.setFormatter(file_formatter)
        self.addHandler(fh)


logging.setLoggerClass(ColoredLogger)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# logger.debug("This is a debug message")
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")
