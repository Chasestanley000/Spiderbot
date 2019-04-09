## Partial code taken from Object detection tutorial at
## https://github.com/EdjeElectronics/TensorFlow-Object-Detection-on-the-Raspberry-Pi
## courtesy of Evan Juras, P.E.


# Import packages
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import sys

# Set up camera constants
CAM_WIDTH = 640
CAM_HEIGHT = 480

# Various paths to folders/data files/constants needed to run object detection
# OBJECT_DETECTION - top level folder holding utils package and pretrained models
# MODEL_NAME - name of the pretrained model being used
# PATH_TO_CKPT - path to a the pretrained model that has been frozen to preserve weights
# PATH_TO_LABELS - path to a dictionary style file holding the labels/values of objects the model can detect
# NUM_CLASSES - Number of classes the object detector can identify
# MIN_SCORE - The minimum value that will determine whether TensorFlow "sees" an object or not, 0.5 = 50% 
OBJECT_DETECTION = '/home/pi/tensorflow1/models/research'
MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'
PATH_TO_CKPT = os.path.join(OBJECT_DETECTION, 'object_detection', MODEL_NAME,'frozen_inference_graph.pb')
PATH_TO_LABELS = os.path.join(OBJECT_DETECTION, 'object_detection', 'data','mscoco_label_map.pbtxt')
NUM_CLASSES = 90
MIN_SCORE = .5


# OBJECT_DETECTION must be appended to the system path so Python can import the
# 'utils' package that is within it
sys.path.append(OBJECT_DETECTION)

# Import utilites
from object_detection.utils import label_map_util


def detect_objects(in_queue, out_queue, spiderbot_logger):
    """
        detect_objects() uses TensorFlow and OpenCV to determine
        what is seen in a frame from the PiCamera and will place 
        the string representation of the object in a Queue to be
        picked up by the main thread.
    """
    spiderbot_logger.info("Starting detect_objects() function...")

    # Use TensorFlow utilities to map the dict file holding the labels to
    # a python style dictionary that can be used to create human readable
    # output for detected objects
    spiderbot_logger.info("mapping labels to dictionary")
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # Create a TensorFlow graph to load in the frozen model and
    # make a TensorFlow session based on it
    spiderbot_logger.info("Creating detection graph for TensorFlow")
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    # Create objects to hold the tensors taken from the frozen model graph.
    # These will be passed to TensorFlow to determine what it is looking
    # for and what it returns.
    spiderbot_logger.info("Creating object tensors for TensorFlow")
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')


    # Initialize Picamera with a custom resolution and a max framerate of 10
    spiderbot_logger.info("Initialize PiCamera")
    camera = PiCamera()
    camera.resolution = (CAM_WIDTH,CAM_HEIGHT)
    camera.framerate = 10
    
    # Create an object reference to the raw RGB values from the PiCamera
    spiderbot_logger.info("Initialize RGB array for PiCamera")
    rawCapture = PiRGBArray(camera, size=(CAM_WIDTH,CAM_HEIGHT))
    rawCapture.truncate(0)

    # Create an infinite loop that will continuously take frames from the PiCamera
    spiderbot_logger.info("Begin frame capture and object detection")
    out_queue.put('ready')
    for frame1 in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        try:
            flag = in_queue.get(block=False)
        except:
            flag = None

        if flag is not None:
            break
            
        spiderbot_logger.info("get new frame and pass to TF")
        # Capture the frame as a numpy array containing the RGB values and use np.expand_dims
        # to place another axis in the 0th spot of the array
        frame = np.copy(frame1.array)
        frame.setflags(write=1)
        frame_expanded = np.expand_dims(frame, axis=0)

        # Run a TF session to check the current frame and output both the scores and classes arrays
        spiderbot_logger.info("Run frame through TF model")
        (scores, classes) = sess.run([detection_scores, detection_classes], feed_dict={image_tensor: frame_expanded})
        # np.squeeze will remove all the "1" values from the scores and 
        # classes arrays as those values can essentially be treated as NULLs
        scores = np.squeeze(scores)
        classes = np.squeeze(classes).astype(np.int32)
        
        # Create a loop to check for the first 5 classes that were detected by TF
        spiderbot_logger.info("Check results from TF and pass to Queue")
        for i in range(5):
            # If the score returned is greater than the minimum then get the
            # class name for that index and place it in a Queue to be sent to the
            # main thread
            if scores is None or scores[i] > MIN_SCORE:
                if classes[i] in category_index.keys():
                    class_name = category_index[classes[i]]['name']
                    out_queue.put(str(class_name))

        # reset capture back to 0 to get a fresh frame
        rawCapture.truncate(0)

    camera.close()
