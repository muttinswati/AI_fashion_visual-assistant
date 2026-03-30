import os
import torch
from PIL import Image
from torchvision import transforms
from torchvision.models import resnet18, ResNet18_Weights
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as p
import pickle
from numpy import dot
from numpy.linalg import norm


print("FILE IS RUNNING")

IMAGE_FOLDER = "backend/images/"

print("Checking folder:", IMAGE_FOLDER)


preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def preprocess_image(image_path):
    img=Image.open(image_path).convert("RGB")
    img=preprocess(img)
    return img

preprocess_image("backend/images/1163.jpg")


def preprocess_all_images():
    image_tensors = {}
    skipped = 0

    for file in os.listdir(IMAGE_FOLDER):



        print("Processing:", file)   

   
        if file.lower().endswith((".jpg", ".png", ".jpeg")):

            path = os.path.join(IMAGE_FOLDER, file)

            try:
                tensor = preprocess_image(path)
                image_tensors[file] = tensor

            except Exception as e:
                print(f"Skipping {file}: {e}")
                skipped += 1

    print(f"✅ Processed: {len(image_tensors)} images")
    print(f"⚠️ Skipped: {skipped} images")

    return image_tensors



model = resnet18(weights=ResNet18_Weights.DEFAULT)


model = torch.nn.Sequential(*list(model.children())[:-1])


model.eval()



def extract_features(image_tensor):
    
    image_tensor = image_tensor.unsqueeze(0)

    
    with torch.no_grad():
        features = model(image_tensor)

   
    features = features.squeeze().numpy()
    features = features / np.linalg.norm(features)

    return features



def extract_all_features(image_tensors):
    feature_dict = {}

    for file, tensor in image_tensors.items():
        print("Extracting:", file)

        features = extract_features(tensor)

        feature_dict[file] = features


    return feature_dict


def final_run():
    print("STARTING PREPROCESSING")
    data = preprocess_all_images()

    print("STARTING FEATURE EXTRACTION")
    features = extract_all_features(data)

    print("DONE")


    print(features)

    return features  


    

if __name__ == "__main__":
    def loadembeds():
        USE_SAVED = True  

        if not USE_SAVED:
            r = final_run()

            os.makedirs("backend/temp", exist_ok=True)

            with open("backend/temp/features.pkl", "wb") as f:
                pickle.dump(r, f)

            print("✅ Features saved!")

        else:
            with open("backend/temp/features.pkl", "rb") as f:
                feature_dict = pickle.load(f)

            print("✅ Features loaded!")
            print("Total images:", len(feature_dict))

       
            print(list(feature_dict.keys())[:5])

    loadembeds()