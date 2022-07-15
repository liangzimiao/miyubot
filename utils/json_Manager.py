import json

data_dir = "./data/CD/"

def readJson(name:str):
    try:
        with open(data_dir + f"{name}usercd.json", "r") as f_in:
            data = json.load(f_in)
            f_in.close()
            return data
    except FileNotFoundError:
        try:
            import os
            os.makedirs(data_dir)
        except FileExistsError:
            pass
        with open(data_dir + f"{name}usercd.json", mode="w") as f_out:
            json.dump({}, f_out)


def writeJson(qid: str, time: int, mid: int, data: dict, name:str):
    try:
        data[qid] = [time, mid]
    except:    
        data = {}
        with open(data_dir + f"{name}usercd.json", "w") as f_out:
            json.dump(data, f_out)
        f_out.close()
        data[qid] = [time, mid]
    with open(data_dir + f"{name}usercd.json", "w") as f_out:
        json.dump(data, f_out)
        f_out.close()


def removeJson(qid: str, name:str):
    with open(data_dir + f"{name}usercd.json", "r") as f_in:
        data = json.load(f_in)
        f_in.close()
    data.pop(qid)
    with open(data_dir + f"{name}usercd.json", "w") as f_out:
        json.dump(data, f_out)
        f_out.close()
