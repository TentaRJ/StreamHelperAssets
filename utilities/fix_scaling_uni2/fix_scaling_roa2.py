from PIL import Image
from glob import glob
import json
import os.path

# file_list = glob("../../games/roa2/base_files/icon/*.png", recursive=True)
with open("../../games/roa2/base_files/icon/config.json", "rt", encoding="utf-8") as config_file:
    icon_config = json.loads(config_file.read())
with open("../../games/roa2/base_files/config.json", "rt", encoding="utf-8") as config_file:
    main_config = json.loads(config_file.read())

rescaling_factor = {}
for character_name in main_config["character_to_codename"].keys():
    codename = main_config["character_to_codename"][character_name]["codename"]
    image_filename = f"../../games/roa2/base_files/icon/{icon_config['prefix']}{codename}{icon_config['postfix']}0.png"
    if os.path.isfile(image_filename):
        image = Image.open(image_filename, "r").convert("RGBA")
        height = image.height
        rescaling_factor[codename] = {"0": 256.0/height}
        print(codename, rescaling_factor[codename]["0"])
    else:
        print(f"Could not find {image_filename}")
icon_config["rescaling_factor"] = rescaling_factor
with open("../../games/roa2/base_files/icon/config.json", "wt", encoding="utf-8") as config_file:
    config_file.write(json.dumps(icon_config, indent=2))
