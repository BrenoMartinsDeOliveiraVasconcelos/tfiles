import json
import os
import helpers

ENVIROMENT = os.environ
CONFIG = helpers.CONFIG_FILE
CONFIG_INITIALIZED = CONFIG["initialized"]
TRANSLATION_FOLDER = helpers.TRANSLATION_FOLDER
HELP_FOLDER = helpers.HELP_FOLDER

DEFAULT_LANG = "en-us"

def set_language() -> bool:
    lang = CONFIG["language"]
    restart = False
    if "LANG" in ENVIROMENT.keys() and not CONFIG_INITIALIZED:
        lang = ENVIROMENT["LANG"].split(".")[0].lower().replace("_", "-")
        
        # Procurar nos arquivos de tradução se existe, se não default
        found = False
        for _, _, files in os.walk(TRANSLATION_FOLDER):
            for file in files:
                if file.startswith(lang):
                    found = True
                    
        if not found:
            lang = DEFAULT_LANG
            
        restart = True
    else:
        lang = DEFAULT_LANG if not CONFIG_INITIALIZED else lang
        
    CONFIG["language"] = lang
    CONFIG["initialized"] = True
    
    json.dump(CONFIG, open('config.json', 'w'), indent=4)   
    
    return restart


def restore_config() -> bool:
    restart = False
    bak = 'config.json.bak'
    if os.path.exists(bak):
        saved_data = json.load(open(bak))
        
        relevant_keys = ["language", "initialized"]
        for key in relevant_keys:
            if key in saved_data.keys():
                CONFIG[key] = saved_data[key]
        
        restart = True

        json.dump(CONFIG, open('config.json', 'w'), indent=4)
        os.remove(bak)
        
    return restart


        