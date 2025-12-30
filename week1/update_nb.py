import json
import os

file_path = "/Users/dante/workspace/dante-code/class/statrack2_python/week1/Day1_1_데이터_구조_심화_Collection.ipynb"

with open(file_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

new_source = [
    "# 1. 공백 제거 (String Stripping)\n",
    "# 실무에서 데이터를 다룰 때 가장 먼저 하는 필수 작업 중 하나가 바로 \"공백 제거\"입니다.\n",
    "# 사용자가 실수로 입력한 앞뒤 공백이나, 시스템 로그에서 발생하는 불필요한 빈칸을 깔끔하게 지워줍니다.\n",
    "\n",
    "# 여기 아주 지저분한 원본 데이터가 있습니다. 앞뒤로 공백(스페이스)이 가득하네요!\n",
    "raw_data = \"  [ERROR] Connection Timeout   \"\n",
    "\n",
    "# f-string을 사용해서 원본 데이터를 따옴표('') 안에 넣어 출력해볼게요. 공백이 어느 정도인지 확인해 보세요.\n",
    "print(f\"원본: \'{raw_data}\'\")\n",
    "\n",
    "# [1] strip(): 양쪽(왼쪽 + 오른쪽)의 모든 공백을 한 번에 싹~ 지워줍니다. 가장 대중적으로 많이 쓰여요!\n",
    "print(f\"strip(): \'{raw_data.strip()}\'\")\n",
    "\n",
    "# [2] lstrip(): 왼쪽(Left)에 있는 공백만 골라서 지워줍니다. 오른쪽 공백은 건드리지 않고 그대로 둡니다.\n",
    "print(f\"lstrip(): \'{raw_data.lstrip()}\'\")\n",
    "\n",
    "# [3] rstrip(): 오른쪽(Right)에 있는 공백만 골라서 지워줍니다. 왼쪽 공백은 그대로 남겨둡니다.\n",
    "print(f\"rstrip(): \'{raw_data.rstrip()}\'\")\n",
    "\n",
    "# 💡 꿀팁: strip()은 눈에 보이는 공백뿐만 아니라 엔터키(\\n)나 탭키(\\t)로 생긴 빈칸도 똑똑하게 다 지워준답니다!"
]

# Ensure each line ends with \n except maybe the last one if we want, but standard is to have \n in source list
new_source = [line if line.endswith("\n") else line + "\n" for line in new_source]
# Actually, the last element in source often doesnt have \n if it is the end of the list, but let s match common practice.
if new_source[-1].endswith("\n"):
    new_source[-1] = new_source[-1][:-1]

found = False
for cell in nb["cells"]:
    if cell["cell_type"] == "code" and any("# 1. 공백 제거" in line for line in cell["source"]):
        cell["source"] = new_source
        found = True
        break

if found:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print("Successfully updated the notebook cell.")
else:
    print("Target cell not found.")
