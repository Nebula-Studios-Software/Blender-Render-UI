# Blender Render UI

This project provides a user-friendly interface for rendering Blender files using command line arguments. The application allows users to construct Blender command line commands through a graphical user interface (GUI) and monitor the rendering process with real-time feedback.

## Features

- **Command Line Argument Builder**: Users can easily build and customize Blender command line arguments using the UI.
- **Progress Monitoring**: Visual feedback on the rendering progress is provided to keep users informed.
- **Output Log**: An integrated log viewer displays the output from the rendering process, helping users troubleshoot any issues.

## Project Structure

```
blender-render-ui
├── src
│   ├── main.py                # Entry point of the application
│   ├── ui                     # UI components
│   │   ├── __init__.py
│   │   ├── main_window.py      # Main application window
│   │   ├── command_builder.py   # Command line argument builder
│   │   ├── progress_monitor.py   # Progress monitoring
│   │   └── log_viewer.py       # Log viewer for output
│   ├── core                   # Core functionality
│   │   ├── __init__.py
│   │   ├── blender_executor.py  # Executes Blender commands
│   │   ├── command_generator.py  # Generates command strings
│   │   └── param_definitions.py  # Defines command line parameters
│   ├── utils                  # Utility functions
│   │   ├── __init__.py
│   │   └── logger.py           # Logging utilities
│   └── resources              # Resource files
│       └── __init__.py
├── requirements.txt           # Project dependencies
├── setup.py                   # Packaging configuration
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/blender-render-ui.git
   cd blender-render-ui
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

Follow the on-screen instructions to build your Blender command and start the rendering process.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.