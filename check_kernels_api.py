
import requests
import json
import os

# Try to find the token and port from the runtime files
runtime_dir = "/teamspace/studios/this_studio/.local/share/jupyter/runtime"
for f in os.listdir(runtime_dir):
    if f.startswith("jpserver-") and f.endswith(".json"):
        with open(os.path.join(runtime_dir, f)) as jf:
            data = json.load(jf)
            port = data['port']
            token = data.get('token', '')
            base_url = data.get('base_url', '')
            print(f"Connecting to {port} with token {token}")
            
            url = f"http://127.0.0.1:{port}{base_url}api/kernelspecs"
            headers = {"Authorization": f"token {token}"}
            try:
                resp = requests.get(url, headers=headers)
                print(json.dumps(resp.json(), indent=2))
            except Exception as e:
                print(f"Error: {e}")
