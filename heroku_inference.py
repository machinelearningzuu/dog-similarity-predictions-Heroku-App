import os
import pickle
import pathlib
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import logging
logging.getLogger('tensorflow').disabled = True
import numpy as np
from tensorflow.keras.models import model_from_json, Sequential, Model, load_model
from tensorflow.keras.layers import Activation, Dense, Input, Flatten, BatchNormalization
from tensorflow.keras import backend as K
from matplotlib import pyplot as plt
from sklearn.neighbors import NearestNeighbors
from util import *
from variables import *

np.random.seed(seed)

physical_devices = tf.config.experimental.list_physical_devices('GPU')
print("\nNum GPUs Available: {}\n".format(len(physical_devices)))
tf.config.experimental.set_memory_growth(physical_devices[0], True)

test_classes, test_images, test_url_strings = load_test_data(test_dir, test_data_path)

interpreter = tf.lite.Interpreter(model_path=model_converter)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def Inference(img):
    input_shape = input_details[0]['shape']
    input_data = np.expand_dims(img, axis=0).astype(np.float32)
    assert np.array_equal(input_shape, input_data.shape), "Input tensor hasn't correct dimension"

    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

def extract_features():
    if not os.path.exists(n_neighbour_weights):
        test_features = np.array(
                        [Inference(img) for img in test_images]
                                    )
        test_features = test_features.reshape(test_features.shape[0],-1)
        neighbor = NearestNeighbors(
                                    n_neighbors = 20,
                                    )
        neighbor.fit(test_features)
        with open(n_neighbour_weights, 'wb') as file:
            pickle.dump(neighbor, file)
    else:
        with open(n_neighbour_weights, 'rb') as file:
            neighbor = pickle.load(file)
    return neighbor

def predict_neighbour(dogimage, img_path, neighbor):
    n_neighbours = {}
    data = Inference(dogimage)
    result = neighbor.kneighbors(data)[1].squeeze()
    result = nearest_neighbour_prediction(result, test_classes)
    for i in range(thres_neighbours):
        neighbour_img_id = result[i]
        label = test_classes[neighbour_img_id]
        print("Neighbour image {} label : {}".format(i+1, int(label)))
        n_neighbours["neighbour {}".format(i+1)] = "{}".format(test_url_strings[neighbour_img_id])
    return n_neighbours
