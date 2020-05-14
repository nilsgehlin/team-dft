from render3d import render3d
from dicom_viewer import dicom_viewer
from multiprocessing import Process, Queue, Event, freeze_support

import os

directory = r'stanford-ct-new'

def main():
    mouse_move_event = Event()
    mouse_queue = Queue()
    p1 = Process(target=dicom_viewer, args=(directory, mouse_queue, mouse_move_event))
    p2 = Process(target=render3d, args=(directory, mouse_queue, mouse_move_event))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

if __name__ == '__main__':
    freeze_support()
    Process(target=main).start()


