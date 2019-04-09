from RPIO import PWM
from time import sleep

class legJoint():
    def __init__(self, gpio_pin_primary, gpio_pin_secondary,
                 orientation_primary, orientation_secondary,
                 forward_pwm_primary, reverse_pwm_primary,
                 forward_pwm_secondary, reverse_pwm_secondary,
                 pause_fwd, pause_backwd,
                 setup_pause_primary, setup_pause_secondary,
                 spiderbot_logger):

        self.spiderbot_logger = spiderbot_logger

        self.gpio_pin_primary = gpio_pin_primary
        self.gpio_pin_secondary = gpio_pin_secondary
        self.servo = PWM.Servo()

        self.front_primary = False
        self.back_primary = False
        self.neutral_primary = False

        self.front_secondary = False
        self.back_secondary = False
        self.neutral_secondary = False

        self.pause_fwd = pause_fwd
        self.pause_backwd = pause_backwd

        self.orientation_primary = orientation_primary
        self.orientation_secondary = orientation_secondary

        self.setup_pause_primary = setup_pause_primary
        self.setup_pause_secondary = setup_pause_secondary

        self.forward_pwm_primary = forward_pwm_primary
        self.reverse_pwm_primary = reverse_pwm_primary

        self.forward_pwm_secondary = forward_pwm_secondary
        self.reverse_pwm_secondary = reverse_pwm_secondary

        if self.orientation_primary == 'right':
            self.setup_pwm_primary = 1400
            self.push_down_pwm_primary = None
        elif self.orientation_primary == 'left':
            self.setup_pwm_primary = 1600
            self.push_down_pwm_primary = None
        elif self.orientation_primary == 'vertical_norm':
            self.setup_pwm_primary = 1400
            self.push_down_pwm_primary = 1500
        elif self.orientation_primary == 'vertical_reverse':
            self.setup_pwm_primary = 1600
            self.push_down_pwm_primary = 1500

        if self.orientation_secondary == 'right':
            self.setup_pwm_secondary = 1400
            self.push_down_pwm_secondary = None
        elif self.orientation_secondary == 'left':
            self.setup_pwm_secondary = 1600
            self.push_down_pwm_secondary = None
        elif self.orientation_secondary == 'vertical_norm':
            self.setup_pwm_secondary = 1400
            self.push_down_pwm_secondary = 1500
        elif self.orientation_secondary == 'vertical_reverse':
            self.setup_pwm_secondary = 1600
            self.push_down_pwm_secondary = 1500

        self.spiderbot_logger.info("Leg object created for GPIO pins: ", self.gpio_pin_primary, " and  ", self.gpio_pin_secondary)
    
    def setup(self):
        self.servo.set_servo(self.gpio_pin_primary, self.setup_pwm_primary)
        self.servo.set_servo(self.gpio_pin_secondary, self.setup_pwm_secondary)
        sleep(1)
        self.servo.stop_servo(self.gpio_pin_primary)
        if(self.gpio_pin_secondary == 26): sleep(0.2)
        self.servo.stop_servo(self.gpio_pin_secondary)

        self.servo.set_servo(self.gpio_pin_primary, self.reverse_pwm_primary)
        self.spiderbot_logger.info("reversing for {} seconds".format(self.setup_pause_primary))
        sleep(self.setup_pause_primary)
        self.servo.stop_servo(self.gpio_pin_primary)

        self.servo.set_servo(self.gpio_pin_secondary, self.reverse_pwm_secondary)
        self.spiderbot_logger.info("reversing for {} seconds".format(self.setup_pause_primary))
        sleep(self.setup_pause_secondary)
        self.servo.stop_servo(self.gpio_pin_secondary)

        self.neutral_primary = True
        self.front_primary = False
        self.back_primary = False

        self.neutral_secondary = True
        self.front_secondary = False
        self.back_secondary = False

        if "vertical" in self.orientation_primary and "vertical" in self.orientation_secondary:
            self.servo.set_servo(self.gpio_pin_primary, self.push_down_pwm_primary)
            self.servo.set_servo(self.gpio_pin_secondary, self.push_down_pwm_secondary)

    def __movement(self, direction):
        self.spiderbot_logger.info("Moving {} for GPIO pins {} and {}".format(direction, self.gpio_pin_primary, self.gpio_pin_secondary))
        if direction == 'forward':
            pause = self.pause_fwd
            pwm_primary = self.forward_pwm_primary
            pwm_secondary = self.forward_pwm_secondary
        elif direction == 'backward':
            pause = self.pause_backwd
            pwm_primary = self.reverse_pwm_primary
            pwm_secondary = self.reverse_pwm_secondary
        elif direction == 'rotate_fwd':
            pause = self.pause_fwd
            pwm_primary = self.forward_pwm_primary
            pwm_secondary = self.reverse_pwm_secondary
        elif direction == 'rotate_bckwd':
            pause = self.pause_backwd
            pwm_primary = self.reverse_pwm_primary
            pwm_secondar = self.forward_pwm_primary
        else:
            self.spiderbot_logger.error("Invalid direction for movement options.")
            exit(1)

        if self.front_primary and self.front_secondary:
            if (direction == 'forward' or direction == 'rotate_fwd'):
                self.spiderbot_logger.info("Legs are already in the forward position and cannot move forward again.")
                return
            elif (direction == 'backward' or direction == 'rotate_bckwd'):
                self.neutral_primary = True
                self.front_primary = False

                self.neutral_secondary = True
                self.front_secondary = False

        elif self.neutral_primary and self.neutral_secondary:
            if (direction == 'forward' or direction == 'rotate_fwd'):
                self.neutral_primary = False
                self.front_primary = True

                self.neutral_secondary = False
                self.front_secondary = True
            elif (direction == 'backward' or direction == 'rotate_bckwd'):
                self.neutral_primary = False
                self.back_primary = True

                self.neutral_secondary = False
                self.back_secondary = True 

        elif self.back_primary and self.back_secondary:
            if (direction == 'forward' or direction == 'rotate_fwd'):
                self.neutral_primary = True
                self.back_primary = False

                self.neutral_secondary = True
                self.back_secondary = False
            elif (direction == 'backward' or direction == 'rotate_bckwd'):
                self.spiderbot_logger.info("Legs are already in the reverse position and cannot move backwards again.")
                return

        self.servo.set_servo(self.gpio_pin_primary, pwm_primary)
        self.servo.set_servo(self.gpio_pin_secondary, pwm_secondary)

        sleep(pause)
        
        self.servo.stop_servo(self.gpio_pin_primary)
        self.servo.stop_servo(self.gpio_pin_secondary)

    def move_forward(self):
        self.__movement(direction='forward')

    def move_backward(self):
        self.__movement(direction='backward')

    def rotate_forward(self):
        self.__movement(direction='rotate_fwd')
        
    def rotate_backward(self):
        self.__movement(direction='rotate_bckwd')

    def push_down(self):
        if self.push_down_pwm_primary is not None and self.push_down_pwm_secondary is not None:
            self.servo.set_servo(self.gpio_pin_primary, self.push_down_pwm_primary)
            self.servo.set_servo(self.gpio_pin_secondary, self.push_down_pwm_secondary)

    def close(self):
        self.servo.stop_servo(self.gpio_pin_primary)
        self.servo.stop_servo(self.gpio_pin_secondary)