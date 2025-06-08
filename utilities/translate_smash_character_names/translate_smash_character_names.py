import requests
import json
from copy import deepcopy

list_games_to_translate = ["ssbu", "ssb64", "ssbm", "ssbwiiu", "pplus", "sms", "msc", "msbl", "mkwii", "mk64", "msb", "mta", "mkwld"]
exclude_locale = ["en_US"]
convert_locale = {"SC": "zh_CN", "TC": "zh_TW", "fr_FR": "fr",
                  "de_DE": "de", "it_IT": "it", "nl_NL": "nl", "ru_RU": "ru", "ko_KR": "ko", "ja_JP": "ja", "es_ES": "es"}

fighter_database_url = "https://www.smashbros.com/assets_v2/data/fighter.json"
fighter_database_request = requests.get(fighter_database_url)
fighter_database_text = fighter_database_request.text
fighter_database = json.loads(fighter_database_text)

for game in list_games_to_translate:
    print(game)
    config_file_path = f"../../games/{game}/base_files/config.json"
    with open(config_file_path, 'rt', encoding="utf-8") as config_file:
        txt_contents = config_file.read()
        config_file_json = json.loads(txt_contents)
    config_character_dict = deepcopy(config_file_json["character_to_codename"])
    for character in config_character_dict.keys():
        for data in fighter_database["fighters"]:
            if data["displayName"]["en_US"].upper().replace("<BR>", "") == character.upper():
                if not config_character_dict[character].get("locale"):
                    config_character_dict[character]["locale"] = {}
                for locale in data["displayName"].keys():
                    if locale not in exclude_locale:
                        actual_locale = locale
                        if convert_locale.get(locale):
                            actual_locale = convert_locale.get(locale)
                        if actual_locale not in config_character_dict[character]["locale"].keys():
                            config_character_dict[character]["locale"][actual_locale] = data["displayName"][locale].replace("<br>", "").title()
                break
    config_file_json["character_to_codename"] = config_character_dict
    with open(config_file_path, 'wt', encoding="utf-8") as config_file:
        txt_contents = json.dumps(config_file_json, indent=2)
        config_file.write(txt_contents)
