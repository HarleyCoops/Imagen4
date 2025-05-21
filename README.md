# Imagen4 CLI

A command-line interface for Google's Imagen 4 image generation model.

## Features

- Generate images from text prompts using Google's Imagen 4 model
- Input prompts directly from the terminal
- Automatically display generated images
- Save images to a specified directory

## Prerequisites

- Python 3.7+
- Google Cloud account with Imagen 4 API access
- Google Cloud authentication set up on your machine

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/HarleyCoops/Imagen4.git
   cd Imagen4
   ```

2. Run the automated setup script:
   ```
   python setup.py
   ```
   
   This script will:
   - Install required dependencies
   - Check and set up Google Cloud authentication
   - Help you select a Google Cloud project
   - Test your connection to the Imagen API
   - Save your configuration for future use

3. Alternatively, you can set up manually:

   a. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

   b. Set up Google Cloud authentication:
   ```
   gcloud auth application-default login
   ```

   c. Set your Google Cloud project ID:
   ```
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   ```

## Usage

### Basic Usage

Run the script and enter your prompt when prompted:

```
python imagen4_cli.py
```

### Command-line Arguments

```
python imagen4_cli.py --prompt "A white wall with two Art Deco travel posters"
```

### Available Options

- `--project`: Google Cloud project ID (if not set in environment)
- `--location`: Google Cloud location (default: us-central1)
- `--output-dir`: Directory to save generated images
- `--model`: Model name to use (default: imagen-4.0-generate-preview-05-20)
- `--prompt`: Text prompt for image generation

### Examples

Generate an image with a specific prompt:
```
python imagen4_cli.py --prompt "A futuristic cityscape with flying cars and neon lights"
```

Save images to a specific directory:
```
python imagen4_cli.py --output-dir ./generated_images
```

Use a specific Google Cloud project:
```
python imagen4_cli.py --project my-gcp-project-id
```

## Troubleshooting

If you encounter issues:

1. **API Access**: Make sure you have access to the Imagen API. Visit [Google's Generative AI documentation](https://developers.generativeai.google/products/imagen) to request access.

2. **Authentication**: Ensure you're properly authenticated with Google Cloud:
   ```
   gcloud auth application-default login
   ```

3. **Project Configuration**: Verify your project ID is correctly set:
   ```
   echo $GOOGLE_CLOUD_PROJECT
   ```

4. **Run Setup Again**: If you're still having issues, try running the setup script again:
   ```
   python setup.py
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
