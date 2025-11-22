import json
import random

def main():
    with open("./db/products.json", "r") as file:
        product = json.load(file).get("data")
    with open("./db/tags.json", "r") as file:
        tags = json.load(file).get("data")
    with open("./db/user.json", "r") as file:
        data = json.load(file).get("data")
    if(not data or not tags or not product):
        raise FileExistsError("Invalid file")
    print(f"len data: {len(data)}")
    for item in data:
        for baby in item.get("baby") or []:
            baby["tags"] = []
            idxs = random.sample(range(20), 3)
            for idx in idxs:
                baby["tags"].append(tags[idx])
        for cloth in item.get("clothes") or []:
            cloth["tags"] = []
            idxs = random.sample(range(9), 3)
            for idx in idxs:
                cloth["tags"].append(product[idx])
    
    with open("./db/new.json", "w") as file:
        json.dump({"data": data}, file, ensure_ascii=False, indent=2)
    

    return

if __name__ == "__main__":
    main()