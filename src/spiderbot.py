import sys
from multiprocessing import Process, Queue
from time import sleep
from getch import getch

from leg import legJoint
from logger import Logger
# from picam import detect_objects


def main():
    # Create a stream and file logger to record data
    spiderbot_logger = Logger('spiderbot')
    spiderbot_logger.set_file_handler('spiderbot.log', 'INFO')
    spiderbot_logger.set_stream_handler(sys.stdout, 'INFO')

    # Create objects for each servo
    spiderbot_logger.info("creating leg objects...")

    front_right_horizontal = legJoint( gpio_pin_primary=27, gpio_pin_secondary=25,
                                       orientation_primary='right', orientation_secondary='left',
                                       forward_pwm_primary=1440, reverse_pwm_primary=1570,
                                       forward_pwm_secondary=1570, reverse_pwm_secondary=1430,
                                       pause_fwd=0.18, pause_backwd=0.18,
                                       setup_pause_primary=0.4, setup_pause_secondary=0.31,
                                       spiderbot_logger=spiderbot_logger )
    
    front_right_vertical = legJoint( gpio_pin_primary=22, gpio_pin_secondary=12,
                                     orientation_primary='vertical_norm', orientation_secondary='vertical_norm',
                                     forward_pwm_primary=1300, reverse_pwm_primary=1700,
                                     forward_pwm_secondary=1300, reverse_pwm_secondary=1700,
                                     pause_fwd=0.18, pause_backwd=0.23,
                                     setup_pause_primary=0.35, setup_pause_secondary=0.35,
                                     spiderbot_logger=spiderbot_logger )

    front_left_horizontal = legJoint( gpio_pin_primary=19, gpio_pin_secondary=24,
                                      orientation_primary='left', orientation_secondary='right',
                                      forward_pwm_primary=1700, reverse_pwm_primary=1300,
                                      forward_pwm_secondary=1420, reverse_pwm_secondary=1580,
                                      pause_fwd=0.18, pause_backwd=0.18,
                                      setup_pause_primary=0.34, setup_pause_secondary=0.37,
                                      spiderbot_logger=spiderbot_logger )

    front_left_vertical = legJoint( gpio_pin_primary=13, gpio_pin_secondary=23,
                                    orientation_primary='vertical_norm', orientation_secondary='vertical_norm',
                                    forward_pwm_primary=1300, reverse_pwm_primary=1700,
                                    forward_pwm_secondary=1300, reverse_pwm_secondary=1700,
                                    pause_fwd=0.18, pause_backwd=0.23,
                                    setup_pause_primary=0.35, setup_pause_secondary=0.35,
                                    spiderbot_logger=spiderbot_logger )

    mid_right_horizontal = legJoint( gpio_pin_primary=17, gpio_pin_secondary=26,
                                     orientation_primary='right', orientation_secondary='left',
                                     forward_pwm_primary=1440, reverse_pwm_primary=1610,
                                     forward_pwm_secondary=1570, reverse_pwm_secondary=1430,
                                     pause_fwd=0.18, pause_backwd=0.18,
                                     setup_pause_primary=0.3, setup_pause_secondary=0.38,
                                     spiderbot_logger=spiderbot_logger )

    mid_right_vertical = legJoint( gpio_pin_primary=18, gpio_pin_secondary=16,
                                   orientation_primary='vertical_norm', orientation_secondary='vertical_reverse',
                                   forward_pwm_primary=1300, reverse_pwm_primary=1700,
                                   forward_pwm_secondary=1700, reverse_pwm_secondary=1300,
                                   pause_fwd=0.18, pause_backwd=0.23,
                                   setup_pause_primary=0.35, setup_pause_secondary=0.35,
                                   spiderbot_logger=spiderbot_logger )
  
    spiderbot_logger.info("All leg objects created...")

    # Create a Queue and thread for the Object detection process
    # spiderbot_logger.info("Creating and staring object detection thread...")                                                  
    # obj_detection_queue = Queue()
    # obj_detection_thread = Process(target=detect_objects, args=(obj_detection_queue, spiderbot_logger,))
    # obj_detection_thread.start()
    # spiderbot_logger.info("Object detection thread created and started...")

    spiderbot_logger.info("Set legs to default position...")
    front_right_vertical.setup()
    front_right_horizontal.setup()

    front_left_vertical.setup()
    front_left_horizontal.setup()

    mid_right_vertical.setup()
    mid_right_horizontal.setup()
    spiderbot_logger.info("All legs set to default position")

    spiderbot_logger.info("getch thread being created")
    q = Queue()
    put_thread = Process(target=get_key, args=(q, spiderbot_logger, ))
    put_thread.start()
    spiderbot_logger.info("getch thread started")
    while True:
        key = q.get()
        spiderbot_logger.info("key pressed: ", key)
        if key is None:
            pass
        elif key.lower() == 'q':
            sleep(1)
            q.put('exit')
            spiderbot_logger.info("terminated thread - press any key")
            put_thread.join()
            break

        elif key.lower() == 's':
            front_right_vertical.setup()
            front_right_horizontal.setup()

            front_left_vertical.setup()
            front_left_horizontal.setup()

            mid_right_vertical.setup()
            mid_right_horizontal.setup()

        elif key.lower() == 'x':
            mid_right_horizontal.move_forward()
        elif key.lower() == 'z':
            mid_right_horizontal.move_backward()

        elif key.lower() == 'r':
            mid_right_horizontal.forward_pwm_primary += 10
            spiderbot_logger.info("\nforward_pwm_primary = ", mid_right_horizontal.forward_pwm_primary)
        elif key.lower() == 'e':
            mid_right_horizontal.forward_pwm_primary -= 10
            spiderbot_logger.info("\nforward_pwm_primary = ", mid_right_horizontal.forward_pwm_primary)
        elif key.lower() == 'f':
            mid_right_horizontal.forward_pwm_secondary += 10   
            spiderbot_logger.info("\nforward_pwm_secondary = ", mid_right_horizontal.forward_pwm_secondary) 
        elif key.lower() == 'd':
            mid_right_horizontal.forward_pwm_secondary -= 10
            spiderbot_logger.info("\nforward_pwm_secondary = ", mid_right_horizontal.forward_pwm_secondary) 

        elif key.lower() == 'y':
            mid_right_horizontal.reverse_pwm_primary += 10
            spiderbot_logger.info("\nreverse_pwm_primary = ", mid_right_horizontal.reverse_pwm_primary)
        elif key.lower() == 't':
            mid_right_horizontal.reverse_pwm_primary -= 10
            spiderbot_logger.info("\nreverse_pwm_primary = ", mid_right_horizontal.reverse_pwm_primary)
        elif key.lower() == 'h':
            mid_right_horizontal.reverse_pwm_secondary += 10   
            spiderbot_logger.info("\nreverse_pwm_secondary = ", mid_right_horizontal.reverse_pwm_secondary) 
        elif key.lower() == 'g':
            mid_right_horizontal.reverse_pwm_secondary -= 10
            spiderbot_logger.info("\nreverse_pwm_secondary = ", mid_right_horizontal.reverse_pwm_secondary) 

        elif key.lower() == 'i':
            mid_right_horizontal.setup_pause_primary += 0.1
            spiderbot_logger.info("\nsetup_pause_primary = ", mid_right_horizontal.setup_pause_primary)
        elif key.lower() == 'u':
            mid_right_horizontal.setup_pause_primary -= 0.1
            spiderbot_logger.info("\nsetup_pause_primary = ", mid_right_horizontal.setup_pause_primary)
        elif key.lower() == 'k':
            mid_right_horizontal.setup_pause_secondary += 0.1  
            spiderbot_logger.info("\nsetup_pause_secondary = ", mid_right_horizontal.setup_pause_secondary)  
        elif key.lower() == 'j':
            mid_right_horizontal.setup_pause_secondary -= 0.1
            spiderbot_logger.info("\nsetup_pause_secondary = ", mid_right_horizontal.setup_pause_secondary)

        elif key.lower() == 'p':
            spiderbot_logger.info("\nforward_pwm_primary   = ", mid_right_horizontal.forward_pwm_primary,
                                  "\nforward_pwm_secondary = ", mid_right_horizontal.forward_pwm_secondary,
                                  "\nreverse_pwm_primary   = ", mid_right_horizontal.reverse_pwm_primary,
                                  "\nreverse_pwm_secondary = ", mid_right_horizontal.reverse_pwm_secondary,
                                  "\nsetup_pause_primary   = ", mid_right_horizontal.setup_pause_primary,
                                  "\nsetup_pause_secondary = ", mid_right_horizontal.setup_pause_secondary)
        

    # front_right_horizontal.close()
    # front_right_vertical.close()

    # front_left_horizontal.close()
    # front_left_vertical.close()

    mid_right_horizontal.close()
    # mid_right_vertical.close()       

    exit(0)

def get_key(q, spiderbot_logger):
    while True:
        try:
            response = q.get(block=False)
            spiderbot_logger.info(response)
            if  response == 'exit':
                break
        except:
            pass
        key = getch()
        q.put(key)
        spiderbot_logger.info("put key in queue")
        sleep(1)

  
if __name__ == "__main__":
    main()
