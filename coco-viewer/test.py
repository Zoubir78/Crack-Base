import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# Load annotations
with open('C:/Users/z.marouf-araibi/Desktop/test2/annotations.json', 'r') as f:
    coco_data = json.load(f)

# Create a mapping from image ID to image info
image_id_to_info = {image['id']: image for image in coco_data['images']}

# Create a mapping from image ID to list of annotations
image_id_to_annotations = {}
for annotation in coco_data['annotations']:
    image_id = annotation['image_id']
    if image_id not in image_id_to_annotations:
        image_id_to_annotations[image_id] = []
    image_id_to_annotations[image_id].append(annotation)

# Category ID to name mapping (customize this based on your categories)
category_id_to_name = {1: 'Category 1', 2: 'Category 2', 3: 'Category 3'}  # Update with actual category names

def display_image_with_annotations(image_info, annotations):
    image_path = image_info['file_name']
    image = Image.open(image_path)
    fig, ax = plt.subplots(1)
    ax.imshow(image)

    for annotation in annotations:
        bbox = annotation['bbox']
        category_id = annotation['category_id']
        category_name = category_id_to_name.get(category_id, 'Unknown')

        # Create a Rectangle patch
        rect = patches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        plt.text(bbox[0], bbox[1], category_name, bbox=dict(facecolor='yellow', alpha=0.5))

    plt.show()

def main():
    for image_id, image_info in image_id_to_info.items():
        annotations = image_id_to_annotations.get(image_id, [])
        display_image_with_annotations(image_info, annotations)

if __name__ == "__main__":
    main()
