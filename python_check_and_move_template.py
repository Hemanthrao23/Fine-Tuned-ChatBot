import os
import shutil

# Define the paths
project_dir = os.path.dirname(os.path.abspath(__file__))  # Current project directory
templates_dir = os.path.join(project_dir, 'templates')

# List of required template files
required_templates = ['home.html', 'login.html', 'register.html', 'chat.html']

# Ensure `templates` folder exists; create it if not
if not os.path.exists(templates_dir):
    print("Creating 'templates' folder...")
    os.makedirs(templates_dir)

# Check and move each template file
for template in required_templates:
    target_path = os.path.join(templates_dir, template)
    found = False

    # Search for the template in the project directory and its subdirectories
    for root, dirs, files in os.walk(project_dir):
        if template in files:
            current_path = os.path.join(root, template)
            print(f"Found '{template}' at: {current_path}")
            found = True
            
            # Move to `templates` folder if not already there
            if current_path != target_path:
                print(f"Moving '{template}' to {templates_dir}")
                shutil.move(current_path, target_path)
            else:
                print(f"'{template}' is already in the correct 'templates' folder.")
            break

    # Notify if the template was not found
    if not found:
        print(f"'{template}' not found in the project directory. Please create it in the 'templates' folder.")

print("Template file check and move completed.")
