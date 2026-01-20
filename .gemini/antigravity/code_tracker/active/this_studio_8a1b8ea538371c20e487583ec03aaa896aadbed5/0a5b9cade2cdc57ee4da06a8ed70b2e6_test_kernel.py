øimport sys
import os

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
try:
    import ipykernel
    print(f"ipykernel version: {ipykernel.__version__}")
except ImportError:
    print("ipykernel not installed")
ø"(8a1b8ea538371c20e487583ec03aaa896aadbed524file:///teamspace/studios/this_studio/test_kernel.py:%file:///teamspace/studios/this_studio