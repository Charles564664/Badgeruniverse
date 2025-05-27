import os, threading, subprocess, webbrowser, random, sys
from flask import Flask, render_template_string, redirect, request
from datetime import datetime

app = Flask(__name__)
# TODO: These paths should be configurable (e.g., via environment variables or a config file)
UNITY_EXE = "C:/Program Files/Unity/Hub/Editor/2022.3.60f1/Editor/Unity.exe"
UNITY_PROJECT = "C:/Users/YourName/UnityProjects/BadGameStudio"
# TODO: Remember to replace 'YourName' in UNITY_PROJECT with your actual user name or make it configurable.
# TODO: Consider using a path relative to the script file for more predictable log location: LOG_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "AI_Assistant_Logs")
LOG_PATH = os.path.join(os.getcwd(), "AI_Assistant_Logs")
os.makedirs(LOG_PATH, exist_ok=True)

# List of Unity Editor methods to be called for different "surprise" builds.
SURPRISE_METHODS = [
    "AutoPrefabBuilder.BuildClicker",
    "AutoPrefabBuilder.BuildFlappyFish",
    "AutoPrefabBuilder.BuildMerge"
]

# Utility function to log messages with a timestamp.
def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Robustness: Try to write to log file, print to console if it fails.
    try:
        with open(os.path.join(LOG_PATH, "activity_log.txt"), "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {msg}\n")
    except Exception as e:
        print(f"CRITICAL: Failed to write to log file: {e}") # Fallback to console

# Flask route for the main page.
@app.route("/")
def index():
    logs = "(No activity yet)"
    # Robustness: Try to read log file, display error if it fails.
    try:
        if os.path.exists(os.path.join(LOG_PATH, "activity_log.txt")):
            with open(os.path.join(LOG_PATH, "activity_log.txt"), "r", encoding="utf-8") as f:
                logs = f.read()
    except Exception as e:
        logs = f"(Error reading log file: {e})"
    # HTML structure for the web interface.
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bad Game Studio</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #2b2b2b; color: #e0e0e0; line-height: 1.6; }
            .container { max-width: 800px; margin: auto; padding: 20px; background-color: #3c3c3c; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.5); }
            h1 { color: #00d1b2; text-align: center; }
            h2 { color: #00bfa5; border-bottom: 1px solid #00bfa5; padding-bottom: 5px; }
            .button-group { text-align: center; margin-bottom: 20px; }
            button { 
                padding: 12px 20px; margin: 8px; border: none; border-radius: 5px; 
                cursor: pointer; font-weight: bold; transition: background-color 0.3s ease;
            }
            button:hover { opacity: 0.9; }
            .surprise-btn { background-color: #00d1b2; color: #2b2b2b; }
            .surprise-btn:hover { background-color: #00bfa5; }
            .quit-btn { background-color: #ff3860; color: white; }
            .quit-btn:hover { background-color: #ff1f4f; }
            pre { 
                background-color: #2b2b2b; border: 1px solid #555; padding: 15px; 
                border-radius: 5px; white-space: pre-wrap; word-wrap: break-word; 
                max-height: 400px; overflow-y: auto; color: #d0d0d0; font-family: 'Courier New', Courier, monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 Bad Game Studio Dashboard</h1>
            <div class="button-group">
                <form method='post' action='/surprise' style='display:inline;'>
                    <button class='surprise-btn' type='submit'>✨ Surprise Me Game</button>
                </form>
                <form method='post' action='/quit' style='display:inline;'>
                    <button class='quit-btn' type='submit'>🛑 Quit Studio</button>
                </form>
            </div>
            <h2>📜 Activity Log</h2>
            <pre>{{ logs }}</pre>
        </div>
    </body>
    </html>
    """, logs=logs)

# Flask route to trigger a "surprise" game build.
@app.post("/surprise")
def build_surprise():
    # Runs the Unity build and launch logic in a separate thread to avoid blocking the web server.
    threading.Thread(target=surprise_me_task).start()
    return redirect("/")

# Flask route to quit the application.
@app.post("/quit")
def quit_app():
    # Attempt to gracefully shut down the Werkzeug development server.
    log("🛑 Quit button pressed. Attempting to shut down.")
    try:
        # This part is specific to Werkzeug and might not work in other WSGI servers.
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func is None:
            log('Werkzeug server shutdown function not found. Using sys.exit() as fallback.')
            sys.exit(0) # Exit the Python interpreter
        else:
            shutdown_func()
            log('🔌 Werkzeug server shutdown function called.')
    except Exception as e:
        log(f"Error during shutdown attempt: {e}. Forcing sys.exit().")
        sys.exit(0)
    # return "Server is shutting down..." # This line might not be reached or sent

# Main logic for building and launching a "surprise" Unity game.
def surprise_me_task():
    # Path Validation: Check if Unity executable exists before proceeding.
    if not os.path.exists(UNITY_EXE):
        log(f"CRITICAL: UNITY_EXE path not found: {UNITY_EXE}. Cannot start Unity process.")
        return

    # Surprise Method Selection: Choose a random method if available.
    if not SURPRISE_METHODS:
        log("ERROR: No surprise methods defined in SURPRISE_METHODS list.")
        return
    method = random.choice(SURPRISE_METHODS)
    log(f"🚀 Building with {method}")

    # Generate unique log file names for this specific Unity process invocation.
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    method_name_part = method.split('.')[-1] if '.' in method else method
    unity_build_log = os.path.join(LOG_PATH, f"unity_build_{method_name_part}_{timestamp_str}.txt")
    unity_launch_log = os.path.join(LOG_PATH, f"unity_launch_{method_name_part}_{timestamp_str}.txt")

    # Execute Unity in batch mode to build the project.
    try:
        log(f"Executing Unity build: {' '.join([UNITY_EXE, '-quit', '-batchmode', '-projectPath', UNITY_PROJECT, '-executeMethod', method, '-logFile', unity_build_log])}")
        build_process = subprocess.run([
            UNITY_EXE, "-quit", "-batchmode",
            "-projectPath", UNITY_PROJECT,
            "-executeMethod", method,
            "-logFile", unity_build_log
        ], capture_output=True, text=True, check=False, timeout=300) # Added timeout

        if build_process.returncode == 0:
            log(f"✅ Unity build for {method} completed successfully. Log: {unity_build_log}")
        else:
            log(f"⚠️ Unity build for {method} failed with code {build_process.returncode}. Log: {unity_build_log}")
            log(f"   Build STDOUT: {build_process.stdout[:500]}...") # Log snippet
            log(f"   Build STDERR: {build_process.stderr[:500]}...") # Log snippet
            return # Do not proceed to launch if build failed
    except subprocess.TimeoutExpired:
        log(f"⚠️ Unity build for {method} timed out after 300 seconds. Log: {unity_build_log}")
        return
    except FileNotFoundError: # This specific check might be redundant if the top-level UNITY_EXE check is solid.
        log(f"CRITICAL: Unity executable not found at {UNITY_EXE} when trying to run build for {method}.")
        return
    except Exception as e:
        log(f"💥 An unexpected error occurred during Unity build for {method}: {e}")
        return

    # Launch the Unity Editor to open the project (and potentially a specific scene).
    try:
        log(f"Attempting to launch Unity editor for project: {UNITY_PROJECT}. Log: {unity_launch_log}")
        launch_process = subprocess.Popen([
            UNITY_EXE,
            "-projectPath", UNITY_PROJECT,
            "-logFile", unity_launch_log
            # Consider adding: "-openScene", "Assets/Scenes/MainScene.unity"
        ])
        log(f"🚀 Unity editor launch process for {UNITY_PROJECT} initiated (PID: {launch_process.pid}). Monitor log: {unity_launch_log}")
    except FileNotFoundError:
        log(f"CRITICAL: Unity executable not found at {UNITY_EXE} when trying to launch project.")
    except Exception as e:
        log(f"💥 An unexpected error occurred during Unity editor launch: {e}")


# Main execution block when the script is run directly.
if __name__ == "__main__":
    # Initial check for Unity executable existence.
    if not os.path.exists(UNITY_EXE):
        # This message goes to console as logger might not be fully ready or path is an issue.
        print(f"WARNING: Unity executable not found at {UNITY_EXE}. The game building features will not work.")
        log(f"WARNING: Unity executable not found at {UNITY_EXE}.") # Also log it

    log("🟢 Bad Game Studio launched")
    webbrowser.open_new_tab("http://localhost:8080") # Opens in a new tab
    app.run(port=8080)
    # app.run(port=8080, debug=True) # Enable debug mode for development only
