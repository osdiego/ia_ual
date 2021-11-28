import argparse


# Inspired by


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Program to filter spam messages and emails.')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Parameter to choose when to log things related with the resolution.')
    args = parser.parse_args()
