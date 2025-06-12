import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("1.png")

plt.imshow(img)

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()