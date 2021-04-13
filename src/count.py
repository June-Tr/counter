#!/usr/bin/python3
import json
import os
import sys
import time
from multiprocessing import Queue
import pydub.playback
from pydub import AudioSegment
from counter import counter, TYPE, CUR
from enum_type import counter_type
from reader import reader

if len(sys.argv) < 2:
    log = reader("data.json")
else:
    log = reader("data.json", sys.argv[1], sys.argv[2])

# create the counter
work_counter = counter(counter_type.WORK, log.get_work())
rest_counter = counter(counter_type.REST, log.get_rest())
cur: counter

q = Queue()
command_q = Queue()


def play_sound():
    sound = AudioSegment.from_file("C_bell.mp3")
    pydub.playback.play(sound)
    print(chr(27)+'[2j')


def counting_task():
    global work_counter, rest_counter, cur

    def read_cur():
        global cur

        with open("counter_type.json", 'r') as log:
            data = json.load(log)
        if len(data) == 0:
            cur = work_counter
        else:
            cur = work_counter if data[str(TYPE)] == counter_type.WORK else rest_counter
            cur.set_cur(data[str(CUR)])
        return cur

    cur = read_cur()

    while True:
        mode = cur.count_down(command_q)

        # make a process to play sound
        # when counter finish swap to another counter
        if mode:
            l_pid = os.fork()
            if l_pid:
                cur = rest_counter if cur == work_counter else work_counter
            else:
                play_sound()
                os.system('clear')
                exit(0)

        else:
            break


pid = -1
while True:

    command = input()

    # if input is to create the counter:
    # pork and make child run the counting_task
    if command.lower() == 'start':
        # ensure there only one process who responsible to do counting down

        pid = os.fork()

        # make the child do the counting task
        if pid != 0:
            time.sleep(1)
            continue
        else:
            # append the pid to the queue in case parent want to kill it
            q.put(pid)
            exec("counting_task()")

            command = command_q.get()
            if command == "end" or command == 'pause':
                break

    if command.lower() == 'resume':
        # ensure there only one process who responsible to do counting down
        os.system("clear")
        pid = os.fork()

        # make the child do the counting task
        if pid != 0:
            time.sleep(1)
            continue
        else:
            # append the pid to the queue in case parent want to kill it
            q.put(pid)
            exec("counting_task()")

            command = command_q.get()
            if command == "end" or command == 'pause':
                command_q.put(command)
                break

    if command.lower() == 'pause':

        if pid != 0:
            command_q.put("pause")

    if command.lower() == 'end':

        if pid != 0:
            command_q.put("end")
        cur.clear_log()
        sys.exit(0)
