import sys
import os
import cv2
import colorama
from colorama import Fore

# ASCII karakter seti
ASCII_CHARS = "@%#*+=-:. "

def main():
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python avg.py <video>")
        sys.exit()

    video_path = sys.argv[1]

    # Karelerin saklanacağı dizinler
    input_dir = os.path.join(os.getcwd(), "engine", "image")
    output_dir = os.path.join(os.getcwd(), "engine", "usedImage")

    # Dizinler mevcut değilse oluştur
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Kareleri çıkar
    frameCount = extract_frames(video_path, input_dir)

    # ASCII dönüştürme işlemini yap
    convert_to_ascii(input_dir, output_dir, frameCount)

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

        print(f"Saved {frame_filename}")

        frame_count += 1

    cap.release()
    print(f"{Fore.GREEN}Extraction completed. {frame_count} frames saved.")
    return frame_count

def convert_to_ascii(input_dir, output_dir, frame_count):
    for i in range(frame_count):
        frame_path = os.path.join(input_dir, f"frame_{i:04d}.png")
        if not os.path.exists(frame_path):
            continue

        # Resmi oku ve gri tonlamaya çevir
        image = cv2.imread(frame_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Boyutu ASCII karakterlerine uyacak şekilde küçült
        height, width = gray_image.shape
        aspect_ratio = height / width
        new_width = 100  # Genişlik
        new_height = int(aspect_ratio * new_width * 0.55)  # Yükseklik (ASCII karakterler için oran ayarı)
        resized_image = cv2.resize(gray_image, (new_width, new_height))

        # ASCII karakterlerine dönüştür
        ascii_image = ""
        for pixel_value in resized_image.flatten():
            ascii_image += ASCII_CHARS[pixel_value // 32]
        ascii_image = "\n".join([ascii_image[i:(i + new_width)] for i in range(0, len(ascii_image), new_width)])

        # ASCII resmini dosyaya kaydet
        output_path = os.path.join(output_dir, f"ascii_frame_{i:04d}.txt")
        with open(output_path, "w") as f:
            f.write(ascii_image)

        print(f"Saved ASCII art {output_path}")

if __name__ == "__main__":
    main()
