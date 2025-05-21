#!/usr/bin/env python3
"""
Imagen4 CLI - A command-line interface for Google's Imagen 4 image generation model.
This script allows users to input prompts from the terminal, sends them to the Imagen4 API,
and displays the generated images.
"""

import os
import sys
import argparse
from pathlib import Path
import tempfile
import webbrowser
from google import genai
from google.cloud import aiplatform

def setup_client(project_id=None, location="us-central1"):
    """
    Set up and return the Google Generative AI client.
    
    Args:
        project_id (str, optional): Google Cloud project ID. If None, will try to get from environment.
        location (str, optional): Google Cloud location. Defaults to "us-central1".
        
    Returns:
        genai.Client: Configured client for the Generative AI API
    """
    if not project_id:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Project ID must be provided either as an argument or via GOOGLE_CLOUD_PROJECT environment variable")
    
    return genai.Client(vertexai=True, project=project_id, location=location)

def generate_image(client, prompt, model="imagen-4.0-generate-preview-05-20", output_dir=None):
    """
    Generate an image based on the provided prompt.
    
    Args:
        client (genai.Client): The Google Generative AI client
        prompt (str): The text prompt for image generation
        model (str, optional): The model to use. Defaults to "imagen-4.0-generate-preview-05-20".
        output_dir (str, optional): Directory to save the generated image. If None, uses a temp directory.
        
    Returns:
        str: Path to the saved image
    """
    print(f"Generating image with prompt: {prompt}")
    
    try:
        response = client.models.generate_images(
            model=model,
            prompt=prompt,
        )
        
        # Save the image
        if output_dir:
            save_dir = Path(output_dir)
            save_dir.mkdir(exist_ok=True, parents=True)
        else:
            save_dir = Path(tempfile.gettempdir())
        
        # Create a safe filename from the prompt
        safe_prompt = "".join(c if c.isalnum() else "_" for c in prompt[:30])
        image_path = save_dir / f"imagen4_{safe_prompt}.png"
        
        # Save the image to disk
        with open(image_path, "wb") as f:
            f.write(response.generated_images[0].image.data)
        
        print(f"Image saved to: {image_path}")
        return str(image_path)
    
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def display_image(image_path):
    """
    Display the generated image using the default image viewer.
    
    Args:
        image_path (str): Path to the image file
    """
    if image_path and os.path.exists(image_path):
        print(f"Opening image: {image_path}")
        webbrowser.open(f"file://{os.path.abspath(image_path)}")
    else:
        print("No image to display.")

def main():
    parser = argparse.ArgumentParser(description="Generate images using Google's Imagen 4 model")
    parser.add_argument("--project", help="Google Cloud project ID")
    parser.add_argument("--location", default="us-central1", help="Google Cloud location")
    parser.add_argument("--output-dir", help="Directory to save generated images")
    parser.add_argument("--model", default="imagen-4.0-generate-preview-05-20", help="Model name to use")
    parser.add_argument("--prompt", help="Text prompt for image generation (if not provided, will prompt interactively)")
    
    args = parser.parse_args()
    
    try:
        # Set up the client
        client = setup_client(project_id=args.project, location=args.location)
        
        # Get the prompt
        if args.prompt:
            prompt = args.prompt
        else:
            prompt = input("Enter your image prompt: ")
        
        # Generate and display the image
        image_path = generate_image(client, prompt, model=args.model, output_dir=args.output_dir)
        if image_path:
            display_image(image_path)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

