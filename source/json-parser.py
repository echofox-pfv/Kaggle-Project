import json
import requests
import numpy as np
from scipy import misc
from io import BytesIO
from PIL import Image

# Load JSON File
with open('Dataset/train.json') as data_file:
    data = json.load(data_file);

images = data["images"]	# list
annotations = data["annotations"] # list

dataset_counter = 0;	# dataset counter
label = {};	# data per label
accepted_label = [];	# labels with dataset size > 2300
accepted_id = [];

# Initialize classes dictionary
# Output: {<label_id> : 0}
for i in range(129):
	if(not(i == 0)):
		label[str(i)] = 0

# Iterate over list annotations
# Output: {<label_id>: count of image per label}
for i in annotations:
	label[str(i["label_id"])] = label[str(i["label_id"])] + 1

# Print count of images per label (greater than 2000)
# Output: accepted_label = [1,2,...,128]
for label_id, value in sorted(label.iteritems()):
	if(value > 2000): #2500
		dataset_counter = dataset_counter + value;
		print(label_id +" : "+ str(value));
		accepted_label.append(int(label_id));

print("Total size of trimmed dataset: " + str(dataset_counter));

for i in annotations:
	if(i["label_id"] in accepted_label):
		accepted_id.append(i["image_id"]);

print("Accepted id list: " +str(len(accepted_id)));

# Create new dataset list for accepted labels
# Output
# url_list = [url 1, url 2, ..., url n]
# label_list = [class 1, class 2, ..., class n]
# img_array_list = [array 1, array 2, ..., array n]

url_list = []
img_array_list = []
label_list = []

accepted_id.sort()

for ids in accepted_id:
	url = images[ids-1]["url"][0]
	url_list.append(url)
	label_list.append(annotations[ids-1]["label_id"])

	try:
		res = requests.get(url)
		if res.status_code == 200:
			img_arr = np.array(Image.open(BytesIO(res.content)))
			img_array_list.append(img_arr)
	except requests.exceptions.RequestException as e:
		print("MISSING: " + url)

# Random Sampling
for i in range(80):
	#print(url_list[i*700])
	print(img_array_list[i*700])
	#print(label_list[i*700])
