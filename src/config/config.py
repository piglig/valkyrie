import json

def get_path(relative_path):
    try:
        base_path = sys._MEIPASS # pyinstaller打包后的路径
    except AttributeError:
        base_path = os.path.abspath(".") # 当前工作目录的路径
 
    return os.path.normpath(os.path.join(base_path, relative_path)) # 返回实际路径

def load_config(config_path="config.json"):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config
    except Exception as e:
        return e