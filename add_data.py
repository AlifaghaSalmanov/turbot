import json

from database.filter_managers import MakeManager, ModelManager, RegionManager

with open("data/regions.json", "r") as file:
    region_data = json.load(file)

with open("data/makes.json", "r") as file:
    make_data = json.load(file)

with open("data/models.json", "r") as file:
    model_data = json.load(file)


for region_name in region_data.get("region_names"):
    RegionManager().get_or_create(region_name)

for make_name in make_data.get("make_names"):
    MakeManager().get_or_create(make_name)

for model_data in model_data.get("model_names"):
    make_name = model_data["make_name"]
    models = model_data["models"]

    try:
        print(f"Creating models for {make_name}")
        make = MakeManager().get_or_create(make_name)
        for model in models:
            ModelManager().get_or_create(make.id, make_name, model)
    except Exception as e:
        print(e)
        print(f"Error creating models for {make_name}")
        continue
