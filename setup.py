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
    
    gcloud_cmd = "gcloud"
    success, output = run_command([gcloud_cmd, "--version"])
    
    if not success:
        # Try with the known full path if the simple command fails
        print("   Attempting to use known SDK path...")
        # For Windows, gcloud is often a .cmd file.
        # The path needs to be specific to your user and OS.
        # $env:LOCALAPPDATA usually C:\Users\<username>\AppData\Local
        # This path should be confirmed or made more robust if possible
        # For this user, it's C:\Users\chris\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd
        # subprocess.run on Windows can often execute .cmd files directly when given the full path.
        
        # Let's construct the path dynamically if possible, or hardcode for now if sure
        # For simplicity in this step, we'll use the known path for 'chris'
        # A more robust solution would involve discovering this path or having user confirm/input
        
        # Determine the OS and construct the path
        sdk_bin_path = ""
        if platform.system() == "Windows":
            local_app_data = os.getenv('LOCALAPPDATA')
            if local_app_data:
                sdk_bin_path = Path(local_app_data) / "Google" / "Cloud SDK" / "google-cloud-sdk" / "bin"
                gcloud_cmd_path = sdk_bin_path / "gcloud.cmd" # For Windows
            else: # Fallback if LOCALAPPDATA is not set, though unlikely
                gcloud_cmd_path = Path("C:/Users/chris/AppData/Local/Google/Cloud SDK/google-cloud-sdk/bin/gcloud.cmd")
        elif platform.system() == "Linux" or platform.system() == "Darwin": # macOS
            # Common paths for gcloud on Linux/macOS - this is a guess
            # User might have installed it elsewhere (e.g. /usr/local/google-cloud-sdk/bin/gcloud)
            # Or via package managers (snap, apt, brew) which put it in standard PATH locations
            # This part is less certain without knowing the install method on non-Windows
            # For now, let's assume if it's not in PATH on Linux/Mac, the user needs to fix PATH
            # Or we could prompt for the path.
            # Given the user is on Windows, we focus on the Windows path.
            pass # No specific fallback path for non-Windows in this quick fix

        if platform.system() == "Windows" and 'gcloud_cmd_path' in locals() and gcloud_cmd_path.exists():
            print(f"   Trying full path: {gcloud_cmd_path}")
            gcloud_cmd = str(gcloud_cmd_path)
            success, output = run_command([gcloud_cmd, "--version"])
        
    if not success:
        print("❌ Google Cloud SDK (gcloud) is not installed or not in PATH.")
        print("   Even after attempting a known common path, gcloud was not found or failed.")
        print("\nPlease install the Google Cloud SDK:")
        print("- Visit: https://cloud.google.com/sdk/docs/install")
        print("- Follow the installation instructions for your operating system.")
        print("- After installation, run 'gcloud init' to initialize the SDK.")
        print("- Then run this setup script again.")
        return False
    
    print("✅ Google Cloud SDK is installed.")
    # Store the successfully used command for other functions to use
    # This is a bit of a hack; a better way would be to pass gcloud_cmd around
    # or set it as a global/class variable if this script were a class.
    # For now, we'll modify other calls directly if needed, or assume PATH works after this.
    # Let's assume if check_gcloud_installation passes, subsequent 'gcloud' calls will use the same mechanism.
    # The run_command will try 'gcloud' first, which might now work if PATH was the issue for this session.
    # If not, we might need to pass the full path to other gcloud calls too.
    # For now, let's assume the PATH issue is intermittent or session-specific and this check helps.
    # A more robust fix would be to ensure gcloud_cmd (potentially full path) is used everywhere.
    
    # To make it more robust, let's modify other gcloud calls to use the determined gcloud_cmd
    # We'll need to pass this 'gcloud_cmd' to other functions or make it accessible.
    # For a quick fix, we can just update the calls in other functions if this one succeeds with a full path.
    # This is getting complex for a quick fix. Let's try a simpler approach first:
    # If the full path worked, subsequent calls to 'gcloud' in the *same script run* might also need the full path.
    # The simplest change is to ensure `check_gcloud_installation` returns the command to use.
    
    # Let's refine: check_gcloud_installation will return the command string (either 'gcloud' or full path)
    # And the main function will pass it to other functions. This is cleaner.
    # This requires more extensive changes to the function signatures.

    # Alternative: If the full path works, we can try to add its directory to the PATH for this script's session.
    if success and gcloud_cmd != "gcloud": # Means full path was used
        gcloud_dir = str(Path(gcloud_cmd).parent)
        print(f"   Adding {gcloud_dir} to PATH for this session.")
        os.environ["PATH"] = gcloud_dir + os.pathsep + os.environ["PATH"]
        # Now, subsequent calls to "gcloud" in this script *should* find it.
    
    if success:
        return True, gcloud_cmd # Return the command that worked
    else:
        return False, None

def setup_gcloud_auth(gcloud_executable):
    """Set up Google Cloud authentication."""
    print_step(4, 6, "Setting up Google Cloud authentication")
    
    print("This step will open a browser window for you to log in to your Google account.")
    print("If you're already authenticated, this step will be skipped.")
    
    input("Press Enter to continue...")
    
    success, output = run_command([gcloud_executable, "auth", "application-default", "login"])
    if not success:
        print(f"❌ Failed to set up authentication: {output}")
        return False
    
    print("✅ Google Cloud authentication set up successfully.")
    return True

def configure_project(gcloud_executable):
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
    success, output = run_command([gcloud_executable, "projects", "list", "--format=json"])
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
    gcloud_ok, gcloud_cmd_to_use = check_gcloud_installation()
    if not gcloud_ok:
        return False
    
    # Set up authentication
    if not setup_gcloud_auth(gcloud_cmd_to_use):
        return False
    
    # Configure project
    success, project_id = configure_project(gcloud_cmd_to_use)
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
