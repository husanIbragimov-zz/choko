import PIL

# Importing Required Modules 
from rembg import remove 
from PIL import Image 

# Store path of the image in the variable input_path 
input_path = "/home/oqdev/Downloads/mac.webp"

# Store path of the output image in the variable output_path 
output_path = '/home/oqdev/Downloads/removed.png' 

# Processing the image 
input = Image.open(input_path) 

# Removing the background from the given Image 
output = remove(input) 

#Saving the image in the given path 
output.save(output_path) 


background_color = (255, 255, 255)  # RGB color for white

# Create a new image with the desired background color
output_with_background = Image.new("RGB", output.size, background_color)

# Paste the removed image onto the new image with the background color
output_with_background.paste(output, (0, 0), output)

# Saving the image with the new background color
output_with_background.save("/home/oqdev/Downloads/removed.png")