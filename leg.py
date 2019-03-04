from RPIO import PWM
from time import sleep

class legJoint():
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self.servo = PWM.Servo()
        self.upper_limit = False
        self.lower_limit = False
        self.neutral = True
        self.half_rotation = 0.15
        self.full_rotation = 0.3
        self.clockwise_pwm = 1300
        self.counter_clockwise_pwm = 1700
    
    def rotate_clockwise(self):
        if self.upper_limit != True and self.neutral == True:
            self.servo.set_servo(self.gpio_pin, self.clockwise_pwm)
            sleep(self.half_rotation)
            self.servo.stop_servo(self.gpio_pin)
            self.upper_limit = True
            self.neutral = False
        elif self.upper_limit != True and self.lower_limit == True:
            self.servo.set_servo(self.gpio_pin, self.clockwise_pwm)
            sleep(self.full_rotation)
            self.servo.stop_servo(self.gpio_pin)
            self.upper_limit = True
            self.lower_limit = False
        else:
            pass

    def rotate_counter_clockwise(self):
        if self.lower_limit != True and self.neutral == True:
            self.servo.set_servo(self.gpio_pin, self.counter_clockwise_pwm)
            sleep(self.half_rotation)
            self.servo.stop_servo(self.gpio_pin)
            self.lower_limit = True
            self.neutral = False
        elif self.lower_limit != True and self.upper_limit == True:
            self.servo.set_servo(self.gpio_pin, self.counter_clockwise_pwm)
            sleep(self.full_rotation)
            self.servo.stop_servo(self.gpio_pin)
            self.lower_limit = True
            self.upper_limit = False
        else:
            pass

    def center_joint(self):
        if self.lower_limit == True:
            self.servo.set_servo(self.gpio_pin, self.clockwise_pwm)
            sleep(self.half_rotation)
            self.servo.stop_servo(self.gpio_pin)
            self.lower_limit = False
            self.neutral = True
        elif self.upper_limit == True:
            self.servo.set_servo(self.gpio_pin, self.counter_clockwise_pwm)
            sleep(self.half_rotation)
            self.servo.stop_servo(self.gpio_pin)
            self.upper_limit = False
            self.neutral = True
        else:
            pass

    def calibrate(self):
        self.servo.set_servo(self.gpio_pin, 1500)
        sleep(60)