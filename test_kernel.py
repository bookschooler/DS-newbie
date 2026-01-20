import sys
import os

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
try:
    import ipykernel
    print(f"ipykernel version: {ipykernel.__version__}")
except ImportError:
    print("ipykernel not installed")
