from pathlib import Path

from PIL import Image

Image.init()

input_icon = Path(__file__).parent.joinpath("icon.png")
output_icon = Path(__file__).parent.joinpath("icon.ico")


def main():
    print("Converting icon from PNG to multi-resolution ICO..")

    if "ICO" not in Image.SAVE.keys():
        raise RuntimeError("Pillow ICO plugin is missing or not installed!")

    if not input_icon.exists():
        raise FileNotFoundError(f"Input icon file {input_icon} does not exist!")

    # open the png
    image = Image.open(input_icon)
    # save the ico
    image.save(
        output_icon,
        format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (96, 96), (128, 128), (256, 256)],
    )
    print("Done!")


if __name__ == "__main__":
    main()
