from datetime import datetime


def log(message):
    print(datetime.now(), '-', message)


def log_debug(message, debug):
    if debug:
        print(datetime.now(), '-', 'Debug message:', message)
