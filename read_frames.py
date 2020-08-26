import os
import cv2
current_path = os.getcwd()
folder = os.path.join(current_path, 'data/WalkByShop1cor.mpg')

try:
    # loop us implemented to read the images one by one from the loop.
    # listdir return a list containing the names of the entries
    # in the directory.
    count=0
    for filename in os.listdir(folder):
        img = cv2.imread((os.path.join(folder, filename)))
        print("Success")
        count+=1

    print(count)


except Exception:
        print("Caught this error:")
        print("any text file appears")