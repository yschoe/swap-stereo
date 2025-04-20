'''
https://github.com/yschoe/swap-stereo
'''

from PIL import ImageGrab, Image
import numpy as np
import cv2
import sys
import pyautogui

def get_clipboard_image():
    try:
        img = ImageGrab.grabclipboard()
        if isinstance(img, Image.Image):
            return img
        else:
            print("No image found in clipboard.")
            sys.exit(1)
    except Exception as e:
        print(f"Error accessing clipboard: {e}")
        sys.exit(1)

def swap_image_halves(img: Image.Image) -> np.ndarray:
    img_np = np.array(img)
    h, w, c = img_np.shape

    mid_x = w // 2
    left = img_np[:, :mid_x]
    right = img_np[:, mid_x:]

    # Handle odd widths
    if w % 2 != 0:
        center_column = img_np[:, mid_x:mid_x+1]
        swapped = np.hstack((right, center_column, left))
    else:
        swapped = np.hstack((right, left))

    return swapped

def resize_to_fit_screen(img: np.ndarray, margin=100) -> np.ndarray:
    screen_width, screen_height = pyautogui.size()
    screen_width -= margin
    screen_height -= margin

    h, w = img.shape[:2]
    scale = min(screen_width / w, screen_height / h, 1.0)  # don't upscale

    if scale < 1.0:
        new_w = int(w * scale)
        new_h = int(h * scale)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    return img

def main():
    img = get_clipboard_image()
    swapped = swap_image_halves(img)
    resized = resize_to_fit_screen(swapped)

    cv2.imshow("Swapped Clipboard Image", cv2.cvtColor(resized, cv2.COLOR_RGB2BGR))

    while True:
        key = cv2.waitKey(0)
        if key == 27:  # ESC
            break
        elif key == ord('s'):
            cv2.imwrite("swapped_output.png", cv2.cvtColor(swapped, cv2.COLOR_RGB2BGR))
            print("Image saved as swapped_output.png")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

