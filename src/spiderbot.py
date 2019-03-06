from leg import legJoint
from time import sleep


def main():
    front_right_horizontal = legJoint( gpio_pin=21 )
    front_right_vertical = legJoint( gpio_pin=20 )
    
    for _ in range(5):
        move_forward( front_right_horizontal, front_right_vertical, 'right')
        sleep(0.1)
        front_right_horizontal.center_joint()
        sleep(0.1)

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