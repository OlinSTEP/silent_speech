import re
import os
import json
import random


def get_session_data(session_path):
    session_data = []
    for file_name in os.listdir(session_path):
        # Only look at _info.json files
        m = re.match(r'(\d+)_info.json', file_name)
        if m is None:
            continue
        # We only care about the specific phrase for purposes of data seperation
        with open(os.path.join(session_path, file_name), 'r') as f:
            file_data = json.load(f)
        data = [file_data["book"], file_data["sentence_index"]]
        # Sentence index of -1 indicates silence
        if data[1] > 0:
            session_data.append(data)
    return sorted(session_data, key=lambda x: x[1])


def main(silent_data_path, output_path, dev_size=0.1, test_size=0.2):
    # We get all test/dev sentences on a single session
    # This means no test phrases will appear in the training data
    session_dir = sorted(os.listdir(silent_data_path))[0]
    session = os.path.join(silent_data_path, session_dir)
    data = get_session_data(session)

    l = len(data)
    dev_len = int(l * dev_size)
    test_len = int(l * test_size)

    random.seed(0)
    random.shuffle(data)
    dev_data = data[:dev_len]
    test_data = data[:test_len]
    json_data = {
        "dev": dev_data,
        "test": test_data,
    }

    print(f"Total Length: {l}");
    print(f"Dev Length: {len(dev_data)}")
    print(f"Train Length: {len(test_data)}")
    
    with open(output_path, 'w') as f:
        json.dump(json_data, f)
        
if __name__ == '__main__':
    main("emg_data/grimm_1/", "testset_grimm.json")
