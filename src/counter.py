'''
Counter object:
which has a : remain time + type
'''
import json
import os
import time
from enum_type import counter_type

COMPLETE: int = 0
TYPE = 0
TIME = 1
CUR = 2


class counter:

    # Construct a counter with a count down + remaining time + current time, All of those are for internal use
    def __init__(self, c_type: counter_type, counter_time):
        self._counter_type = c_type
        self._time = counter_time
        self._cur_time = self._time

    def count_down(self, command_q) -> int:
        """
        Continuously countdown until either:
        - Cur_time come to 0 {successful termination}
        - Interrupt by another process {fail}

        Since there are cur_time : the remaining state for the resume
        :return: termination_status.SUCCESSFUL or termination_status.INTERRUPT
        """

        # Use iteration for decrease the cur_time till 0
        while self._cur_time != COMPLETE:
            # decrement the count and let the process sleep for 1 second
            if command_q.qsize() != 0:
                command = command_q.get()
                if command == 'pause':
                    command_q.put('pause')
                    self._print()
                    self.check_in()
                    return 0

                if command == 'end':
                    command_q.put('end')
                    self.reset_counter()
                    return 0

            time.sleep(1)
            self._cur_time -= 1

        self.reset_counter()
        return 1

    def reset_counter(self):
        """
        Internally reset the counter
        :return: null
        """
        self._cur_time = self._time
        self.clear_log()

    def check_in(self):
        if self._counter_type == counter_type.WORK:
            c_type = 1
        else:
            c_type = 2
        with open("counter_type.json", 'w') as log:
            json.dump({TYPE: c_type,
                       CUR: self._cur_time}, log)
        log.close()

    @staticmethod
    def clear_log():
        with open("counter_type.json", "w") as log:
            json.dump({}, log)
        log.close()

    def set_cur(self, cur):
        self._cur_time = cur

    def get_cur(self):
        return self._cur_time

    def _print(self):
        hour = 0
        min = 0
        second = 0

        hour = self._cur_time // (60 * 60)
        min = (self._cur_time % (60*60)) // 60
        second = self._cur_time % (60)
        os.system("clear")
        print("Remained: " + str(hour) + ":" + str(min) + ":" + str(second))
