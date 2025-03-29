import argparse
import re
import os

parser = argparse.ArgumentParser()

parser.description = "Compile the HD44780 driver for a specific board and interface."
parser.add_argument("-b" ,"--board",
                    description="The board to compile for. This will search <board>_<interface>_HAL"
                                " file in ./HAL",)
parser.add_argument("-i", "--interface",
                    description="The interface to compile for. This will search <board>_<interface>_HAL"
                                " file in ./HAL",)
parser.add_argument("-a", "--architecture",
                    description="The architecture to compile for.")
parser.add_argument("-o", "--output",
                    describption="Output path. Default is ./mpy/",
                    default="./mpy/")

relative_import_pattern = re.compile(r'(?<=\sfrom\s)\.\S+(?=\simport\s)|(?<=\simport\s)\.\S+')
visited_files = []

def remove_relative_imports(file_path, output_path):
    with open(file_path, 'r') as source_file:
        source_file_lines = source_file.readlines()

    with open(output_path, 'w') as output_file:
        for source_line in source_file_lines:

            # check if the line is a docstring or comment or does not contain a relative import
            if ( source_line.startswith('"""')     # ignore docstring
                or source_line.startswith('#')     # ignore comment
                or not relative_import_pattern.match(source_line) ):

                output_file.write(source_line)
                continue

            # Check if the file has already been visited
            if file_path in visited_files:
                print(f"Skipped {file_path} as it has already been visited.")
                continue

            visited_files.append(file_path)
            lib_path = relative_import_pattern.search(source_line)

            # If not relative import is found, ignore it
            if lib_path is None:
                output_file.write(source_line)
                print(f"Skipped {file_path} as it not relative.")
                continue

            with open(os.path.join(file_path, lib_path.group()), 'r') as lib_file:
                output_file.write(f"# ============== from {lib_path.group()} ==============")
                output_file.write(lib_file.read())
                output_file.write(f"# =====================================================")
                print(f"Removed relative import from {file_path}: {source_line}")
