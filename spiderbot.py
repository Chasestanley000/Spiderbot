from leg import legJoint
from time import sleep


def main():
    front_right_horizontal = legJoint( gpio_pin=21 )
    front_right_vertical = legJoint( gpio_pin=20 )

    move_forward( front_right_horizontal, front_right_vertical, 'right')

    exit(0)

def  move_forward( joint1, joint2, orientation):
    
    if orientation == 'right':
        joint2.rotate_counter_clockwise()
        joint1.rotate_counter_clockwise()
        joint2.center_joint()
    elif orientation == 'left':
        joint2.rotate_clockwise()
        joint1.rotate_clockwise()
        joint2.center_joint()
    else:
        raise ValueError 

if __name__ == "__main__":
    main()