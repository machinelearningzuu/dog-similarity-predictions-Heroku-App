import os
target_size = (224, 224)
thres_neighbours = 5
seed = 1234
host = '0.0.0.0'
port = 5000
found_table = 'found_dog'
lost_table = 'lost_dog'
found_table = 'foundImages'
root_password = '1234'
db_url = 'mysql+pymysql://root:{}@localhost:3306/doggy_similarity'.format(root_password)
local_url = 'http://0.0.0.0:5000/predict'

# data directories and model paths
found_img_dir = os.path.join(os.getcwd(),'data/Found Dogs')
lost_img_dir = os.path.join(os.getcwd(),'data/Lost Dogs')
test_dir = os.path.join(os.getcwd(), 'data/Test images/')
test_data_path = 'data/weights/Test_data.npz'
model_converter = "data/weights/model.tflite"
n_neighbour_weights = 'data/weights/nearest_neighbour.pkl'