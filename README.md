# aieye

Main repository for the AIeye camera project.

## 3D Printing

- **Layer Height**: 0.2mm
- **Infill**: 10%
- **Printer**: Printed on an Ender 3 S1 (any FDM printer will suffice).
- **Material**: PLA+
- **Supports**: The only parts that require supports are the overhangs above the screen and button panel. I'm using organic supports and forcing the slicer to only generate supports in these areas using the painted support enforcer tool.
- **Orientation**: Some parts are designed to be printed in a specific orientation. Refer to the image below for correct orientations:
  
  ![image](https://github.com/user-attachments/assets/b0c4cffd-cedf-47da-8693-62824eec4426)

## Circuit Board

- **PCB Fabrication**: You'll need to get a custom PCB fabricated; I recommend using PCBway.
- **Soldering Components**: Start by soldering the through-hole components to the board. These are highlighted below. Note how the voltage regulator is mounted slightly off the board. The orientation of the buttons does not matter (ensure the power switch button is right side up).
  
  ![image](https://github.com/user-attachments/assets/10cb776f-fcab-41f9-949a-a0fc67d0b0cc)
  ![image](https://github.com/user-attachments/assets/566008aa-e590-450a-a54b-4e741cc798be)
  
- **Battery Cord**: Solder wires to the female battery port, and use plenty of shrink wrap to avoid short circuits. When soldering it onto the board, ensure that when the battery is plugged in, the ground goes to the ground pad (the square one). These connectors are easy to mix up and wire backward. It won't damage the device, but it is annoying to fix. The side of the board you solder it to doesn't matter as long as ground goes to ground. Below is a close-up of the battery connection:
  
  ![image](https://github.com/user-attachments/assets/d1d1fd2b-0103-4604-a646-6cf41c7d7d96)
  ![image](https://github.com/user-attachments/assets/fd3076cb-f38c-41bd-a451-e512cd0d14aa)

- **5V Connection**: Solder the 5V connection wire to the board. This is soldered on the underside of the board to avoid short circuits if the solder joint faces directly towards the board.
- **Camera Ribbon Cable**: Connect the camera ribbon cable carefully. The port on the Pi is delicate, and if you don't push the plastic piece directly in or out, it can snap off easily.
- **Header Pins**: Solder the header pins onto the Pi and then solder the board onto the Pi. In the image, you’ll see two damaged, dusty pins. These were unnecessary and have been removed from the PCB fab file. The blackboard should connect as far to the right as possible with all of the Pi's header pins still going through the board.
- **5V Connection to Pi**: Solder the 5V connection cord to the back of the Pi. It needs to connect to the 5V pin on the back, not the front, to avoid interference with the screen.
  
  ![image](https://github.com/user-attachments/assets/4f64a8b2-d54a-4e46-8e3b-8aa95abc94b0)
  
- **Screen Connection**: Press the screen onto the header pins. It should be on the far left of the pins.
  
  ![image](https://github.com/user-attachments/assets/363d26ef-4f77-4583-9230-2a06c414c3e7)

- **Testing**: Before placing it in the enclosure, test to ensure everything is working correctly.

## Software/Code

- **Overview**:
  - The project runs on PIOS, which is a slow but functional operating system. It takes a long time to boot up.
  - Once booted, it runs a Python script that displays the camera's GUI using a library called Pygame.

- **Flashing the SD Card**:
  - Use [win32diskimager](https://sourceforge.net/projects/win32diskimager/) to flash the SD card with the camera's code.
  - Download win32diskimager.
  - Download the `.img` file from my repository.
  - Within win32diskimager, select your SD card, then select your downloaded image and click write. This process can take 10-30 minutes.
  
- **Configuring the SD Card**:
  - Once the image is flashed, remove the SD card and reinsert it into your computer.
  - Open the drive, and you should see a few folders.
  - In the folder called `wifi credentials`, edit the text file and replace the credentials with your mobile hotspot credentials.
    - You can add your home Wi-Fi later, but not at this point.
    - I recommend using a mobile hotspot so you can take the camera outside your house. If you don’t want it to leave your house, just add your home Wi-Fi. You can replace these credentials with a new Wi-Fi network once you've booted up the camera and loaded them into memory, which I'll cover later.
    
- **API Keys**:
  - In the folder labeled `API keys`, you'll need to enter two API keys: one for Astica and one for OpenAI. You only need to input the keys once; the program will pull from that file every time it runs.
    - To get the Astica API key, go to [Astica AI](https://astica.ai/).
    - You'll need to add funds to Vision Compute. I recommend adding $10. Each image costs roughly $0.03 for Astica and OpenAI, so about $0.06 per image.
    - For the OpenAI key, go to [OpenAI Platform](https://platform.openai.com/settings/profile?tab=api-keys).
    - You'll need to create a user API key, which is now considered legacy. I recommend adding $10 to it as well.
    
- **Final Steps**:
  - Once you’ve added the API keys to the text file, you should be all set! Plug in the battery and power it on with the large button.
  - Once fully booted, press the middle button to open the settings menu, then press the knob to load the Wi-Fi settings. If you find that the camera is taking photos that are 90° or 180° off, go to the second menu in the settings and click rotate 90 degrees.
  - If you want to export the images from the camera, then take the SD card out and put it in your comptor. Navigate to the photos file on the card and they should all be there.

## Debugging

- **Troubleshooting**:
  - If something isn’t working, you'll need to connect to the Pi directly. You can do this by opening the bottom and plugging a mini HDMI cable and keyboard into the Pi. Alternatively, you can connect to the Pi via VNC Viewer. Note that you will not be able to connect to the Pi via VNC Viewer if it isn’t connected to the internet.
  - I have also included an image for the camera where the drivers to make it fit to the screen are not included. This may be easier to modify code as the screen will not be small on the VNC viewer.
    - You should also use this if you want to upgrade the screen.
