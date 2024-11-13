import numpy as np
import matplotlib.pyplot as plt

class create_shapes:
      def __init__(self, left, top, width, height):
        self.top_left_x  = left
        self.top_left_y = top
        self.width = width
        self.height = height

      '''
      output: 90 pair points of x and y of an oval perimeter
      '''
      def create_oval(self):
        # Define the oval parameters
        # top_left_x = 11728  # x-coordinate of the top-left corner left
        # top_left_y = 6837  # y-coordinate of the top-left corner top
        # width = 2464      # width of the oval
        # height = 3686     # height of the oval

        # Calculate the center of the oval
        center_x = self.top_left_x + self.width / 2
        center_y = self.top_left_y + self.height / 2

        # Calculate the semi-major and semi-minor axes
        a = self.width / 2  # semi-major axis (half of the width)
        b = self.height / 2 # semi-minor axis (half of the height)

        # Generate angles from 0 to 2*pi to get points along the perimeter
        theta = np.linspace(0, 2 * np.pi, 90)  # 180 points along the perimeter

        # Parametric equations for the ellipse
        x_perimeter = center_x + a * np.cos(theta)
        y_perimeter = center_y + b * np.sin(theta)

        # Now you have the (x, y) coordinates of all points on the oval's perimeter
        # print(x_perimeter)
        # print(y_perimeter)

        paired_list = list(zip(x_perimeter, y_perimeter))
        return paired_list

# Optionally, plot the oval perimeter
#plt.figure()
#plt.plot(x_perimeter, y_perimeter, 'b-')
#plt.gca().set_aspect('equal', adjustable='box')
#plt.title("Perimeter of the Oval")
#plt.show()
