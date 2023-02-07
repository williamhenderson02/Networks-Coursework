import sys
import os

filename = "file.txt"

print(filename)
if os.path.isfile(filename):
    print('yes')
else:
    print("no")