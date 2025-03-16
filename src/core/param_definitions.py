class ParamDefinitions:
    """
    Complete definitions of Blender 4.0+ command line parameters
    Organized by category with defined order
    """
    
    # Dictionary mapping parameters to their priority order
    PARAM_ORDER = {
        "-b": 0,            # --background (always first)
        "-E": 1,           # --engine (right after the .blend file)
        "-F": 3,           # --render-format
        "-o": 4,           # --render-output
        "-f": 5,           # --render-frame
        "-e": 5,           # --frame-end (same priority as -f because they cannot coexist)
        "-s": 6,           # --frame-start
        "-a": 7,           # --render-anim (always after frame parameters)
        "-S": 8,           # --scene
        "-j": 9,           # --frame-jump
        "-x": 10,          # --use-extension
        "-w": 11,          # --window-border
        "-W": 12,          # --window-fullscreen
        "-p": 13,          # --window-geometry
        "-M": 14,          # --window-maximized
        "-con": 15,        # --start-console
        "--no-native-pixels": 16,
        "--no-window-focus": 17,
        "-y": 18,          # --enable-autoexec
        "-Y": 19,          # --disable-autoexec
        "-P": 20,          # --python
        "--python-text": 21,
        "--python-expr": 22,
        "--python-console": 23,
        "--python-exit-code": 24,
        "--python-use-system-env": 25,
        "--addons": 26,
        "--factory-startup": 27,
        "--resolution-x": 28,
        "--resolution-y": 29,
        "-d": 30,           # --debug
        "--debug-memory": 31,
        "--debug-cycles": 32
    }
    
    # Basic parameters
    BACKGROUND = "-b"
    PYTHON = "-P"
    PYTHON_EXPR = "--python-expr"
    PYTHON_EXIT = "--python-exit-code"
    HELP = "--help"
    VERSION = "--version"
    
    # Rendering parameters
    RENDER = "-a"
    RENDER_FRAME = "-f"
    RENDER_OUTPUT = "-o"
    SCENE = "-S"
    ENGINE = "-E"
    
    # File parameters
    FILE = "--"
    ADDONS = "--addons"
    
    # Format and resolution parameters
    FORMAT = "-F"
    USE_EXTENSION = "-x"
    RESOLUTION_X = "--resolution-x"  # Added
    RESOLUTION_Y = "--resolution-y"  # Added
    RESOLUTION_PERCENTAGE = "--resolution-percentage"
    
    # Frame parameters
    FRAME_START = "-s"
    FRAME_END = "-e"
    FRAME_JUMP = "-j"
    
    # Cycles parameters
    CYCLES_PRINT_STATS = "--cycles-print-stats"
    CYCLES_SAMPLES = "--cycles-samples"  # Added
    
    # Thread and performance parameters
    THREADS = "-t"
    
    # View parameters
    WINDOW_BORDER = "-w"
    WINDOW_FULLSCREEN = "-W"
    WINDOW_GEOMETRY = "-p"
    WINDOW_MAXIMIZED = "-M"
    
    # Startup parameters
    START_CONSOLE = "-con"
    NO_NATIVE_PIXELS = "--no-native-pixels"
    NO_WINDOW_FOCUS = "--no-window-focus"
    ENABLE_AUTOEXEC = "-y"
    DISABLE_AUTOEXEC = "-Y"
    FACTORY_STARTUP = "--factory-startup"

    # Debug parameters
    DEBUG = "-d"
    DEBUG_MEMORY = "--debug-memory"
    DEBUG_CYCLES = "--debug-cycles"
    
    @staticmethod
    def get_param_order(param):
        """Returns the priority order of a parameter"""
        return ParamDefinitions.PARAM_ORDER.get(param, 999)  # Unknown parameters at the end

    @staticmethod
    def get_categories():
        """Returns parameters organized by category for the user interface"""
        return {
            "Base": [
                {"name": "Background", "param": ParamDefinitions.BACKGROUND, "type": "bool", 
                 "description": "Run Blender in headless mode (without GUI)"},
                {"name": "Python Script", "param": ParamDefinitions.PYTHON, "type": "file", 
                 "description": "Execute a Python script"},
                {"name": "Python Expression", "param": ParamDefinitions.PYTHON_EXPR, "type": "string", 
                 "description": "Execute a Python expression"},
                {"name": "Help", "param": ParamDefinitions.HELP, "type": "bool", 
                 "description": "Show command line help"},
                {"name": "Version", "param": ParamDefinitions.VERSION, "type": "bool", 
                 "description": "Show Blender version"}
            ],
            "File": [
                {"name": "Blend File", "param": ParamDefinitions.FILE, "type": "file", 
                 "description": "Blend file to open"},
                {"name": "Addons", "param": ParamDefinitions.ADDONS, "type": "string", 
                 "description": "List of addons to enable, comma separated"}
            ],
            "Rendering": [
                {"name": "Render Animation", "param": ParamDefinitions.RENDER, "type": "bool", 
                 "description": "Render the complete animation"},
                {"name": "Render Frame", "param": ParamDefinitions.RENDER_FRAME, "type": "string", 
                 "description": "Render specific frames (e.g. '1,3,5-10')"},
                {"name": "Output Path", "param": ParamDefinitions.RENDER_OUTPUT, "type": "path", 
                 "description": "Path for output files"},
                {"name": "Scene", "param": ParamDefinitions.SCENE, "type": "string", 
                 "description": "Scene name to render"},
                {"name": "Engine", "param": ParamDefinitions.ENGINE, "type": "enum", 
                 "options": ["CYCLES", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"], 
                 "description": "Render engine to use"}
            ],
            "Format": [
                {"name": "Format", "param": ParamDefinitions.FORMAT, "type": "enum", 
                 "options": ["PNG", "JPEG", "OPEN_EXR", "TIFF", "WEBP", "FFMPEG"], 
                 "description": "Output file format"},
                {"name": "Resolution X", "param": ParamDefinitions.RESOLUTION_X, "type": "int", 
                 "description": "Rendered image width in pixels"},
                {"name": "Resolution Y", "param": ParamDefinitions.RESOLUTION_Y, "type": "int", 
                 "description": "Rendered image height in pixels"},
                {"name": "Resolution %", "param": ParamDefinitions.RESOLUTION_PERCENTAGE, "type": "int", 
                 "description": "Resolution percentage (1-100)"}
            ],
            "Frames": [
                {"name": "Start Frame", "param": ParamDefinitions.FRAME_START, "type": "int", 
                 "description": "Start frame of animation"},
                {"name": "End Frame", "param": ParamDefinitions.FRAME_END, "type": "int", 
                 "description": "End frame of animation"},
                {"name": "Frame Jump", "param": ParamDefinitions.FRAME_JUMP, "type": "int", 
                 "description": "Number of frames to skip between renders"}
            ],
            "Cycles": [
                {"name": "Samples", "param": ParamDefinitions.CYCLES_SAMPLES, "type": "int", 
                 "description": "Number of samples for rendering"}
            ],
            "Performance": [
                {"name": "Threads", "param": ParamDefinitions.THREADS, "type": "int", 
                 "description": "Number of threads for rendering (0=auto)"}
            ],
            "Debug": [
                {"name": "Debug", "param": ParamDefinitions.DEBUG, "type": "bool", 
                 "description": "Enable debug mode"},
                {"name": "Debug Memory", "param": ParamDefinitions.DEBUG_MEMORY, "type": "bool", 
                 "description": "Show memory usage information"},
                {"name": "Debug Cycles", "param": ParamDefinitions.DEBUG_CYCLES, "type": "bool", 
                 "description": "Enable Cycles debug"}
            ],
            "Advanced": [
                {"name": "Window Geometry", "param": ParamDefinitions.WINDOW_GEOMETRY, "type": "string", 
                 "description": "Window position and size (X,Y,W,H)"},
                {"name": "Factory Startup", "param": ParamDefinitions.FACTORY_STARTUP, "type": "bool", 
                 "description": "Use factory settings"},
                {"name": "Enable Autoexec", "param": ParamDefinitions.ENABLE_AUTOEXEC, "type": "bool", 
                 "description": "Enable Python scripts auto-execution"},
                {"name": "Disable Autoexec", "param": ParamDefinitions.DISABLE_AUTOEXEC, "type": "bool", 
                 "description": "Disable Python scripts auto-execution"}
            ]
        }
        
    @staticmethod
    def get_all_parameters():
        """Returns a flat list of all available parameters"""
        all_params = []
        for category in ParamDefinitions.get_categories().values():
            for param in category:
                all_params.append(param)
        return all_params