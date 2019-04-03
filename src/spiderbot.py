from leg import legJoint
# from picam import detect_objects
from time import sleep
from multiprocessing import Process, Queue
from logging import Logger
from getch import getch
import sys


def main():
    front_right_horizontal = legJoint( gpio_pin=27, orientation='right' )
    front_right_vertical = legJoint( gpio_pin=22, orientation='vertical_norm' )
    
    front_left_horizontal = legJoint( gpio_pin=19, orientation='left' )
    front_left_vertical = legJoint( gpio_pin=13, orientation='vertical_norm' )

    mid_right_horizontal = legJoint( gpio_pin=17, orientation='right' )
    mid_right_vertical = legJoint( gpio_pin=18, orientation='vertical_norm' )
    
    mid_left_horizontal = legJoint( gpio_pin=26, orientation='left' )
    mid_left_vertical = legJoint( gpio_pin=16, orientation='vertical_reverse' )

    back_right_horizontal = legJoint( gpio_pin=24, orientation='right' )
    back_right_vertical = legJoint( gpio_pin=23, orientation='vertical_norm' )
    
    back_left_horizontal = legJoint( gpio_pin=25, orientation='left' )
    back_left_vertical = legJoint( gpio_pin=12, orientation='vertical_norm' )

    q = Queue()
    put_thread = Process(target=get_key, args=(q,))
    put_thread.start()

    while True:
        key = q.get()
        print(key)
        if key is None:
            pass
        elif key.lower() == 'q':
            sleep(1)
            q.put('exit')
            print("terminated thread - press any key")
            break
        elif key.lower() == 'c':
            front_left_vertical.rotate_clockwise()
        elif key.lower() == 'x':
            front_right_vertical.servo.set_servo(22, 1520)
            front_left_vertical.servo.set_servo(13, 1520)
            mid_right_vertical.servo.set_servo(18, 1520)
            mid_left_vertical.servo.set_servo(16, 1480)
            back_right_vertical.servo.set_servo(23, 1520)
            back_left_vertical.servo.set_servo(12, 1520)
        elif key.lower() == 'v':
            front_right_vertical.servo.set_servo(22, 1700)
            front_left_vertical.servo.set_servo(13, 1700)
            mid_right_vertical.servo.set_servo(18, 1700)
            mid_left_vertical.servo.set_servo(16, 1300)
            back_right_vertical.servo.set_servo(23, 1700)
            back_left_vertical.servo.set_servo(12, 1700)
        elif key.lower() == 'z':
            front_right_vertical.servo.stop_servo(22)
            front_left_vertical.servo.stop_servo(13)
            mid_right_vertical.servo.stop_servo(18)
            mid_left_vertical.servo.stop_servo(16)
            back_right_vertical.servo.stop_servo(23)
            back_left_vertical.servo.stop_servo(12)
        elif key.lower() == 'f':
            front_left_vertical.servo.set_servo(13, 1300)
            back_right_vertical.servo.set_servo(23, 1300)
            sleep(0.15)
            front_left_vertical.servo.stop_servo(13)
            back_right_vertical.servo.stop_servo(23)
            front_left_horizontal.servo.set_servo(19, 1700)
            back_right_horizontal.servo.set_servo(24, 1300)
            sleep(0.15)
            front_left_horizontal.servo.stop_servo(19)
            back_left_horizontal.servo.stop_servo(24)
            front_left_vertical.servo.set_servo(13, 1700)
            back_right_vertical.servo.set_servo(23, 1700)
            sleep(0.15)
            front_left_vertical.servo.set_servo(13, 1520)
            back_right_vertical.servo.set_servo(23, 1520)
        elif key.lower() == 'g':
            front_left_vertical.move_forward()
            back_right_vertical.move_forward()

            front_left_horizontal.move_forward()
            back_right_horizontal.move_forward()

            front_left_vertical.move_backward()
            back_right_vertical.move_backward()

            front_left_vertical.push_down()
            back_right_vertical.push_down()            




    #         objects = q.get()
    #         print(objects)
    #         # for obj in objects:
    #         #     if obj == "person":
    #         #         move_forward( front_right_horizontal, front_right_vertical, 'right')
    #         #         sleep(0.1)
    #         #         front_right_horizontal.center_joint()
    #         #         sleep(0.1)

    #         #     # for _ in range(5):
    #         #     #     move_forward( front_left_horizontal, front_left_vertical, 'left')
    #         #     #     sleep(0.1)
    #         #     #     front_left_horizontal.center_joint()
    #         #     #     sleep(0.1)

    exit(0)

def get_key(q):
    while True:
        try:
            response = q.get(block=False)
            print(response)
            if  response == 'exit':
                break
        except:
            pass
        key = getch()
        q.put(key)
        print("put key in queue")
        sleep(1)
    
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
        joint1.rotate_counter_clockwise()
        sleep(0.1)
        joint2.center_joint()
    else:
        raise ValueError 
    
    return
  
if __name__ == "__main__":
    main()
