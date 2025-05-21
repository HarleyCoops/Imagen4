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

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up Google Cloud authentication:
   ```
   gcloud auth application-default login
   ```

4. Set your Google Cloud project ID:
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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

