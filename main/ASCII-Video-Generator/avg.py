import sys
import os
import cv2
import time
import colorama
from colorama import Fore
colorama.init(autoreset=True)

# ASCII chars
ASCII_CHARS = "@%#*+=-:.1234567890qwertyuıopğü,asdfghjklşizxcvbnmöç."

def main():
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Incorrect use!")
        print(f"{Fore.LIGHTYELLOW_EX}Use: python avg.py <video>")
        sys.exit()

    video_path = sys.argv[1]

    input_dir = os.path.join(os.getcwd(), "engine", "image")
    output_dir = os.path.join(os.getcwd(), "engine", "usedImage")

    frameCount = extract_frames(video_path, input_dir)
    convert_to_ascii(input_dir, output_dir, frameCount)

    # showTime
    display_ascii_video(output_dir, frameCount)

def extract_frames(path, output_dir):
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        print(f"{Fore.RED}Error: Cannot open video {path}")
        return 0

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_filename, frame)

        print(f"{Fore.GREEN}Saved {Fore.LIGHTYELLOW_EX}{frame_count} ")

        frame_count += 1

    cap.release()
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print(f"{Fore.GREEN}Extraction completed. {Fore.CYAN}({frame_count} frames saved)")
    print(f"{Fore.CYAN}Initiating conversion..")
    time.sleep(3)
    return frame_count

def convert_to_ascii(input_dir, output_dir, frame_count):
    for i in range(frame_count):
        frame_path = os.path.join(input_dir, f"frame_{i:04d}.png")
        if not os.path.exists(frame_path):
            continue

        image = cv2.imread(frame_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        height, width = gray_image.shape
        aspect_ratio = height / width
        new_width = 100
        new_height = int(aspect_ratio * new_width * 0.55)
        resized_image = cv2.resize(gray_image, (new_width, new_height))


        ascii_image = ""
        for pixel_value in resized_image.flatten():
            ascii_image += ASCII_CHARS[pixel_value // 32]
        ascii_image = "\n".join([ascii_image[i:(i + new_width)] for i in range(0, len(ascii_image), new_width)])


        output_path = os.path.join(output_dir, f"ascii_frame_{i:04d}.txt")
        with open(output_path, "w") as f:
            f.write(ascii_image)

        print(f"{Fore.GREEN}Saved ASCII art !! ")

def display_ascii_video(output_dir, frame_count):
    while True:
        for i in range(frame_count):
            ascii_path = os.path.join(output_dir, f"ascii_frame_{i:04d}.txt")
            if not os.path.exists(ascii_path):
                continue

            with open(ascii_path, "r") as f:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(Fore.LIGHTBLACK_EX+f.read())

            time.sleep(0.0300)

if __name__ == "__main__":
    main()
