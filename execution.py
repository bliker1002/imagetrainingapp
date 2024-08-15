import subprocess
import sys
import pkg_resources
import json

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(error.decode())
        sys.exit(1)
    return output.decode()

def check_and_install_python_packages():
    required_packages = [
        'flask', 'flask-cors', 'boto3', 'stripe', 'sendgrid', 'anthropic',
        'torch', 'diffusers', 'transformers', 'datasets'
    ]

    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    missing_packages = [pkg for pkg in required_packages if pkg not in installed_packages]

    if missing_packages:
        print(f"Installing missing Python packages: {', '.join(missing_packages)}")
        run_command(f"pip install {' '.join(missing_packages)}")
    else:
        print("All required Python packages are installed.")

def check_and_install_node_packages():
    with open('package.json', 'r') as f:
        package_json = json.load(f)

    required_packages = package_json.get('dependencies', {})

    print("Checking Node.js packages...")
    for package, version in required_packages.items():
        try:
            run_command(f"npm list {package}")
        except subprocess.CalledProcessError:
            print(f"Installing missing Node.js package: {package}")
            run_command(f"npm install {package}@{version}")

    print("All required Node.js packages are installed.")

def setup_environment():
    print("Setting up environment...")
    check_and_install_python_packages()
    check_and_install_node_packages()

def start_backend():
    print("Starting backend server...")
    run_command("python backend.py &")

def build_frontend():
    print("Building frontend...")
    run_command("npm run build")

def start_frontend():
    print("Starting frontend server...")
    run_command("npm start")

if __name__ == "__main__":
    setup_environment()
    start_backend()
    build_frontend()
    start_frontend()