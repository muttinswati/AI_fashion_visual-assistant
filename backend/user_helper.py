import os
import uuid
from shutil import copyfile
from preexecute import preprocess_image, extract_features
from pipeline import knn, image_files, final_data
from config import category_map
from config import compatibility
from collections import Counter

def get_group_internal(article_type):
    a_type = str(article_type).strip().lower()
    for group, types in category_map.items():
        if a_type in [t.lower() for t in types]:
            return group
    return None

def recommend_outfit_for_user(user_image_path):
    img_tensor = preprocess_image(user_image_path)
    query_vector = extract_features(img_tensor).reshape(1, -1)
    
    _, idx = knn.kneighbors(query_vector, n_neighbors=11)
    
    neighbor_genders = []
    neighbor_types = []
    neighbor_usages = []

    for i in idx[0]:
        info = final_data.get(image_files[i], {})
        neighbor_genders.append(str(info.get("gender", "Men")).strip().capitalize())
        neighbor_types.append(str(info.get("articleType", "")).strip())
        neighbor_usages.append(str(info.get("usage", "Casual")).strip())

    user_gender = Counter(neighbor_genders).most_common(1)[0][0]
    user_type = Counter(neighbor_types).most_common(1)[0][0] 
    user_usage = Counter(neighbor_usages).most_common(1)[0][0]

    top_info = final_data.get(image_files[idx[0][0]], {})
    user_color = str(top_info.get("baseColour", "")).lower().strip()

    user_group = None
    clean_user_type = user_type.lower().replace(" ", "").replace("-", "")
    for group, types in category_map.items():
        clean_types = [t.lower().replace(" ", "").replace("-", "") for t in types]
        if clean_user_type in clean_types:
            user_group = group
            break

    print(f"👑 FINAL VERDICT -> Gender: {user_gender} | Type: {user_type} | Group: {user_group} | Usage: {user_usage}")
    
    target_groups = compatibility.get(user_group, ["Topwear", "Bottomwear", "Footwear", "Bags", "Accessories"])
    target_groups = [g for g in target_groups if g != user_group]
    outfit_buckets = {group: None for group in target_groups}
    
    blacklist = ["Briefs", "Bra", "Innerwear", "Socks", "Vests", "Nightdress", "Nightwear", "Boxers", "Camisoles"]
    _, all_indices = knn.kneighbors(query_vector, n_neighbors=len(image_files))

    for i in all_indices[0]:
        cand_id = image_files[i]
        info = final_data.get(cand_id, {})
        
        cand_gender = str(info.get("gender", "")).strip().capitalize()
        cand_type = str(info.get("articleType", "")).strip()
        cand_usage = str(info.get("usage", "")).strip()

        is_wrong_gender = (
            (user_gender == "Men" and cand_gender == "Women") or 
            (user_gender == "Women" and cand_gender == "Men")
        )
        if is_wrong_gender:
            continue
        
        if cand_type in blacklist or cand_type == user_type:
            continue

        clean_cand_type = cand_type.lower().replace(" ", "").replace("-", "")
        cand_group = None
        for g, types in category_map.items():
            clean_types = [t.lower().replace(" ", "").replace("-", "") for t in types]
            if clean_cand_type in clean_types:
                cand_group = g
                break

        if cand_group in outfit_buckets and outfit_buckets[cand_group] is None:
            if cand_usage == user_usage:
                outfit_buckets[cand_group] = cand_id

        if all(v is not None for v in outfit_buckets.values()):
            break

    for group in outfit_buckets:
        if outfit_buckets[group] is None:
            for i in all_indices[0]:
                cand_id = image_files[i]
                info = final_data.get(cand_id, {})
                c_gen = str(info.get("gender", "")).strip().capitalize()
                c_type = str(info.get("articleType", "")).strip()
                c_usage = str(info.get("usage", "")).strip()
                
                if (user_gender == "Men" and c_gen == "Women") or (user_gender == "Women" and c_gen == "Men"): 
                    continue
                
                clean_c_type = c_type.lower().replace(" ", "").replace("-", "")
                c_grp = None
                for g, types in category_map.items():
                    clean_types = [t.lower().replace(" ", "").replace("-", "") for t in types]
                    if clean_c_type in clean_types:
                        c_grp = g
                        break

                if c_grp == group and c_usage == user_usage and c_type not in blacklist:
                    outfit_buckets[group] = cand_id
                    break

    return [img for img in outfit_buckets.values() if img is not None]

def recommend_outfit_for_user(user_image_path):
    img_tensor = preprocess_image(user_image_path)
    query_vector = extract_features(img_tensor).reshape(1, -1)
    
    _, idx = knn.kneighbors(query_vector, n_neighbors=11)
    neighbor_genders = [str(final_data.get(image_files[i], {}).get("gender", "Men")).strip() for i in idx[0]]
    user_gender = Counter(neighbor_genders).most_common(1)[0][0]
    
    top_info = final_data.get(image_files[idx[0][0]], {})
    user_type = str(top_info.get("articleType", "")).strip()
    user_usage = str(top_info.get("usage", "Casual")).strip()
    user_color = str(top_info.get("baseColour", "")).lower().strip()

    user_group = None
    clean_user_type = user_type.lower().replace(" ", "").replace("-", "")
    for group, types in category_map.items():
        if clean_user_type in [t.lower().replace(" ", "").replace("-", "") for t in types]:
            user_group = group
            break

    print(f"🕵️ AI VERDICT -> Gender: {user_gender} | Type: {user_type} | Usage: {user_usage}")

    target_groups = compatibility.get(user_group, ["Topwear", "Bottomwear", "Footwear", "Bags", "Accessories"])
    target_groups = [g for g in target_groups if g != user_group]
    outfit_buckets = {group: None for group in target_groups}
    
    blacklist = ["Briefs", "Bra", "Innerwear", "Socks", "Vests", "Nightdress", "Nightwear", "Boxers"]
    _, all_indices = knn.kneighbors(query_vector, n_neighbors=len(image_files))

    for i in all_indices[0]:
        cand_id = image_files[i]
        info = final_data.get(cand_id, {})
        
        cand_gender = str(info.get("gender", "")).strip().capitalize()
        cand_type = str(info.get("articleType", "")).strip()
        cand_usage = str(info.get("usage", "")).strip()

        if user_gender == "Men" and cand_gender == "Women":
            continue
        if user_gender == "Women" and cand_gender == "Men":
            continue
        
        if cand_type in blacklist or cand_type == user_type:
            continue

        clean_cand_type = cand_type.lower().replace(" ", "").replace("-", "")
        cand_group = None
        for g, types in category_map.items():
            if clean_cand_type in [t.lower().replace(" ", "").replace("-", "") for t in types]:
                cand_group = g
                break

        if cand_group in outfit_buckets and outfit_buckets[cand_group] is None:
            if cand_usage == user_usage:
                outfit_buckets[cand_group] = cand_id

        if all(v is not None for v in outfit_buckets.values()):
            break

    for group in outfit_buckets:
        if outfit_buckets[group] is None:
            for i in all_indices[0]:
                cand_id = image_files[i]
                info = final_data.get(cand_id, {})
                c_gen = str(info.get("gender", "")).strip().capitalize()
                c_type = str(info.get("articleType", "")).strip()
                c_usage = str(info.get("usage", "")).strip()
                
                if user_gender == "Men" and c_gen == "Women": continue
                if user_gender == "Women" and c_gen == "Men": continue
                
                clean_c_type = c_type.lower().replace(" ", "").replace("-", "")
                c_grp = None
                for g, types in category_map.items():
                    if clean_c_type in [t.lower().replace(" ", "").replace("-", "") for t in types]:
                        c_grp = g
                        break

                if c_grp == group and c_usage == user_usage and c_type not in blacklist:
                    outfit_buckets[group] = cand_id
                    break

    return [img for img in outfit_buckets.values() if img is not None]

def handle_user_request(image_path):
    UPLOAD_BASE = "temp/user_uploads"
    os.makedirs(UPLOAD_BASE, exist_ok=True)
    session_id = str(uuid.uuid4())
    session_folder = os.path.join(UPLOAD_BASE, session_id)
    os.makedirs(session_folder, exist_ok=True)
    
    dest_path = os.path.join(session_folder, os.path.basename(image_path))
    copyfile(image_path, dest_path)

    recs = recommend_outfit_for_user(dest_path)
    return {
        "session_id": session_id,
        "uploaded_image": os.path.basename(dest_path),
        "recommendations": recs
    }