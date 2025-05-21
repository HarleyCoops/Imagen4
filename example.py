#!/usr/bin/env python3
"""
Example script demonstrating how to use the Google Imagen 4 API directly.
"""

import os
from google import genai

# Get project ID from environment variable
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
if not project_id:
    project_id = input("Enter your Google Cloud project ID: ")

# Initialize the client
client = genai.Client(vertexai=True, project=project_id, location="us-central1")

# Example prompt
prompt = """
A white wall with two Art Deco travel posters mounted. First poster has the text: "NEPTUNE", 
tagline: "The jewel of the solar system!" Second poster has the text: "JUPITER", 
tagline: "Travel with the giants!"
"""

# Generate the image
image = client.models.generate_images(
    model="imagen-4.0-generate-preview-05-20",
    prompt=prompt,
)

# Save the image to a file
with open("example_output.png", "wb") as f:
    f.write(image.generated_images[0].image.data)

print("Image generated and saved as 'example_output.png'")

# Uncomment to display the image (works in Jupyter notebooks)
# image.generated_images[0].image.show()

