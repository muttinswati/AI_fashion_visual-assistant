
category_map = {
    "Topwear": ["Tshirts", "Shirts", "Tops", "Kurtas", "Tunics", "Blazers"],
    "Bottomwear": ["Jeans", "Trousers", "Casual Pants", "Shorts", "Skirts", "Leggings", "Salwars"],
    "Footwear": ["Casual Shoes", "Heels", "Flats", "Sports Shoes", "Formal Shoes", "Sandals", "Flip Flops"],
    "Bags": ["Handbags", "Backpacks", "Clutches", "Messenger Bags", "Duffel Bag"],
    "Accessories": ["Watches", "Belts", "Sunglasses", "Jewellery", "Wallets"]
}

valid_usages = ["Casual", "Formal", "Party", "Sports", "Ethnic", "Smart Casual"]

NEUTRALS = ["black", "white", "grey", "navy", "beige", "off white", "charcoal"]


BLACKLIST_CATEGORIES = [
    "Innerwear", "Briefs", "Trunks", "Vests", "Bras", 
    "Socks", "Nightwear", "Boxers", "Panties"
]

compatibility = {
    "Topwear": ["Bottomwear", "Footwear", "Bags", "Accessories"],
    "Bottomwear": ["Topwear", "Footwear", "Accessories"],
    "Footwear": ["Bottomwear", "Topwear", "Accessories", "Bags"], # Added this!
    "Accessories": ["Topwear", "Bottomwear", "Footwear"]
}