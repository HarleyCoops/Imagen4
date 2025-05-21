#!/usr/bin/env python3
"""
Imagen4 Setup Script

This script helps users set up their environment for using the Imagen4 CLI tool.
It guides users through:
1. Installing required dependencies
2. Setting up Google Cloud authentication
3. Configuring project ID
4. Testing the connection to the Imagen4 API
"""

import os
import sys
import subprocess
import platform
import json
import tempfile
from pathlib import Path

def print_step(step_num, total_steps, message):
    """Print a formatted step message."""
    print(f"\n[{step_num}/{total_steps}] {message}")
    print("=" * 80)

def run_command(command, shell=False):
    """Run a shell command and return the result."""
    try:
        if shell:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        else:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr
    except Exception as e:
        return False, str(e)

def check_python_version():
    """Check if the Python version is compatible."""
    print_step(1, 6, "Checking Python version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required.")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade your Python installation.")
        return False
    
    print(f"✅ Python version {sys.version.split()[0]} is compatible.")
    return True

def install_dependencies():
    """Install required Python packages."""
    print_step(2, 6, "Installing dependencies")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found in the current directory.")
        return False
    
    success, output = run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    if not success:
        print(f"❌ Failed to install dependencies: {output}")
        return False
    
    print("✅ Dependencies installed successfully.")
    return True

def check_gcloud_installation():
    """Check if gcloud CLI is installed."""
    print_step(3, 6, "Checking Google Cloud SDK installation")
    
    success, output = run_command(["gcloud", "--version"])
    if not success:
        print("❌ Google Cloud SDK (gcloud) is not installed or not in PATH.")
        print("\nPlease install the Google Cloud SDK:")
        print("- Visit: https://cloud.google.com/sdk/docs/install")
        print("- Follow the installation instructions for your operating system.")
        print("- After installation, run 'gcloud init' to initialize the SDK.")
        print("- Then run this setup script again.")
        return False
    
    print("✅ Google Cloud SDK is installed.")
    return True

def setup_gcloud_auth():
    """Set up Google Cloud authentication."""
    print_step(4, 6, "Setting up Google Cloud authentication")
    
    print("This step will open a browser window for you to log in to your Google account.")
    print("If you're already authenticated, this step will be skipped.")
    
    input("Press Enter to continue...")
    
    success, output = run_command(["gcloud", "auth", "application-default", "login"])
    if not success:
        print(f"❌ Failed to set up authentication: {output}")
        return False
    
    print("✅ Google Cloud authentication set up successfully.")
    return True

def configure_project():
    """Configure the Google Cloud project ID."""
    print_step(5, 6, "Configuring Google Cloud project")
    
    # Check if project ID is already set in environment
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if project_id:
        print(f"Project ID is already set in environment: {project_id}")
        change = input("Do you want to change it? (y/N): ").lower()
        if change != 'y':
            return True, project_id
    
    # List available projects
    success, output = run_command(["gcloud", "projects", "list", "--format=json"])
    if not success:
        print(f"❌ Failed to list projects: {output}")
        project_id = input("Enter your Google Cloud project ID manually: ")
    else:
        try:
            projects = json.loads(output)
            if not projects:
                print("No projects found in your Google Cloud account.")
                project_id = input("Enter your Google Cloud project ID: ")
            else:
                print("\nAvailable projects:")
                for i, project in enumerate(projects, 1):
                    print(f"{i}. {project['projectId']} - {project.get('name', 'No name')}")
                
                choice = input("\nSelect a project number or enter a project ID manually: ")
                if choice.isdigit() and 1 <= int(choice) <= len(projects):
                    project_id = projects[int(choice) - 1]['projectId']
                else:
                    project_id = choice
        except json.JSONDecodeError:
            print("❌ Failed to parse project list.")
            project_id = input("Enter your Google Cloud project ID manually: ")
    
    # Set the project ID in the environment
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
    
    # Write to .env file for future use
    with open(".env", "w") as f:
        f.write(f"GOOGLE_CLOUD_PROJECT={project_id}\n")
    
    print(f"✅ Project ID '{project_id}' configured and saved to .env file.")
    print("You can load this in your shell with:")
    if platform.system() == "Windows":
        print("   set /p GOOGLE_CLOUD_PROJECT=<.env")
    else:
        print("   export GOOGLE_CLOUD_PROJECT=$(cat .env | grep GOOGLE_CLOUD_PROJECT | cut -d= -f2)")
    
    return True, project_id

def test_imagen_api(project_id):
    """Test the connection to the Imagen API."""
    print_step(6, 6, "Testing connection to Imagen API")
    
    try:
        from google import genai
        from google.cloud import aiplatform
        
        print("Initializing client...")
        client = genai.Client(vertexai=True, project=project_id, location="us-central1")
        
        print("Testing API access with a simple prompt...")
        # Use a very simple prompt for testing
        test_prompt = "A simple blue circle on a white background"
        
        response = client.models.generate_images(
            model="imagen-4.0-generate-preview-05-20",
            prompt=test_prompt,
        )
        
        # Save the test image
        test_dir = Path(tempfile.gettempdir())
        test_image_path = test_dir / "imagen4_test.png"
        
        with open(test_image_path, "wb") as f:
            f.write(response.generated_images[0].image.data)
        
        print(f"✅ Successfully connected to Imagen API!")
        print(f"✅ Test image saved to: {test_image_path}")
        
        # Ask if user wants to view the image
        view_image = input("Do you want to view the test image? (y/N): ").lower()
        if view_image == 'y':
            import webbrowser
            webbrowser.open(f"file://{test_image_path.absolute()}")
        
        return True
    except ImportError:
        print("❌ Failed to import required modules. Make sure dependencies are installed.")
        return False
    except Exception as e:
        print(f"❌ Failed to connect to Imagen API: {str(e)}")
        print("\nPossible reasons:")
        print("1. Your Google Cloud project doesn't have access to the Imagen API")
        print("2. The Imagen API is not enabled for your project")
        print("3. Authentication issues with your Google Cloud account")
        print("\nTo request access to Imagen:")
        print("- Visit: https://developers.generativeai.google/products/imagen")
        print("- Follow the instructions to request access for your project")
        return False

def main():
    """Main function to run the setup process."""
    print("\n" + "=" * 80)
    print("Welcome to the Imagen4 CLI Setup".center(80))
    print("=" * 80)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check gcloud installation
    if not check_gcloud_installation():
        return False
    
    # Set up authentication
    if not setup_gcloud_auth():
        return False
    
    # Configure project
    success, project_id = configure_project()
    if not success:
        return False
    
    # Test Imagen API
    if not test_imagen_api(project_id):
        return False
    
    print("\n" + "=" * 80)
    print("🎉 Setup completed successfully! 🎉".center(80))
    print("=" * 80)
    print("\nYou can now use the Imagen4 CLI tool:")
    print("python imagen4_cli.py --prompt \"Your creative prompt here\"")
    print("\nOr run the example script:")
    print("python example.py")
    print("\nEnjoy creating amazing images with Imagen4!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nAn unexpected error occurred: {str(e)}")
        sys.exit(1)

