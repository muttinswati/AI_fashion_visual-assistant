import pickle
import pandas as pd

usefile=False

if not usefile:
    print("STARTING LABELING FILE")

# ✅ STEP 1: LOAD FEATURES (from previous file)
    with open("backend/temp/features.pkl", "rb") as f:
        feature_dict = pickle.load(f)

    print("✅ Features loaded:", len(feature_dict))



# ✅ STEP 2: LOAD CSV
    df = pd.read_csv( "data/styles.csv",
    sep=",",
    quotechar='"',        # ✅ handles commas inside text
    on_bad_lines="skip",
    engine="python")


    print(df.columns)
    print("✅ CSV loaded:", len(df))


    
# ✅ STEP 3: FIX ID TYPE
    df["id"] = df["id"].astype(str)

    print("Normalization")

    def normalize_gender(g):
        if g == "Men":
            return "Men"
        elif g == "Women":
            return "Women"
        elif g == "Unisex":
            return "Unisex"
        else:
            return None   # ❌ mark invalid

    df["gender"] = df["gender"].apply(normalize_gender)

    df = df[df["gender"].notnull()]

# ✅ STEP 4: MERGE FEATURES + CSV
    final_data = {}
    missing = 0

    for file, vector in feature_dict.items():

        img_id = file.split(".")[0]

        row = df[df["id"] == img_id]

        if not row.empty:
            final_data[file] = {
            "features": vector,
            "gender": row.iloc[0]["gender"], 
            "masterCategory": row.iloc[0]["masterCategory"],
            "subCategory": row.iloc[0]["subCategory"],
            "articleType": row.iloc[0]["articleType"],
            "color": row.iloc[0]["baseColour"],
            "usage": row.iloc[0]["usage"],
            "name": row.iloc[0]["productDisplayName"]
        }
        else:
            missing += 1


# ✅ STEP 5: RESULTS
    print("✅ Mapped:", len(final_data))
    print("⚠️ Missing:", missing)


#  STEP 6: SAVE FINAL FILE
    with open("backend/temp/final_data.pkl", "wb") as f:
        pickle.dump(final_data, f)

    print("🎉 FINAL DATA SAVED")


else:
    print("file loaded failed!!!")

category_map = {
    "Topwear": ["Shirts", "Tshirts"],
    "Bottomwear": ["Jeans", "Trousers","Skirts"],
    "Footwear": ["Shoes","Sandals","Flasts","Flip Flops"],
    "Accessories": ["Watches", "Bags","Belts"]
}


compatibility = {
    "Topwear": ["Bottomwear", "Footwear","Accessories"],
    "Bottomwear": ["Topwear", "Footwear","Accessories"],
    "Footwear": ["Topwear", "Bottomwear","Accessories"],
    "Accessories":["Topwear", "Bottomwear","Footwear"],
}
