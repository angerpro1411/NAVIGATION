import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms


image = cv2.imread("35.png")

# Image dimensions
h, w = image.shape[:2]
cx, cy = w / 2, h / 2  # center coordinates

fig, ax = plt.subplots()

# Step 1: Translate origin to center
# Step 2: Flip Y axis to make positive Y go upward
transform = transforms.Affine2D().translate(-cx, -cy).scale(1, -1)

# Show the image with custom transform
ax.imshow(image, transform=transform + ax.transData, origin='upper')

# Adjust limits to match the new coordinate system
ax.set_xlim(-cx, cx)
ax.set_ylim(-cy, cy)  # Now positive Y is upward

# Add labels and grid
ax.set_title('Coordinate with Origin at Center')
ax.set_xlabel('X')
ax.set_ylabel('Y')

plt.show()
