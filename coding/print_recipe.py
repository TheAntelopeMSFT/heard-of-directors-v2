# filename: print_recipe.py

def print_recipe(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print("The file was not found. Please check the file path and try again.")

# Replace 'path_to_recipe.txt' with the actual path to your recipe file.
print_recipe('path_to_recipe.txt')