from argparse import ArgumentParser
from pathlib import Path
from sys import argv
from typing import Optional

from PIL import Image

parser = ArgumentParser(prog="pic2jpg", description="Converts images to jpg format")
parser.add_argument("paths", nargs="+", type=Path, help="Path(s) to image file(s) or folder(s)")
args = parser.parse_args(argv[1:])

log_file = Path.cwd().joinpath("pic2jpg.log")
log_lines = []


def log(message: Optional[str] = None, dump: bool = False) -> None:
    if message is not None:
        log_lines.append(message)
    if dump:
        log_file.write_text("\n".join(log_lines))


def main(files: list[Path]) -> None:
    for file in files:
        out_file = file.with_suffix(".jpg")
        if out_file.exists():
            log(f"Skipping {file} as {out_file} already exists")
            continue
        try:
            img = Image.open(file)
            img.convert("RGB").save(out_file)
            log(f"Converted {file} to {out_file}")
        except Exception as e:
            log(f"Error converting {file}: {e}")


if __name__ == "__main__":
    # initialize PIL
    Image.init()
    # get supported extensions
    IMAGE_EXTENSIONS = Image.EXTENSION.keys()

    # Resolve paths
    paths = [path.resolve() for path in args.paths if path.exists()]

    # Get all files passed as arguments
    files: set[Path] = {x for x in paths if x.is_file() and x.suffix.lower() in IMAGE_EXTENSIONS}

    # Get all files in folders passed as arguments
    for folder in [x for x in paths if x.is_dir()]:
        files.update({x for x in folder.rglob("**/*") if x.suffix.lower() in IMAGE_EXTENSIONS})

    try:
        # run the conversion function
        main(files=files)
    finally:
        # make sure log is dumped
        log(dump=True)
