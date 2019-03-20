## Partial code taken from Object detection tutorial at
## https://github.com/EdjeElectronics/TensorFlow-Object-Detection-on-the-Raspberry-Pi

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

# object_detection folder holds the paths to the tf models as well as the folder for the utils imports.
object_detection_path = '/home/pi/tensorflow1/models/research'
sys.path.append(object_detection_path)

# Import utilites
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

def detect_objects(in_queue):
    # Name of the directory containing the object detection module we're using
    MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'

    # Path to frozen detection graph .pb file, which contains the model that is used
    # for object detection.
    PATH_TO_CKPT = os.path.join(object_detection_path, 'object_detection' ,MODEL_NAME,'frozen_inference_graph.pb')

    # Path to label map file
    PATH_TO_LABELS = os.path.join(object_detection_path,'object_detection', 'data','mscoco_label_map.pbtxt')

    # Number of classes the object detector can identify
    NUM_CLASSES = 90

    ## Load the label map.
    # Label maps map indices to category names, so that when the convolution
    # network predicts `5`, we know that this corresponds to `airplane`.
    # Here we use internal utility functions, but anything that returns a
    # dictionary mapping integers to appropriate string labels would be fine
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # Load the Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    # Define input and output tensors (i.e. data) for the object detection classifier
    # only using classes on output side to save computation, avoiding bounding boxes, masks, etc

    # Input tensor is the image
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

    min_score_thresh = .5
    # Initialize Picamera and grab reference to the raw capture
    camera = PiCamera()
    camera.resolution = (CAM_WIDTH,CAM_HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(CAM_WIDTH,CAM_HEIGHT))
    rawCapture.truncate(0)

    for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
        print("getting frame data")
        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        frame = np.copy(frame1.array)
        frame.setflags(write=1)
        frame_expanded = np.expand_dims(frame, axis=0)

        # Perform the actual detection by running the model with the image as input
        (scores, classes) = sess.run([detection_scores, detection_classes], feed_dict={image_tensor: frame_expanded})
        scores = np.squeeze(scores)
        classes = np.squeeze(classes).astype(np.int32)
        
        for i in range(5):
            if scores is None or scores[i] > min_score_thresh:
                if classes[i] in category_index.keys():
                    class_name = category_index[classes[i]]['name']
                    in_queue.put(str(class_name))

        rawCapture.truncate(0)

    camera.close()

    cv2.destroyAllWindows()
