from RPIO import PWM
from time import sleep

class legJoint():
    def __init__(self, gpio_pin, orientation):
        self.gpio_pin = gpio_pin
        self.servo = PWM.Servo()
        self.upper_limit = False
        self.lower_limit = False
        self.neutral = True
        self.half_rotation = 0.15
        self.full_rotation = 0.3
        if orientation == 'right':
            self.forward_pwm = 1300
            self.reverse_pwm = 1700
            self.push_down_pwm = None
        elif orientation == 'left':
            self.forward_pwm = 1700
            self.reverse_pwm = 1300
            self.push_down_pwm = None
        elif orientation == 'vertical_norm':
            self.forward_pwm = 1300
            self.reverse_pwm = 1700
            self.push_down_pwm = 1520
        elif orientation == 'vertical_reverse':
            self.forward_pwm = 1700
            self.reverse_pwm = 1300
            self.push_down_pwm = 1480
    
    def move_forward(self):
        if self.upper_limit != True and self.neutral == True:
            # print("moving GPIO %f for %f seconds at pwm %f" % (self.gpio_pin, self.half_rotation, self.forward_pwm))
            self.servo.set_servo(self.gpio_pin, self.forward_pwm)
            sleep(self.half_rotation)
            self.servo.stop_servo(self.gpio_pin)
            self.upper_limit = True
            self.neutral = False
        elif self.upper_limit != True and self.lower_limit == True:
            self.servo.set_servo(self.gpio_pin, self.forward_pwm)
            sleep(self.full_rotation)
            self.servo.stop_servo(self.gpio_pin)
            self.upper_limit = True
            self.lower_limit = False
        else:
            pass

    def move_backward(self):
        if self.lower_limit != True and self.neutral == True:
            self.servo.set_servo(self.gpio_pin, self.reverse_pwm)
            sleep(self.half_rotation)
            self.servo.stop_servo(self.gpio_pin)
            self.lower_limit = True
            self.neutral = False
        elif self.lower_limit != True and self.upper_limit == True:
            self.servo.set_servo(self.gpio_pin, self.reverse_pwm)
            sleep(self.full_rotation)
            self.servo.stop_servo(self.gpio_pin)
            self.lower_limit = True
            self.upper_limit = False
        else:
            pass

    def center_joint(self):
        if self.lower_limit == True:
            self.servo.set_servo(self.gpio_pin, self.forward_pwm)
            sleep(self.half_rotation)
            self.servo.stop_servo(self.gpio_pin)
            self.lower_limit = False
            self.neutral = True
        elif self.upper_limit == True:
            self.servo.set_servo(self.gpio_pin, self.reverse_pwm)
            sleep(self.half_rotation)
            self.servo.stop_servo(self.gpio_pin)
            self.upper_limit = False
            self.neutral = True
        else:
            pass

    def push_down(self):
        if self.push_down_pwm is not None:
            self.servo.set_servo(self.gpio_pin, self.push_down_pwm)
    def calibrate(self):
        self.servo.set_servo(self.gpio_pin, 1500)
        sleep(60)