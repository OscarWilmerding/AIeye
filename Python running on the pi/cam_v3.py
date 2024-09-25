import sys
import pygame
import subprocess
import time
import requests
import json
import base64
import os
from openai import OpenAI
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap
from gpiozero import RotaryEncoder, Button
from signal import pause
import threading

# Global variables for API keys and settings
ASTICA_API_KEY = ''
OPENAI_API_KEY = ''
ASTICA_API_TIMEOUT = 25
ASTICA_API_ENDPOINT = 'https://vision.astica.ai/describe'
ASTICA_API_MODEL_VERSION = '2.1_full'
ASTICA_API_VISION_PARAMS = 'gpt'

# Define global variables for the indices and lists
var1_index = 0
var1_list = ['normal', 'melancholy', 'awe inspiring', 'desolate', 'tranquil', 'evil', 'vengeful', 'nostalgic', 'mysterious', 'hyper-realistic', 'chaotic', 'weird', 'unhinged','robotic', 'overgrown', 'brutalist', 'devious']

#for settings menu
settings_options = ['Load WiFi Credentials, Must Reboot After', 'Update Photo Rotation']  #option 3 and option 4 are settings options names that have a template for a command to be executed in the execute_settings_option function if you want to add them here
settings_index = 0

encoder_var1 = RotaryEncoder(20,21)
button_var1 = Button(16)
button_var2 = Button(5, pull_up=True)  #  button for 'settings'
button_var3 = Button(6, pull_up=True)  #  button for 'playback

bg_color = pygame.Color("#1E2438")
text_color = pygame.Color("#F1F2ED")
font_path = "/home/oewil/Documents/Futura Std Heavy Oblique.otf"
font_size = 24

image_values = 0
knob_value = 0

# Initialize Pygame and set up the display
def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    global custom_font
    custom_font = pygame.font.Font(font_path, font_size)
    pygame.mouse.set_visible(False)
    return screen

screen = init_pygame()

directory = "/boot/photos"

def create_text_image(paragraph, theme_word, font_path, font_size=52, image_width=800, image_height=600, 
                      text_color="#FFFFFF", bg_color="#000000", margin=50, save_path="output_image.png"):
    """Creates an image with a theme label above a centered paragraph of text.

    Args:
        paragraph (str): The paragraph of text to display.
        theme_word (str): The single word theme to display above the paragraph.
        font_path (str): Path to the font file to use.
        font_size (int, optional): Font size for the text. Defaults to 24.
        image_width (int, optional): Width of the image in pixels. Defaults to 800.
        image_height (int, optional): Height of the image in pixels. Defaults to 600.
        text_color (str, optional): Hex color code for the text color. Defaults to "#FFFFFF".
        bg_color (str, optional): Hex color code for the background color. Defaults to "#000000".
        margin (int, optional): Margin between the text and the edges of the image. Defaults to 50.
        save_path (str, optional): Filepath to save the image. Defaults to "output_image.png".
    """
    # Create a blank image with the specified background color
    image = Image.new('RGB', (image_width, image_height), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Load the specified font
    font = ImageFont.truetype(font_path, 48)
    # Prepare the theme text
    theme_text = f"A {theme_word} image"
    theme_width, theme_height = draw.textsize(theme_text, font=font)

    # Split the paragraph into lines of 7 words each
    words = paragraph.split()
    lines = [' '.join(words[i:i + 7]) for i in range(0, len(words), 7)]

    # Calculate the height of the paragraph text
    line_height = font.getsize('Ag')[1]
    line_spacing = 18  # Spacing between lines
    num_lines = len(lines)
    total_paragraph_height = num_lines * line_height + (num_lines - 1) * line_spacing

    # Calculate the total height of the combined text block (theme text + paragraph)
    total_text_height = theme_height + total_paragraph_height

    # Calculate the starting y position to vertically center the combined text block
    start_y = (image_height - total_text_height) // 2

    # Draw the theme text at the calculated position
    theme_x = (image_width - theme_width) // 2
    draw.text((theme_x, start_y), theme_text, font=font, fill=text_color)

    # Draw each line of the paragraph text on the image, centered horizontally
    text_y_position = start_y + theme_height

    for line in lines:
        line_width, _ = draw.textsize(line, font=font)
        text_x_position = (image_width - line_width) // 2
        draw.text((text_x_position, text_y_position), line, font=font, fill=text_color)
        text_y_position += line_height + line_spacing

    # Save the image to the specified path
    image.save(save_path)
    print(f"Image saved to {save_path}")

def load_rotation_value():
    """Loads the rotation value from the text file."""
    rotation_file = '/home/oewil/rotation_value'
    try:
        with open(rotation_file, 'r') as file:
            rotation_value = int(file.read().strip())
            return rotation_value
    except FileNotFoundError:
        return 0  # Default to 0 if the file doesn't exist
    except ValueError:
        return 0  # Default to 0 if there's an error in reading the file

def get_file_by_recency(index):
    # Ensure index is non-negative
    index = max(0, index)

    # Get all files in the directory, sorted by modification time (most recent first)
    try:
        files = [os.path.join(directory, f) for f in os.listdir(directory)]
        files = [f for f in files if os.path.isfile(f)]
        files.sort(key=os.path.getmtime, reverse=True)
    except Exception as e:
        return f"Error accessing directory or sorting files: {str(e)}"

    # Check if the index is within the bounds of available files
    if index >= len(files):
        # If index is out of bounds, return the oldest file
        index = len(files) - 1 if files else 0  # Adjust index to the oldest file's index

    # Return the path of the file corresponding to the adjusted index
    return files[index] if files else "No files found in the directory"

def display_image(image_values):
    image_path = get_file_by_recency(image_values)

    # Load the image from the path and maintain aspect ratio
    def load_and_scale_image(path, screen_size):
        # Load the image
        image = pygame.image.load(path)
        # Determine scaling factor to maintain aspect ratio
        img_width, img_height = image.get_size()
        scale = min(screen_size[0] / img_width, screen_size[1] / img_height)
        # Apply scaling
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        return pygame.transform.scale(image, (new_width, new_height))

    # Center and draw the image on the screen
    def draw_image_centered(screen, image):
        img_width, img_height = image.get_size()
        screen_size = screen.get_size()
        x = (screen_size[0] - img_width) // 2
        y = (screen_size[1] - img_height) // 2
        screen.blit(image, (x, y))

    # Clear the screen with the specified background color
    screen.fill((25, 25, 25))

    # Load, scale, and draw the image
    image = load_and_scale_image(image_path, screen.get_size())
    draw_image_centered(screen, image)

    # Update the display
    pygame.display.flip()

def display_filler_text(screen, custom_font, sentence, text_color, bg_color):
    screen.fill(bg_color)
    screen_width, screen_height = screen.get_size()
    text_surface = custom_font.render(sentence, True, text_color)
    text_rect = text_surface.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

# Load and render text
def render_text(screen, custom_font, sentence, text_color, bg_color):
    screen.fill(bg_color)
    screen_width, screen_height = screen.get_size()
    text_surface = custom_font.render(sentence, True, text_color)
    text_rect = text_surface.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

def update_rotation_value():
    """Updates the rotation value by adding 90. Resets to 0 if the value is 360."""
    rotation_file = '/home/oewil/rotation_value'
    rotation_value = load_rotation_value()
    
    # Add 90 degrees to the current rotation value
    rotation_value += 90
    
    # Reset to 0 if the value is 360
    if rotation_value >= 360:
        rotation_value = 0
    
    # Save the updated rotation value back to the file
    with open(rotation_file, 'w') as file:
        file.write(str(rotation_value))
    
    print(f"Rotation value updated to {rotation_value}°")
    return rotation_value

def take_photo_and_save():
    """Takes a photo and saves it with a Unix timestamp-based filename using rotation value from the text file."""
    photo_timestamp = int(time.time())
    photo_filename = f"img_{photo_timestamp}.jpg"
    photo_directory = '/boot/photos'
    photo_path = os.path.join(photo_directory, photo_filename)

    rotation_value = load_rotation_value()

    try:
        subprocess.run(['raspistill', '-o', photo_path, '-rot', str(rotation_value)], check=True)
        print(f"Photo saved to {photo_path} with rotation {rotation_value}°")
        return photo_path, photo_timestamp  # Return both path and timestamp
    except subprocess.CalledProcessError as e:
        print(f"Failed to take photo: {e}")
        return None, None  # Return None for both values on failure

def get_image_base64_encoding(image_path):
    """Encodes an image at `image_path` to a base64 string."""
    with open(image_path, 'rb') as file:
        image_data = file.read()
    image_extension = os.path.splitext(image_path)[1]
    return f"data:image/{image_extension[1:]};base64,{base64.b64encode(image_data).decode('utf-8')}"

def asticaAPI(payload):
    """Sends a request to the asticaVision API and returns the response."""
    headers = {'Content-Type': 'application/json'}
    response = requests.post(ASTICA_API_ENDPOINT, data=json.dumps(payload), timeout=ASTICA_API_TIMEOUT, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to connect to the API.")
        return None

def save_image_from_url(url, timestamp):
    """Downloads an image from a URL and saves it with the Unix timestamp."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        image_name = f"img_{timestamp}_GENERATED.jpg"  # Use the timestamp here

        save_path = os.path.join("/boot/photos", image_name)
        image.save(save_path)

        print(f"Image saved successfully to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download the image: {e}")
    except IOError as e:
        print(f"Failed to save the image: {e}")

def display_image_from_url(url):
    """Fetches and displays an image from `url`."""
    response = requests.get(url)
    if response.status_code == 200:
        Image.open(BytesIO(response.content)).show()
    else:
        print("Failed to fetch the image.")

def cam_sequence(mood):
    """Main function orchestrating the process."""
    print(f"Python version: {sys.version}")
    print(f"sys.path: {sys.path}")

    image_path, image_timestamp = take_photo_and_save()  # Capture both values
    if not image_path:
        return

    display_filler_text(screen, custom_font, "Analyzing photo and generating description", text_color, bg_color)

    asticaAPI_input = get_image_base64_encoding(image_path)
    asticaAPI_payload = {
        'tkn': ASTICA_API_KEY,
        'modelVersion': ASTICA_API_MODEL_VERSION,
        'visionParams': ASTICA_API_VISION_PARAMS,
        'input': asticaAPI_input,
    }

    api_result = asticaAPI(asticaAPI_payload)
    if not api_result:
        return

    print('\nastica API Output:')
    print(json.dumps(api_result, indent=4))

    display_filler_text(screen, custom_font, "Generating a new image", text_color, bg_color)

    if api_result.get('status') == 'success':
        raw_description = api_result.get("caption_GPTS", "")
        
        create_text_image(paragraph = raw_description, theme_word = mood, font_path=font_path, font_size=34, image_width=1200, image_height=1200, 
                      text_color = (241,242,237), bg_color = (30,36,56), margin=50, save_path=f"/boot/photos/img_{str(int(time.time()))}.jpg")
        final_description = f"the most important part of this image is that the mood is {mood}, the image should look like this: {raw_description}. REMEMBER that the general mood should be {mood}. Please make sure the mood is {mood} that is the most important part of this image."
        print("final description = " + final_description)
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.images.generate(
            model="dall-e-3",
            prompt=final_description,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        print(image_url)
        save_image_from_url(image_url, image_timestamp)  # Pass the timestamp here

def display_sentence():
    global var1_index
    sentence = f"A {var1_list[var1_index]} photo."

    screen.fill(bg_color)
    screen_width, screen_height = screen.get_size()
    text_surface = custom_font.render(sentence, True, text_color)
    text_rect = text_surface.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

def update_values(change):
    global var1_index, image_values, settings_index
    if current_display == 'text':
        var1_index = (var1_index + change) % len(var1_list)
        print(f'Mood index changed to {var1_index}')
        display_sentence()
    elif current_display == 'image':
        print(f'change detected is {change}')
        image_values = max(0, image_values - change)
        print(f'value changed for the image menu, now {image_values}')
        display_image(image_values)
    elif current_display == 'settings':
        settings_index = (settings_index + change) % len(settings_options)
        print(f'Settings option changed to: {settings_options[settings_index]}')
        display_settings_option()
    elif current_display == 'playback':
        image_values = max(0, image_values - change)
        print(f'value changed for the playback menu, now {image_values}')
        display_image(image_values)

def display_settings_option():
    option = settings_options[settings_index]
    display_filler_text(screen, custom_font, f"Settings: {option}", text_color, bg_color)

def execute_settings_option():
    option = settings_options[settings_index]
    message = 'you should not see this'
    if option == 'Load WiFi Credentials, Must Reboot After':
        success = load_wifi_credentials()
        message = "WiFi Credentials Loaded Successfully" if success else "Failed to Load WiFi Credentials"
    elif option == 'Update Photo Rotation':
        update_rotation_value()
        print("Executing screen rotation")
        message = "Photos taken are now rotated 90 degrees clockwise"
    elif option == 'Option 3':
        print("Executing Option 3")
        message = "Option 3 Executed"
    elif option == 'Option 4':
        print("Executing Option 4")
        message = "Option 4 Executed"
    
    display_filler_text(screen, custom_font, message, text_color, bg_color)
    time.sleep(2)  # Display the message for 2 seconds
        
    display_settings_option()  # Return to settings display

def on_button_press(button):
    global current_display, screen, image_values, var1_index
    print(f'Button {button.pin.number} has been pressed')
    
    if button.pin.number == 16:  # Original button
        print("Original button pressed")
        if current_display == 'text':
            display_filler_text(screen, custom_font, "Taking Photo", text_color, bg_color)
            cam_sequence(var1_list[var1_index])
            display_image(0)
            image_values = 0
            current_display = 'image'
        elif current_display == 'settings':
            execute_settings_option()
        else:
            display_sentence()
            current_display = 'text'
            image_values = 0
    elif button.pin.number == 5:  # New 'settings' button
        print("Settings button pressed")
        if current_display != 'settings':
            current_display = 'settings'
            display_settings_option()
        else:
            current_display = 'text'
            display_sentence()
    elif button.pin.number == 6:  # New 'playback' button
        print("Playback button pressed")
        image_values = 0
        if current_display != 'image':
            current_display = 'image'
            display_image(image_values)
        else:
            current_display = 'text'
            display_sentence()
    
    print(f"Current display mode: {current_display}")

def load_wifi_credentials(file_path="/boot/WiFi Credentials/WiFi Credentials.txt"):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: Wi-Fi credentials file not found at {file_path}")
        return False

    try:
        # Read Wi-Fi credentials from the file
        with open(file_path, "r") as file:
            ssid = file.readline().strip()
            password = file.readline().strip()

        if not ssid or not password:
            print("Error: SSID and password are required")
            return False

        # Generate the hashed passphrase using wpa_passphrase
        result = subprocess.run(["wpa_passphrase", ssid, password], capture_output=True, text=True)

        # Extract the network block generated by wpa_passphrase
        network_config = ""
        inside_network_block = False
        for line in result.stdout.splitlines():
            if "network=" in line:
                inside_network_block = True
            if inside_network_block:
                network_config += line + "\n"
            if line == "}":
                inside_network_block = False

        # Path to wpa_supplicant.conf
        wpa_supplicant_path = "/etc/wpa_supplicant/wpa_supplicant.conf"

        # Check if we have write permissions
        if not os.access(wpa_supplicant_path, os.W_OK):
            print("Error: No write permission for wpa_supplicant.conf. Try running with sudo.")
            return False

        # Append the new network to wpa_supplicant.conf
        with open(wpa_supplicant_path, "a") as wpa_file:
            wpa_file.write(network_config)

        print(f"Wi-Fi credentials for '{ssid}' added successfully")

        # Reconfigure wpa_supplicant to apply changes
        subprocess.run(["wpa_cli", "-i", "wlan0", "reconfigure"], check=True)

        print("Wi-Fi configuration updated. The Pi will attempt to connect to the new network.")
        return True

    except Exception as e:
        print(f"Error loading Wi-Fi credentials: {str(e)}")
        return False

def load_ai_api_keys(file_path="/boot/API_keys/keys.txt"):
    # Initialize variables to store API keys
    astica_ai_key = None
    openai_key = None
    additional_keys = {}

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: API key file not found at {file_path}")
        return None, None, {}

    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip().lower()  # Convert to lowercase for case-insensitive comparison
                    value = value.strip()

                    if key == "astica ai key":
                        astica_ai_key = value
                    elif key == "openai key":
                        openai_key = value
                    else:
                        additional_keys[key] = value

        if not astica_ai_key or not openai_key:
            print("Error: Both Astica AI Key and OpenAI Key are required")
            return None, None, {}

        print("AI API keys loaded successfully")
        print(f"Astica AI Key: {astica_ai_key[:5]}...{astica_ai_key[-5:]}")
        print(f"OpenAI Key: {openai_key[:5]}...{openai_key[-5:]}")
        for key, value in additional_keys.items():
            print(f"{key}: {value[:5]}...{value[-5:]}")

        return astica_ai_key, openai_key

    except Exception as e:
        print(f"Error loading AI API keys: {str(e)}")
        return None, None, {}

def main():
    global custom_font, text_color, bg_color, current_display, values, ASTICA_API_KEY, OPENAI_API_KEY

    ASTICA_API_KEY, OPENAI_API_KEY = load_ai_api_keys()
    
    if ASTICA_API_KEY and OPENAI_API_KEY:
        print("AI API keys loaded successfully. Ready to use in main script.")
    else:
        print("Failed to load required AI API keys.")
        display_filler_text(screen, custom_font, "API KEYS NOT FOUND", text_color, bg_color)
        time.sleep(10)

    current_display = 'text'
    values = [0, 0]
    display_sentence()

    encoder_var1.when_rotated_clockwise = lambda: update_values(1)
    encoder_var1.when_rotated_counter_clockwise = lambda: update_values(-1)

    button_var1.when_pressed = lambda: on_button_press(button_var1)
    button_var2.when_pressed = lambda: on_button_press(button_var2)
    button_var3.when_pressed = lambda: on_button_press(button_var3)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

    button_var1.close()
    button_var2.close()
    button_var3.close()
    encoder_var1.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_thread = threading.Thread(target=main)
    main_thread.start()
