import sys
from multiprocessing import Process, Queue
from time import sleep
from getch import getch

from leg import legJoint
from logger import Logger
from picam import detect_objects


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
                                     forward_pwm_primary=1300, reverse_pwm_primary=1800,
                                     forward_pwm_secondary=1300, reverse_pwm_secondary=1800,
                                     pause_fwd=0.18, pause_backwd=0.25,
                                     setup_pause_primary=0.4, setup_pause_secondary=0.4,
                                     spiderbot_logger=spiderbot_logger )

    front_left_horizontal = legJoint( gpio_pin_primary=19, gpio_pin_secondary=24,
                                      orientation_primary='left', orientation_secondary='right',
                                      forward_pwm_primary=1700, reverse_pwm_primary=1300,
                                      forward_pwm_secondary=1420, reverse_pwm_secondary=1580,
                                      pause_fwd=0.18, pause_backwd=0.18,
                                      setup_pause_primary=0.31, setup_pause_secondary=0.4,
                                      spiderbot_logger=spiderbot_logger )

    front_left_vertical = legJoint( gpio_pin_primary=13, gpio_pin_secondary=23,
                                    orientation_primary='vertical_norm', orientation_secondary='vertical_norm',
                                    forward_pwm_primary=1300, reverse_pwm_primary=1800,
                                    forward_pwm_secondary=1300, reverse_pwm_secondary=1800,
                                    pause_fwd=0.18, pause_backwd=0.25,
                                    setup_pause_primary=0.4, setup_pause_secondary=0.4,
                                    spiderbot_logger=spiderbot_logger )

    mid_right_horizontal = legJoint( gpio_pin_primary=17, gpio_pin_secondary=26,
                                     orientation_primary='right', orientation_secondary='right',
                                     forward_pwm_primary=1440, reverse_pwm_primary=1570,
                                     forward_pwm_secondary=1430, reverse_pwm_secondary=1610,
                                     pause_fwd=0.18, pause_backwd=0.18,
                                     setup_pause_primary=0.33, setup_pause_secondary=0.38,
                                     spiderbot_logger=spiderbot_logger )

    mid_right_vertical = legJoint( gpio_pin_primary=18, gpio_pin_secondary=16,
                                   orientation_primary='vertical_norm', orientation_secondary='vertical_reverse',
                                   forward_pwm_primary=1300, reverse_pwm_primary=1800,
                                   forward_pwm_secondary=1700, reverse_pwm_secondary=1200,
                                   pause_fwd=0.18, pause_backwd=0.25,
                                   setup_pause_primary=0.4, setup_pause_secondary=0.4,
                                   spiderbot_logger=spiderbot_logger )
  
    spiderbot_logger.info("All leg objects created...")

    # Create a Queue and thread for the Object detection process
    spiderbot_logger.info("Creating and staring object detection thread...")                                                  
    obj_detection_queue = Queue()
    obj_detection_thread = Process(target=detect_objects, args=(obj_detection_queue, spiderbot_logger,))
    obj_detection_thread.start()
    spiderbot_logger.info("Object detection thread created and started...")

    # run the setup function for each pair of legs
    spiderbot_logger.info("Set legs to default position...")
    front_right_vertical.setup()
    front_right_horizontal.setup()

    front_left_vertical.setup()
    front_left_horizontal.setup()

    mid_right_vertical.setup()
    mid_right_horizontal.setup()
    spiderbot_logger.info("All legs set to default position")

    turn_count = 0
    
    while True:
        sleep(1)
        try:
            detected_object = obj_detection_queue.get(block=False)
        except:
            spiderbot_logger.info("No object detected")
            detected_object = None

        if detected_object is None:
            spiderbot_logger.info("Turn count is currently: ", turn_count)
            # if turn_count % 8 == 0:
            #     front_left_vertical.move_forward()
            #     front_left_horizontal.rotate_forward()
            #     front_left_vertical.move_backward()
            #     front_left_vertical.push_down()

            #     mid_right_vertical.move_forward()
            #     mid_right_horizontal.rotate_forward()
            #     mid_right_vertical.move_backward()
            #     mid_right_vertical.push_down()

            #     front_right_vertical.move_forward()
            #     front_left_horizontal.rotate_forward()
            #     mid_right_horizontal.move_backward()
            #     front_right_vertical.move_backward()
            #     front_right_vertical.push_down()

            if turn_count % 2 == 0:
                front_left_vertical.move_forward()
                front_left_horizontal.move_forward()
                front_left_vertical.move_backward()
                front_left_vertical.push_down()

                mid_right_vertical.move_forward()
                mid_right_horizontal.move_forward()
                mid_right_vertical.move_backward()
                mid_right_vertical.push_down()

                front_right_vertical.move_forward()
                front_left_horizontal.move_backward()
                mid_right_horizontal.move_backward()
                front_right_vertical.move_backward()
                front_right_vertical.push_down()
                
            else:
                front_right_vertical.move_forward()
                front_right_horizontal.move_forward()
                front_right_vertical.move_backward()
                front_right_vertical.push_down()

                mid_right_vertical.move_forward()
                mid_right_horizontal.move_forward()
                mid_right_vertical.move_backward()
                mid_right_vertical.push_down()

                front_left_vertical.move_forward()
                front_right_horizontal.move_backward()
                mid_right_horizontal.move_backward()
                front_left_vertical.move_backward()
                front_right_vertical.push_down()
            
            turn_count += 1

        elif detected_object == 'person':
            turn_count = 0
            while turn_count < 10:
                if turn_count % 2 == 0:
                    front_left_vertical.move_forward()
                    front_left_horizontal.move_forward()
                    front_left_vertical.move_backward()
                    front_left_vertical.push_down()

                    mid_right_vertical.move_forward()
                    mid_right_horizontal.move_forward()
                    mid_right_vertical.move_backward()
                    mid_right_vertical.push_down()

                    front_right_vertical.move_forward()
                    front_left_horizontal.move_backward()
                    mid_right_horizontal.move_backward()
                    front_right_vertical.move_backward()
                    front_right_vertical.push_down()
                else:
                    front_left_vertical.move_forward()
                    front_left_horizontal.move_forward()
                    front_left_vertical.move_backward()
                    front_left_vertical.push_down()

                    mid_right_vertical.move_forward()
                    mid_right_horizontal.move_forward()
                    mid_right_vertical.move_backward()
                    mid_right_vertical.push_down()

                    front_right_vertical.move_forward()
                    front_left_horizontal.move_backward()
                    mid_right_horizontal.move_backward()
                    front_right_vertical.move_backward()
                    front_right_vertical.push_down()
                turn_count += 1
            break

    front_right_horizontal.close()
    front_right_vertical.close()

    front_left_horizontal.close()
    front_left_vertical.close()

    mid_right_horizontal.close()
    mid_right_vertical.close()       

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
