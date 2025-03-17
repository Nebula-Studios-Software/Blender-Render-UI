# Blender Render UI

Built with ❤️ by Nebula Studios Software

This project provides a user-friendly interface for rendering Blender files using command line arguments. The application allows users to construct Blender command line commands through a graphical user interface (GUI) and monitor the rendering process with real-time feedback.

## Features

- **Command Line Argument Builder**: Users can easily build and customize Blender command line arguments using the UI.
- **Preset System**: Save your settings for later use or share it with other people
- **Render Settings**: The application provides a variety of settings for rendering, such as resolution, frame range, and output file format.
- **Output Directory**: Users can specify the output directory for the rendered files.
- **Automatic Argument ordering**: The application automatically orders the command line arguments to ensure the correct rendering process.
- **Progress Monitoring**: Visual feedback on the rendering progress is provided to keep users informed.
- **Output Log**: An integrated log viewer displays the output from the rendering process, helping users troubleshoot any issues.

## Installation

## Executable file

Download the latest release from the [Releases](https://github.com/Nebula-Studios-Software/Blender-Render-UI/releases/) page and start the executable.

## Manual Installation

1. Clone the repository:
   ```
   git clone https://github.com/Nebula-Studios-Software/Blender-Render-UI/
   cd blender-render-ui
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```
   Or build the executable:
   ```
   python build.py
   ```
   The executable will be located in the `dist` folder.

## Usage

1. Open the Blender Render UI application.
2. Click the `Browse` button to select the Blender executable if it is not automatically detected.
3. Tune the rendering settings to your liking.
4. Click the `Render` button to start the rendering process.

# Preset sharing and manual editing
You can find the preset file in your %appdata% folder (Roaming). Search for the "BlenderRenderUI" folder and share / modify the presets.json file

# Uninstalling
1. Delete the executable
2. Go to your %appdata% folder (Roaming) and delete the "BlenderRenderUI" folder

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
