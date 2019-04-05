from RPIO import PWM
from time import sleep

class legJoint():
    def __init__(self, gpio_pin_primary, gpio_pin_secondary,
                 orientation_primary, orientation_secondary,
                 pause_primary, pause_secondary,
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

        self.pause_primary = pause_primary
        self.pause_secondary = pause_secondary

        self.orientation_primary = orientation_primary
        self.orientation_secondary = orientation_secondary

        if self.orientation_primary == 'right':
            self.setup_pwm_primary = 1400
            self.setup_pause_primary = setup_pause_primary
            self.forward_pwm_primary = 1300
            self.reverse_pwm_primary = 1700
            self.push_down_pwm_primary = None
        elif self.orientation_primary == 'left':
            self.setup_pwm_primary = 1600
            self.setup_pause_primary = setup_pause_primary
            self.forward_pwm_primary = 1700
            self.reverse_pwm_primary = 1300
            self.push_down_pwm_primary = None
        elif self.orientation_primary == 'vertical_norm':
            self.setup_pwm_primary = 1400
            self.setup_pause_primary = setup_pause_primary
            self.forward_pwm_primary = 1300
            self.reverse_pwm_primary = 1700
            self.push_down_pwm_primary = 1500
        elif self.orientation_primary == 'vertical_reverse':
            self.setup_pwm_primary = 1600
            self.setup_pause_primary = setup_pause_primary
            self.forward_pwm_primary = 1700
            self.reverse_pwm_primary = 1300
            self.push_down_pwm_primary = 1500

        if self.orientation_secondary == 'right':
            self.setup_pwm_secondary = 1400
            self.setup_pause_secondary = setup_pause_secondary
            self.forward_pwm_secondary = 1300
            self.reverse_pwm_secondary = 1700
            self.push_down_pwm_secondary = None
        elif self.orientation_secondary == 'left':
            self.setup_pwm_secondary = 1600
            self.setup_pause_secondary = setup_pause_secondary
            self.forward_pwm_secondary = 1700
            self.reverse_pwm_secondary = 1300
            self.push_down_pwm_secondary = None
        elif self.orientation_secondary == 'vertical_norm':
            self.setup_pwm_secondary = 1400
            self.setup_pause_secondary = setup_pause_secondary
            self.forward_pwm_secondary = 1300
            self.reverse_pwm_secondary = 1700
            self.push_down_pwm_secondary = 1500
        elif self.orientation_secondary == 'vertical_reverse':
            self.setup_pwm_secondary = 1600
            self.setup_pause_secondary = setup_pause_secondary
            self.forward_pwm_secondary = 1700
            self.reverse_pwm_secondary = 1300
            self.push_down_pwm_secondary = 1500

        self.spiderbot_logger.info("Leg object created for GPIO pins: ", self.gpio_pin_primary, " and  ", self.gpio_pin_secondary)
    
    def setup(self):
        self.servo.set_servo(self.gpio_pin_primary, self.setup_pwm_primary)
        self.servo.set_servo(self.gpio_pin_secondary, self.setup_pwm_secondary)
        sleep(1)
        self.servo.stop_servo(self.gpio_pin_primary)
        self.servo.stop_servo(self.gpio_pin_secondary)

        self.servo.set_servo(self.gpio_pin_primary, self.reverse_pwm_primary)
        sleep(self.setup_pause_primary)
        self.servo.stop_servo(self.gpio_pin_primary)

        self.servo.set_servo(self.gpio_pin_secondary, self.reverse_pwm_secondary)
        sleep(self.setup_pause_secondary)
        self.servo.stop_servo(self.gpio_pin_secondary)

        self.neutral_primary = True
        self.neutral_secondary = True

    def move_forward(self):
        if self.orientation_primary == 'right' or self.orientation_primary == 'left' and \
           self.orientation_secondary == 'right' or self.orientation_secondary == 'left':
            
            if self.front_primary and self.front_secondary:
                self.spiderbot_logger.info("Legs are already in the forward position and cannot move forwrd again.")
                pass
            elif self.neutral_primary and self.neutral_secondary:

                self.servo.set_servo(self.gpio_pin_primary, self.forward_pwm_primary)
                self.servo.set_servo(self.gpio_pin_secondary, self.forward_pwm_secondary)

                sleep(self.pause_primary)
                
                self.servo.stop_servo(self.gpio_pin_primary)
                self.servo.stop_servo(self.gpio_pin_secondary)
                
                self.neutral_primary = False
                self.front_primary = True

                self.neutral_secondary = False
                self.front_secondary = True

            elif self.back_primary and self.back_secondary:

                self.servo.set_servo(self.gpio_pin_primary, self.forward_pwm_primary)
                self.servo.set_servo(self.gpio_pin_secondary, self.forward_pwm_secondary)

                sleep(self.pause_primary)
                
                self.servo.stop_servo(self.gpio_pin_primary)
                self.servo.stop_servo(self.gpio_pin_secondary)
                
                self.back_primary = False
                self.neutral_primary = True

                self.back_secondary = False
                self.neutral_secondary = True
            else:
                self.spiderbot_logger.error("Positions of leg pair are in an illegal state.")

        elif self.orientation_primary == 'vertical_norm' or self.orientation_primary == 'vertical_revers' and \
             self.orientation_secondary == 'vertical_norm' or self.orientation_secondary == 'vertical_revers':

            if self.front_primary and self.front_secondary:
                self.spiderbot_logger.info("Legs are already in the forward position and cannot move forwrd again.")
                pass
            elif self.neutral_primary and self.neutral_secondary:

                self.servo.set_servo(self.gpio_pin_primary, self.forward_pwm_primary)
                self.servo.set_servo(self.gpio_pin_secondary, self.forward_pwm_secondary)

                sleep(self.pause_primary)
                
                self.servo.stop_servo(self.gpio_pin_primary)
                self.servo.stop_servo(self.gpio_pin_secondary)
                
                self.neutral_primary = False
                self.front_primary = True

                self.neutral_secondary = False
                self.front_secondary = True

            elif self.back_primary and self.back_secondary:
                self.spiderbot_logger.info("The 'back' position is an illegal state for vertical legs.")
                pass
            else:
                self.spiderbot_logger.error("Positions of leg pair are in an illegal state.")
        
        else:
            self.spiderbot_logger.error("The orientions of the leg pair are in an illegal combination.")


    def move_backward(self):
        if self.orientation_primary == 'right' or self.orientation_primary == 'left' and \
           self.orientation_secondary == 'right' or self.orientation_secondary == 'left':
            
            if self.front_primary and self.front_secondary:
    
                self.servo.set_servo(self.gpio_pin_primary, self.reverse_pwm_primary)
                self.servo.set_servo(self.gpio_pin_secondary, self.reverse_pwm_secondary)

                sleep(self.pause_primary)
                
                self.servo.stop_servo(self.gpio_pin_primary)
                self.servo.stop_servo(self.gpio_pin_secondary)
                
                self.front_primary = False
                self.neutral_primary = True

                self.front_secondary = False
                self.neutral_secondary = True

            elif self.neutral_primary and self.neutral_secondary:

                self.servo.set_servo(self.gpio_pin_primary, self.reverse_pwm_primary)
                self.servo.set_servo(self.gpio_pin_secondary, self.reverse_pwm_secondary)

                sleep(self.pause_primary)
                
                self.servo.stop_servo(self.gpio_pin_primary)
                self.servo.stop_servo(self.gpio_pin_secondary)
                
                self.neutral_primary = False
                self.back_primary = True

                self.neutral_secondary = False
                self.back_secondary = True

            elif self.back_primary and self.back_secondary:
                self.spiderbot_logger.info("Legs are already in the rear position and cannot move forwrd again.")
                pass
                
            else:
                self.spiderbot_logger.error("Positions of leg pair are in an illegal state.")

        elif self.orientation_primary == 'vertical_norm' or self.orientation_primary == 'vertical_revers' and \
             self.orientation_secondary == 'vertical_norm' or self.orientation_secondary == 'vertical_revers':

            if self.front_primary and self.front_secondary:
                
                self.servo.set_servo(self.gpio_pin_primary, self.reverse_pwm_primary)
                self.servo.set_servo(self.gpio_pin_secondary, self.reverse_pwm_secondary)

                sleep(self.pause_primary)
                
                self.servo.stop_servo(self.gpio_pin_primary)
                self.servo.stop_servo(self.gpio_pin_secondary)
                
                self.front_primary = False
                self.neutral_primary = True

                self.front_secondary = False
                self.neutral_secondary = True

            elif self.neutral_primary and self.neutral_secondary:
                self.spiderbot_logger.info("Legs are already in the forward position and cannot move forwrd again.")
                pass
                
            elif self.back_primary and self.back_secondary:
                self.spiderbot_logger.info("The 'back' position is an illegal state for vertical legs.")
                pass

            else:
                self.spiderbot_logger.error("Positions of leg pair are in an illegal state.")
        
        else:
            self.spiderbot_logger.error("The orientions of the leg pair are in an illegal combination.")


    # def center_joint(self):
    #     if self.lower_limit == True:
    #         self.servo.set_servo(self.gpio_pin, self.forward_pwm)
    #         sleep(self.half_rotation)
    #         self.servo.stop_servo(self.gpio_pin)
    #         self.lower_limit = False
    #         self.neutral = True
    #     elif self.upper_limit == True:
    #         self.servo.set_servo(self.gpio_pin, self.reverse_pwm)
    #         sleep(self.half_rotation)
    #         self.servo.stop_servo(self.gpio_pin)
    #         self.upper_limit = False
    #         self.neutral = True
    #     else:
    #         pass

    def push_down(self):
        if self.push_down_pwm_primary is not None and self.push_down_pwm_secondary is not None:
            self.servo.set_servo(self.gpio_pin_primary, self.push_down_pwm_primary)
            self.servo.set_servo(self.gpio_pin_secondary, self.push_down_pwm_secondary)

    def close(self):
        self.servo.stop_servo(self.gpio_pin_primary)
        self.servo.stop_servo(self.gpio_pin_secondary)