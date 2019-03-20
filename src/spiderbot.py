from leg import legJoint
from picam import detect_objects
from time import sleep
from queue import Queue
from threading import Thread
import sys


def main():
    front_right_horizontal = legJoint( gpio_pin=12 )
    front_right_vertical = legJoint( gpio_pin=16 )
    
    front_left_horizontal = legJoint( gpio_pin=19 )
    front_left_vertical = legJoint( gpio_pin=26 )

    q = Queue()
    detection_thread = Thread(target=detect_objects, args=(q,))
    detection_thread.start()

    while True:
        if not q.empty():
            objects = q.get()
            print(objects)
            # for obj in objects:
            #     if obj == "person":
            #         move_forward( front_right_horizontal, front_right_vertical, 'right')
            #         sleep(0.1)
            #         front_right_horizontal.center_joint()
            #         sleep(0.1)

            #     # for _ in range(5):
            #     #     move_forward( front_left_horizontal, front_left_vertical, 'left')
            #     #     sleep(0.1)
            #     #     front_left_horizontal.center_joint()
            #     #     sleep(0.1)

    exit(0)

def  move_forward( joint1, joint2, orientation):
    
    if orientation == 'right':
        joint2.rotate_counter_clockwise()
        sleep(0.1)
        joint1.rotate_counter_clockwise()
        sleep(0.1)
        joint2.center_joint()
    elif orientation == 'left':
        joint2.rotate_clockwise()
        sleep(0.1)
        joint1.rotate_clockwise()
        sleep(0.1)
        joint2.center_joint()
    else:
        raise ValueError 

if __name__ == "__main__":
    main()
