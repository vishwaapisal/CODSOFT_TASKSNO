from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Load the pre-trained image captioning model
print("Loading image captioning model...")

processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

print("Model loaded successfully!")


def generate_caption(image_path):
    # Open the image
    image = Image.open(image_path).convert("RGB")

    # Prepare image for the model
    inputs = processor(images=image, return_tensors="pt")

    # Generate caption
    output = model.generate(**inputs, max_new_tokens=30)

    # Convert generated tokens into text
    caption = processor.decode(output[0], skip_special_tokens=True)

    return caption


# Ask the user for an image
image_path = input("Enter the path of your image: ")

try:
    caption = generate_caption(image_path)

    print("\nGenerated Caption:")
    print(caption)

except Exception as e:
    print("\nError:", e)