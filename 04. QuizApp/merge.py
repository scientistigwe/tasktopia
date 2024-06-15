from PIL import Image
import os

def merge_images(image_dir, output_path, grid_size=(3, 9)):
    # Get a list of image file paths in the directory
    image_paths = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.endswith(('.jpg', '.jpeg'))]
    
    # Sort the images to ensure they are in the correct order
    image_paths.sort()
    
    # Check if we have exactly 27 images
    if len(image_paths) != 27:
        raise ValueError("There must be exactly 27 images in the directory")

    # Open images and store them in a list
    images = [Image.open(image_path) for image_path in image_paths]
    
    # Get the size of each image (assuming all images are the same size)
    image_width, image_height = images[0].size
    
    # Calculate the total size of the final merged image
    grid_width = grid_size[0] * image_width
    grid_height = grid_size[1] * image_height
    
    # Create a new blank image with the calculated size
    merged_image = Image.new('RGB', (grid_width, grid_height))
    
    # Paste images into the grid
    for index, image in enumerate(images):
        x = (index % grid_size[0]) * image_width
        y = (index // grid_size[0]) * image_height
        merged_image.paste(image, (x, y))
    
    # Save the merged image
    merged_image.save(output_path)
    print(f'Merged image saved to {output_path}')

# Directory containing the input images
image_dir = r'C:\Users\admin\Downloads\3months-SoA'
# Path to the output merged image
output_path = r'C:\Users\admin\Downloads\merged_image.jpg'

# Merge the images
merge_images(image_dir, output_path)
