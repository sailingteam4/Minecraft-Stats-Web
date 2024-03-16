# Minecraft Stats to Web !

This is a Python Flask application that allows users to upload zip files of their minecraft world to a server. The application checks if the uploaded file is a zip file and saves it to a secure location, then extracts the zip file and reads the stats file of each player to get the stats. The stats are then displayed on a webpage.

## Prerequisites

- Python 3.6 or higher
- Flask
- Mojang API

## Installation

1. Clone the repository
```bash
git clone https://github.com/sailingteam4/Minecraft-Stats-Web.git
```
2. Install the required packages (you can use a virtual environment if you want to keep the packages separate from your system's packages)
```bash
pip install -r requirements.txt
```
3. Run the application
```bash
flask --app main run
```

## Usage

1. Open the web browser and go to the URL given by the flask application
2. Click on the "Choose File" button and select the zip file of your minecraft world
3. Click on the "Upload" button
4. Wait for the application to process the file
5. Choose the player from the dropdown list to see the stats

## Contributing

I am currently looking to improve the application not in the backend but in the frontend because for now it is very basic. If you have any ideas on how to improve the application, feel free to open an issue or a pull request.

## Contact 

If you have any questions or suggestions, feel free to contact me at [my email](mailto:sailing4team@gmail.com)
Or you can contact me on @nathan_nrg4