import argparse
import re
import os
from pathlib import Path
import mpy_cross

parser = argparse.ArgumentParser()

parser.description = "merge file to single .py and compiled .mpy file."
parser.add_argument("-s", "--source",
                    help="source file path.",
                    default=os.getcwd())
parser.add_argument("-o", "--output",
                    help="Output file path. Default is ./build/output.py",
                    default="./build/output.py")
parser.add_argument("--opt",
                    help="Set optimistic mode. As same as mpy-cross -O[N]. Default is 3.",
                    default="3",
                    choices=[0, 1, 2, 3])

args = parser.parse_args()

relative_import_pattern = re.compile(r'(?<=from\s)\.\S+(?=\simport\s)|(?<=import\s)\.\S+')

def resolve_dependence(source_file: Path) -> dict[str, dict|None]:
    dependence_tree = {}

    with open(source_file, "r") as file:
        for line in file.readlines():
            line = line.strip()
            if line.startswith('"""') or line.startswith('#'): continue

            matches = relative_import_pattern.search(line)
            if matches is None: continue

            called_lib_path = Path(source_file.parent, "." + matches.group(0).replace('.', '/') + ".py")
            dependence_tree[str(called_lib_path)] = None if len(d:=resolve_dependence(called_lib_path)) == 0 else d

    return dependence_tree


def get_file_insert_order(dependence_tree: dict[str, dict|None]) -> list[str]:
    result = []
    for key, value in dependence_tree.items():
        if value is None:
            result.append(key)
        else:
            result.extend(get_file_insert_order(value))
            result.append(key)
    return result

        

def merge_files(file_path:list[str], output_path:str) -> None:
    visited_files = {}
    with open(output_path, "w") as output_file:
        for path in file_path:

            if path in visited_files: continue
            visited_files[path] = None

            with open(path, "r") as file:
                output_file.write(f"# ==== {path} ====\r")

                for line in file.readlines():
                    if relative_import_pattern.search(line) is not None: continue
                    output_file.write(line)

                output_file.write("\r# ===================================\r\r")


def main():
    source = Path(os.path.join(os.getcwd(), args.source))
    output = Path(os.path.join(os.getcwd(), args.output))

    if source.is_dir(): RuntimeError("Source path is a directory")
    if output.is_dir():
        output = Path(os.path.join(str(output), source.name))

    output.parent.mkdir(parents=True, exist_ok=True)
    output.touch(exist_ok=True)

    dependence_tree = {str(source): resolve_dependence(source)}
    merge_files_order = get_file_insert_order(dependence_tree) + [str(source)]
    merge_files(merge_files_order, str(output))

    mpy_cross.run("-o", str(output.with_suffix('.mpy')), f"-O{args.opt}",  str(output))


if __name__ == "__main__":
    main()