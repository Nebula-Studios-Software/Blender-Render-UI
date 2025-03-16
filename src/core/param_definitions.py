class ParamDefinitions:
    """
    Definizioni complete dei parametri della linea di comando di Blender 4.0+
    Organizzati per categoria e con ordine definito
    """
    
    # Dizionario che mappa i parametri al loro ordine di priorità
    PARAM_ORDER = {
        "-b": 0,            # --background (sempre per primo)
        "-E": 1,           # --engine (subito dopo il file .blend)
        "--cycles-device": 2,  # device per cycles
        "-F": 3,           # --render-format
        "-o": 4,           # --render-output
        "-f": 5,           # --render-frame
        "-e": 5,           # --frame-end (stessa priorità di -f perché non possono coesistere)
        "-s": 6,           # --frame-start
        "-a": 7,           # --render-anim (sempre dopo i frame parameters)
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
    
    # Parametri di base
    BACKGROUND = "-b"
    PYTHON = "-P"
    PYTHON_EXPR = "--python-expr"
    PYTHON_EXIT = "--python-exit-code"
    HELP = "--help"
    VERSION = "--version"
    
    # Parametri di rendering
    RENDER = "-a"
    RENDER_FRAME = "-f"
    RENDER_OUTPUT = "-o"
    SCENE = "-S"
    ENGINE = "-E"
    
    # Parametri per i file
    FILE = "--"
    ADDONS = "--addons"
    
    # Parametri per il formato e la risoluzione
    FORMAT = "-F"
    USE_EXTENSION = "-x"
    RESOLUTION_X = "--resolution-x"  # Aggiunto
    RESOLUTION_Y = "--resolution-y"  # Aggiunto
    RESOLUTION_PERCENTAGE = "--resolution-percentage"
    
    # Parametri per i frame
    FRAME_START = "-s"
    FRAME_END = "-e"
    FRAME_JUMP = "-j"
    
    # Parametri Cycles
    CYCLES_DEVICE = "--cycles-device"
    CYCLES_PRINT_STATS = "--cycles-print-stats"
    CYCLES_SAMPLES = "--cycles-samples"  # Aggiunto
    
    # Parametri per thread e performance
    THREADS = "-t"
    
    # Parametri di vista
    WINDOW_BORDER = "-w"
    WINDOW_FULLSCREEN = "-W"
    WINDOW_GEOMETRY = "-p"
    WINDOW_MAXIMIZED = "-M"
    
    # Parametri di avvio
    START_CONSOLE = "-con"
    NO_NATIVE_PIXELS = "--no-native-pixels"
    NO_WINDOW_FOCUS = "--no-window-focus"
    ENABLE_AUTOEXEC = "-y"
    DISABLE_AUTOEXEC = "-Y"
    FACTORY_STARTUP = "--factory-startup"

    # Parametri di debug
    DEBUG = "-d"
    DEBUG_MEMORY = "--debug-memory"
    DEBUG_CYCLES = "--debug-cycles"
    
    @staticmethod
    def get_param_order(param):
        """Restituisce l'ordine di priorità di un parametro"""
        return ParamDefinitions.PARAM_ORDER.get(param, 999)  # Parametri sconosciuti alla fine

    @staticmethod
    def get_categories():
        """Restituisce i parametri organizzati per categoria per l'interfaccia utente"""
        return {
            "Base": [
                {"name": "Background", "param": ParamDefinitions.BACKGROUND, "type": "bool", 
                 "description": "Esegui Blender in modalità headless (senza interfaccia grafica)"},
                {"name": "Python Script", "param": ParamDefinitions.PYTHON, "type": "file", 
                 "description": "Esegui uno script Python"},
                {"name": "Python Expression", "param": ParamDefinitions.PYTHON_EXPR, "type": "string", 
                 "description": "Esegui un'espressione Python"},
                {"name": "Help", "param": ParamDefinitions.HELP, "type": "bool", 
                 "description": "Mostra l'help della linea di comando"},
                {"name": "Version", "param": ParamDefinitions.VERSION, "type": "bool", 
                 "description": "Mostra la versione di Blender"}
            ],
            "File": [
                {"name": "Blend File", "param": ParamDefinitions.FILE, "type": "file", 
                 "description": "File .blend da aprire"},
                {"name": "Addons", "param": ParamDefinitions.ADDONS, "type": "string", 
                 "description": "Lista di addon da abilitare, separati da virgola"}
            ],
            "Rendering": [
                {"name": "Render Animation", "param": ParamDefinitions.RENDER, "type": "bool", 
                 "description": "Rendi l'animazione completa"},
                {"name": "Render Frame", "param": ParamDefinitions.RENDER_FRAME, "type": "string", 
                 "description": "Rendi specifici frame (es. '1,3,5-10')"},
                {"name": "Output Path", "param": ParamDefinitions.RENDER_OUTPUT, "type": "path", 
                 "description": "Percorso per i file di output"},
                {"name": "Scene", "param": ParamDefinitions.SCENE, "type": "string", 
                 "description": "Nome della scena da renderizzare"},
                {"name": "Engine", "param": ParamDefinitions.ENGINE, "type": "enum", 
                 "options": ["CYCLES", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"], 
                 "description": "Motore di rendering da utilizzare"}
            ],
            "Format": [
                {"name": "Format", "param": ParamDefinitions.FORMAT, "type": "enum", 
                 "options": ["PNG", "JPEG", "OPEN_EXR", "TIFF", "WEBP", "FFMPEG"], 
                 "description": "Formato dei file di output"},
                {"name": "Resolution X", "param": ParamDefinitions.RESOLUTION_X, "type": "int", 
                 "description": "Larghezza in pixel dell'immagine renderizzata"},
                {"name": "Resolution Y", "param": ParamDefinitions.RESOLUTION_Y, "type": "int", 
                 "description": "Altezza in pixel dell'immagine renderizzata"},
                {"name": "Resolution %", "param": ParamDefinitions.RESOLUTION_PERCENTAGE, "type": "int", 
                 "description": "Percentuale della risoluzione (1-100)"}
            ],
            "Frames": [
                {"name": "Start Frame", "param": ParamDefinitions.FRAME_START, "type": "int", 
                 "description": "Frame iniziale dell'animazione"},
                {"name": "End Frame", "param": ParamDefinitions.FRAME_END, "type": "int", 
                 "description": "Frame finale dell'animazione"},
                {"name": "Frame Jump", "param": ParamDefinitions.FRAME_JUMP, "type": "int", 
                 "description": "Numero di frame da saltare tra i render"}
            ],
            "Cycles": [
                {"name": "Device", "param": ParamDefinitions.CYCLES_DEVICE, "type": "enum", 
                 "options": ["CPU", "CUDA", "OPTIX", "HIP", "METAL", "ONEAPI"], 
                 "description": "Dispositivo di calcolo per Cycles"},
                {"name": "Samples", "param": ParamDefinitions.CYCLES_SAMPLES, "type": "int", 
                 "description": "Numero di campioni per il rendering"}
            ],
            "Performance": [
                {"name": "Threads", "param": ParamDefinitions.THREADS, "type": "int", 
                 "description": "Numero di thread per il rendering (0=auto)"}
            ],
            "Debug": [
                {"name": "Debug", "param": ParamDefinitions.DEBUG, "type": "bool", 
                 "description": "Abilita modalità debug"},
                {"name": "Debug Memory", "param": ParamDefinitions.DEBUG_MEMORY, "type": "bool", 
                 "description": "Mostra informazioni sull'uso della memoria"},
                {"name": "Debug Cycles", "param": ParamDefinitions.DEBUG_CYCLES, "type": "bool", 
                 "description": "Abilita debug per Cycles"}
            ],
            "Avanzate": [
                {"name": "Window Geometry", "param": ParamDefinitions.WINDOW_GEOMETRY, "type": "string", 
                 "description": "Posizione e dimensione finestra (X,Y,W,H)"},
                {"name": "Factory Startup", "param": ParamDefinitions.FACTORY_STARTUP, "type": "bool", 
                 "description": "Usa le impostazioni di fabbrica"},
                {"name": "Enable Autoexec", "param": ParamDefinitions.ENABLE_AUTOEXEC, "type": "bool", 
                 "description": "Abilita auto-esecuzione degli script Python"},
                {"name": "Disable Autoexec", "param": ParamDefinitions.DISABLE_AUTOEXEC, "type": "bool", 
                 "description": "Disabilita auto-esecuzione degli script Python"}
            ]
        }
        
    @staticmethod
    def get_all_parameters():
        """Restituisce una lista piatta di tutti i parametri disponibili"""
        all_params = []
        for category in ParamDefinitions.get_categories().values():
            for param in category:
                all_params.append(param)
        return all_params