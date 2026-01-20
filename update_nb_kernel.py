
import json

path = "/teamspace/studios/this_studio/sophie/week1/Day2_2_파일_IO와_직렬화.ipynb"
with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

nb['metadata']['kernelspec'] = {
    "display_name": "Studio Local Kernel (Venv)",
    "language": "python",
    "name": "studio_local_kernel"
}

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("Updated notebook metadata to use 'studio_local_kernel'")
