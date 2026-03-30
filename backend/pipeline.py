import pickle
import numpy as np
from sklearn.neighbors import NearestNeighbors

try:
    from config import category_map, compatibility
except ImportError:
    from config import category_map, compatibility

print("🚀 Loading search engine...")

with open("backend/temp/final_data.pkl", "rb") as f:
    final_data = pickle.load(f)

image_files = list(final_data.keys())
features = np.array([final_data[file]["features"] for file in image_files])

knn = NearestNeighbors(n_neighbors=100, metric='euclidean')
knn.fit(features)
print(f"✅ KNN Engine ready with {len(image_files)} items")

def get_group(article_type):
    for group, items in category_map.items():
        if article_type in items:
            return group
    return None

def find_similar(image_file, k=5):
    query_vector = final_data[image_file]["features"].reshape(1, -1)
    distances, indices = knn.kneighbors(query_vector, n_neighbors=k+1)
    return [image_files[i] for i in indices[0][1:]]

def recommend_outfit(image_file, k=5):
    item_info = final_data[image_file]
    current_art_type = item_info["articleType"]
    current_gender = item_info["gender"]
    
    current_group = get_group(current_art_type)
    
    allowed_groups = compatibility.get(current_group, [])
    
    allowed_article_types = []
    for group in allowed_groups:
        allowed_article_types.extend(category_map.get(group, []))

    query_vector = item_info["features"].reshape(1, -1)
    distances, indices = knn.kneighbors(query_vector, n_neighbors=100)

    outfit_results = []
    for idx in indices[0]:
        cand_file = image_files[idx]
        cand_info = final_data[cand_file]
        
        if (cand_info["articleType"] in allowed_article_types and 
            cand_info["gender"] == current_gender):
            outfit_results.append(cand_file)
            
        if len(outfit_results) >= k:
            break
            
    return outfit_results

if __name__ == "__main__":
    test_img = image_files[0]
    print(f"👕 Input Item: {test_img} ({final_data[test_img]['articleType']})")
    print("🔍 Similar Items:", find_similar(test_img))
    print("✨ Recommended Outfit:", recommend_outfit(test_img))