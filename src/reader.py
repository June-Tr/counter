import json

SECOND = 0
MINUTE = 1
HOUR = 2
WORK = True
REST = False


def check_input(time_txt: str) -> int:
    """
    :argument time_txt: string contain a number represent time and a character, string represent the unit
    :return integer that repsent SECOND, HOUR or HOUR
    """
    if "m" in time_txt.lower():
        return MINUTE

    if "min" in time_txt.lower():
        return MINUTE

    if "sec" in time_txt.lower():
        return SECOND

    if "s" in time_txt.lower():
        return SECOND

    if "h" in time_txt.lower():
        return HOUR

    if "hour" in time_txt.lower():
        return HOUR


def parse_time_txt(time_txt: str) -> int:
    """
    :param time_txt: expected format "num unit" or "numUnit"
    :return: an int represent the input after translate into second
    """
    time_str: str = ""

    # extract all the time value
    for char in time_txt:
        if not char.isnumeric():
            break

        time_str += char

    # obtain the unit of the number
    unit = check_input(time_txt)

    if unit == SECOND:
        return int(time_str)

    if unit == MINUTE:
        return int(time_str) * 60

    if unit == HOUR:
        return int(time_str) * 60 * 60


class reader:

    def __init__(self, file_dir: str, work_counter: str = "", rest_counter: str = ""):

        self._data = file_dir
        self._work = 0
        self._rest = 0

        if work_counter == "":
            self.read_counter()
        else:

            self._work = parse_time_txt(work_counter)
            self._rest = parse_time_txt(rest_counter)
            self.log()

    def read_counter(self):
        """
        read counter from the file
        """
        with open(self._data, 'r') as data:
            saved_time = json.load(data)

        data.close()
        # prompt user to enter the work time
        if len(saved_time) == 0:
            # prompt user to enter a time.
            work_time_txt = input("Please enter working time with unit: ")

            if len(work_time_txt) == 0:
                print("Invalid value for working time~!!!")
                exit(0)

            self._work = parse_time_txt(work_time_txt)

            # prompt user to enter a time.
            rest_time_txt = input("Please enter rest time with unit: ")

            if len(rest_time_txt) == 0:
                print("Invalid value for rest time~!!!")
                exit(0)

            self._rest = parse_time_txt(rest_time_txt)
            # saved the read version
            self.log()

        else:
            self._work = saved_time["work_time"]
            self._rest = saved_time["rest_time"]

    def log(self):
        """
        save the data in this logger to
        :return:
        """
        # write both into JSON file
        saved_time = {
            "work_time": self._work,
            "rest_time": self._rest
        }
        with open("data.json", 'w') as log:
            json.dump(saved_time, log)

    def get_work(self) -> int:
        """
        Getter
        :return: the time on work counter in s
        """
        return self._work

    def get_rest(self) -> int:
        """
        Getter
        :return: the time in rest counter in s
        """
        return self._rest


