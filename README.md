# AIeye

If you are interested in buying a kit for this fill out this form, if there are enough people I will make and sell kits:
https://forms.gle/SYHFhyDxsT9Xxbqz5
Main repository for the AIeye camera project.

## Supplies

### Parts List
| Name                           | Quantity | Total Price | Link                                                                                                          | Notes                                                                                                                                  |
|--------------------------------|----------|-------------|---------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| Raspberry Pi Zero 2W           | 1        | $26         | [Amazon](https://amzn.to/3Aza8KZ)                                                                             |                                                                                                                                        |
| Display                        | 1        | $18         | [Amazon](https://amzn.to/3WQWfPW)                                                                             |                                                                                                                                        |
| Camera                         | 1        | $9.50       | [Amazon](https://amzn.to/4cCxRY8)                                                                             |                                                                                                                                        |
| Camera Ribbon Cable            | 1        | $9          | [Amazon](https://amzn.to/3AAfSnO)                                                                             | You need this because the Pi Zero has a different ribbon cable than the regular Pi                                                     |
| Custom PCB                     | 1        | $9          | Recommend [PCBWay](https://www.pcbway.com/) or [JLCPCB](https://jlcpcb.com/)                                  | You will need to upload the PCB zip file to the respective website                                                                     |
| PCB Part - Button Power Switch | 1        | $1.85       | [Digi-Key](https://www.digikey.com/en/products/detail/cw-industries/GPTS203211B/3190590)                      |                                                                                                                                        |
| PCB Part - Rotary Encoder      | 1        | $2.60       | [Digi-Key](https://www.digikey.com/en/products/detail/cui-devices/RIC11-22S16D5M-TH/21705934)                 |                                                                                                                                        |
| PCB Part - Alternate Encoder   | *        | *           | [Digi-Key](https://www.digikey.com/en/products/detail/cui-devices/RIC11-22S15D7-TH/21705936)                  | Footprint should be the same for the PCB, but you may need to modify the 3D file for the knob so it fits on the shaft                  |
| PCB Part - Alternate Encoder   | *        | *           | [Digi-Key](https://www.digikey.com/en/products/detail/cui-devices/RIC11-22S13D5S-TH/21705929)                 | Footprint should be the same for the PCB, but you may need to modify the 3D file for the knob so it fits on the shaft                  |
| PCB Part - Voltage Converter   | 1        | $3.95       | [Digi-Key](https://www.digikey.com/en/products/detail/adafruit-industries-llc/4654/12697636)                  |                                                                                                                                        |
| PCB Part - Momentary Button    | 2        | $0.10       | [Digi-Key](https://www.digikey.com/en/products/detail/c-k/PTS636-SK43-LFS/10071716)                           |                                                                                                                                        |
| PCB Part - Female Battery Port | 1        | $0.12       | [Digi-Key](https://www.digikey.com/en/products/detail/jst-sales-america-inc/S2B-PH-K-S/926626)                |                                                                                                                                        |
| Battery                        | 1        | $10.95      | [Digi-Key](https://www.digikey.com/en/products/detail/sparkfun-electronics/PRT-18286/14302550)                |                                                                                                                                        |
| Battery Charger                | 1        | $10.96      | [Amazon](https://amzn.to/3yW2CcH)                                                                             |                                                                                                                                        |

**Total:** ~$102.03  
*Probably will cost 10-20% more with shipping included.*


---

### Other Needed Supplies

| Name                   | Quantity                           | Link                                        | Notes                                                                                                          |
|------------------------|------------------------------------|---------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| 3D Printed Parts       |                                    |                                             |                                                                                                                |
| M3 Screws              | 2 short (5-10mm), 2 long (15-25mm) |                                             | 3D file could be modified for similarly sized screws to fit                                                    |
| Super Glue or Hot Glue |                                    |                                             |                                                                                                                |
| Sandpaper              |                                    |                                             | If you want to improve the surface quality of the prints                                                       |
| Spray Paint            |                                    |                                             | If you are not using colored filament and want to change the surface finish                                    |
| Soldering Iron         |                                    | [Amazon](https://amzn.to/3Z03ozY)          | For making the circuit board                                                                                   |
| Wire                   |                                    |                                             | I used 24 ga, but similarly sized copper wire should work the same (solid core wire may be trickier to solder) |
| MicroSD Card           |                                    | [Amazon](https://amzn.to/4763LuP)          |                                                                                                                |
| SD Card Reader         |                                    |                                             | Some way to read the SD card                                                                                   |

---

### Recommended if You Need to Debug

- **Mini HDMI to HDMI Adapter**
- **Micro USB OTG Adapter**
- **Mouse**
- **Keyboard**

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
- **Soldering Components**: Start by soldering the through-hole components to the board. These are highlighted below. Note how the voltage regulator is mounted slightly off the board. The orientation of the buttons does not matter. Just make sure all the components are soldered to the front side of the board (the side with the text on it).
  
  ![image](https://github.com/user-attachments/assets/10cb776f-fcab-41f9-949a-a0fc67d0b0cc)
  ![image](https://github.com/user-attachments/assets/566008aa-e590-450a-a54b-4e741cc798be)
  
- **Battery Cord**: Solder wires to the female battery port, and use plenty of shrink wrap to avoid short circuits. When soldering it onto the board, ensure that when the battery is plugged in, the ground goes to the ground pad (the square one). These connectors are easy to mix up and wire backward. It won't damage the device, but if you wire the positive and gnd backwards it will not turn on. The side of the board you solder it to doesn't matter as long as ground goes to ground (square pad). Below is a close-up of the battery connection:
  
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
    - https://drive.google.com/drive/folders/1noxVPlFzV9c3eGpXCnVfaX7x1-svAIYr?usp=sharing
  - Within win32diskimager, select your SD card, then select your downloaded image and click write. This process can take 10-30 minutes.
  
- **Configuring the SD Card**:
  - Once the image is flashed, remove the SD card and reinsert it into your computer.
  - Open the drive from your computor, and you should see a few folders. Many of the files are folders that the Raspberry Pi will rely on when it boots.
  - There should be a folder called `wifi credentials`, edit the text file and replace the credentials with the wifi credentials you wish the camera to use.
    - You can add your home Wi-Fi later, but not at this point.
    - You can make these credentials your mobile hotspot so you can take the camera outside your house. If you don’t want it to leave your house, just add your home Wi-Fi.
    - You can replace these credentials with a second or third Wi-Fi network once you've booted up the camera and loaded them into memory, which I'll cover later.
    - Be warned mobile hotspots can be annoying to connect to from the Pi, in my experience my Iphone hotspot was far less reliable than my home wifi.
  - Notice the folder called the photos, you dont need to do anything with it now but this is where the photos are going to be saved to so if you want to take the photos off the camera then that's where you get them.
    
- **API Keys**:
  - In the folder labeled `API keys`, you'll need to enter two API keys: one for Astica and one for OpenAI. You only need to input the keys once; the program will pull from that file every time it runs.
    - To get the Astica API key, go to [Astica AI](https://astica.ai/).
    - You'll need to add funds to Vision Compute. I recommend adding $10. Each image costs roughly $0.03 for Astica and OpenAI, so about $0.06 per image.
    - For the OpenAI key, go to [OpenAI Platform](https://platform.openai.com/settings/profile?tab=api-keys).
    - You'll need to create a user API key, which is now considered legacy. I recommend adding $10 to it as well.
    
- **Final Steps**:
  - Once you’ve added the API keys to the text file, you should be all set! Plug in the battery and power it on with the large button.
  - Once fully booted, press the middle button to open the settings menu, then press the knob to load the Wi-Fi settings. If you find that the camera is taking photos that are 90° or 180° off, go to the second menu in the settings and click rotate 90 degrees.
  - If you want to get the photos off of the pi then remove the sd card, plug it in your computor, and all the photos should be in the folder called photos.

- **Controls:**
  - When the "a normal photo" screen is being displayed this is the home screen, press the knob in to take a photo. Rotate the knob to change what the descriptor is for the photo you are taking.
  - Leftmost button is the power switch, you will need to press it more than the other 2 buttons to get it to click.
  - Middle button is settings
    - Once in the settings twist the know to navigate to which setting you want to do. When you press the knob in it will load the setting. 
  - Right button is playback. Press it and you will be able to see all the photos you have already taken. Press it again to go back to the screen with the descriptor sentence where you can take the photo.
  ![image](https://github.com/user-attachments/assets/53c2d7cb-7436-41ae-9751-9fed7f31024c)

## Debugging

- **Troubleshooting**:
  - If something isn’t working, you'll need to connect to the Pi directly. You can do this by opening the bottom and plugging a mini HDMI cable and keyboard into the Pi. Alternatively, you can connect to the Pi via VNC Viewer. Note that you will not be able to connect to the Pi via VNC Viewer if it isn’t connected to the internet.
  - once you connect to the pi via vnc viewer you will need to press the escape key to ente the desktop
  - I have also included an image for the camera where the drivers to make it fit to the screen are not included. This may be easier to modify code as the screen will not be small on the VNC viewer.
  - You should also use this if you want to upgrade the screen.
  - If you want to run the script without booting on the entire camera, you are going to need to go to the terminal and run the command: sudo -E python3 cam_v3.py
