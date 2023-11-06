import os
import faiss
import numpy as np
from PIL import Image
import torch
from torchvision import transforms, models
from tqdm import tqdm

# Load pre-trained model
# Assuming you have a pre-trained model that outputs 128-dimensional embeddings
# model = YourPretrainedModel()
# Load pre-trained ResNet-50 model
model = models.resnet50(pretrained=True)
model.eval()  # Set the model to evaluation mode

# Remove the classification layer (final fully connected layer)
model = torch.nn.Sequential(*list(model.children())[:-1])
# Define a function to extract embeddings from images
def extract_embedding(image_path, model):
    image = Image.open(image_path).convert("RGB")
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_image = preprocess(image).unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        embedding = model(input_image)  # Assuming model returns a 128-dimensional embedding
    return embedding.numpy()

# Directory containing images
image_folder = "data/train/1"

# Get a list of image files in the folder
image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith('.jpg')]

# Extract embeddings for images in the folder
embeddings = []
for image_file in tqdm(image_files, desc="Extracting Embeddings"):
    embedding = extract_embedding(image_file, model)
    embeddings.append(embedding.flatten())

# Directory containing images
image_folder = "data/train/2"

# Get a list of image files in the folder
image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith('.jpg')]

# Extract embeddings for images in the folder
# embeddings = []
for image_file in tqdm(image_files, desc="Extracting Embeddings"):
    embedding = extract_embedding(image_file, model)
    embeddings.append(embedding.flatten())

# Directory containing images
image_folder = "data/train/3"

# Get a list of image files in the folder
image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith('.jpg')]

# Extract embeddings for images in the folder
# embeddings = []
for image_file in tqdm(image_files, desc="Extracting Embeddings"):
    embedding = extract_embedding(image_file, model)
    embeddings.append(embedding.flatten())

# Convert the list of embeddings to a numpy array
embeddings = np.array(embeddings).astype('float32')

# Build the FAISS index
d = 2048  # Dimension of the embeddings
index_cpu = faiss.IndexFlatL2(d)  # L2 distance metric
index_cpu.add(embeddings)

# Example query image path
query_image_path = "data/train/2/image_05087.jpg"

# Extract embedding for the query image
query_embedding = extract_embedding(query_image_path, model).flatten()

# Perform a similarity search using the FAISS index
k = 5  # Number of nearest neighbors to search for
query_embedding = np.array([query_embedding.astype('float32')])
_, I = index_cpu.search(query_embedding, k)
print("Indices of nearest neighbors:", I)

gpu_index = faiss.index_cpu_to_all_gpus(  # build the index
    index_cpu
)
gpu_index.add(embeddings)
_, I = gpu_index.search(query_embedding, k)

# Print the indices of the nearest neighbors
print("Indices of nearest neighbors:", I)
