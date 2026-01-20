
import json
import os

path = "/teamspace/studios/this_studio/sophie/week1/Day2_2_파일_IO와_직렬화.ipynb"
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Restore to default python3
    nb['metadata']['kernelspec'] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    }

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print("Restored notebook metadata to default 'python3'")
