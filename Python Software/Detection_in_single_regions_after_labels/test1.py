import numpy as np
import cv2
import matplotlib.pyplot as plt

def create_mask(polygon, shape):
    """Create a binary mask from a polygon."""
    mask = np.zeros(shape, dtype=np.uint8)
    cv2.fillPoly(mask, [polygon], 1)
    return mask

def are_polygons_partially_inside(mask, polygons, threshold=0.7):
    """Check if at least `threshold` percent of the vertices of the polygons are inside the mask."""
    polygons_array = np.array(polygons, dtype=np.int32)
    
    # Extract the y and x coordinates separately
    y_coords, x_coords = polygons_array[:, :, 1], polygons_array[:, :, 0]
    
    # Check if all points of each polygon are inside the mask
    inside_mask = mask[y_coords, x_coords]
    
    # Calculate the percentage of points inside the mask for each polygon
    inside_ratio = np.mean(inside_mask, axis=1)
    
    # A polygon is considered partially inside if the inside_ratio is greater than or equal to the threshold
    return inside_ratio >= threshold

def count_polygons_partially_inside(big_polygon, small_polygons, image_shape, threshold=0.7):
    """Count the number of small polygons that are at least `threshold` percent inside the big polygon."""
    big_polygon_mask = create_mask(np.array(big_polygon, dtype=np.int32), image_shape)
    
    # Check which polygons meet the inside threshold
    inside_flags = are_polygons_partially_inside(big_polygon_mask, small_polygons, threshold)
    
    # Sum the number of True flags to get the count
    return np.sum(inside_flags)

# Example usage
big_polygon = [(50, 50), (300, 50), (300, 300), (50, 300)]
small_polygons = [
    [(100, 100), (150, 100), (150, 150), (100, 150)],
    [(200, 200), (250, 200), (250, 250), (200, 250)],
    [(400, 400), (450, 400), (450, 450), (400, 450)],  # Completely outside
    [(250, 250), (350, 250), (350, 350), (250, 350)]   # Partially inside polygon
]

image_shape = (500, 500)  # height, width
count = count_polygons_partially_inside(big_polygon, small_polygons, image_shape, threshold=0.7)
print(f"Number of small polygons with at least 70% of their vertices inside the big polygon: {count}")

# Visualizing
plt.figure(figsize=(6, 6))
plt.imshow(create_mask(np.array(big_polygon, dtype=np.int32), image_shape), cmap='gray')
for poly in small_polygons:
    poly = np.array(poly)
    plt.plot(poly[:, 0], poly[:, 1], 'r-')
plt.show()
