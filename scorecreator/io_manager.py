import os
import pickle
import datetime
from music21 import stream, converter
from scorecreator.project_paths import project_path, log_path, ensure_project_dir

def save_project(score: stream.Score):
    ensure_project_dir()

    print("\n--- Save Project ---")
    filename = input("Enter a filename (e.g., song.xml or song.m21data): ").strip()

    if not filename:
        print("A filename is required.")
        return
    
    save_user_input(f"Save project filename: {filename}")
    path = project_path(filename)

    try:
        if filename.endswith(".xml"):
            score.write("musicxml", fp=path)
            print(f"Project saed as MusicXML: {path}")
        elif filename.endswith(".m21data"):
            with open(path, "wb") as f:
                pickle.dump(score, f)
            print(f"Project saved in legacy format: {path}")
        else:
            print("Unsupported file type. Use .xml or .m21data.")
    except Exception as e:
        print(f"Error saving project: {e}")

def load_project(filename: str) -> stream.Score:

    ensure_project_dir()
    path = project_path(filename)

    try:
        if not os.path.exists(path):
            print(f"File not found: {filename}")
            return stream.Score()
        
        if filename.endswith(".m21data"):
            with open(path, "rb") as f:
                score = pickle.load(f)
            print(f"Loaded legacy project: {filename}")
            return score
        
        elif filename.endswith(".xml"):
            score = converter.parse(path)
            print(f"Loaded MusicXML project: {filename}")
            return score
        
        else:
            print("Unsupported file type. Use .xml or .m21data.")
            return stream.Score()
        
    except Exception as e:
        print(f"Error loading project: {e}")
        return stream.Score()

def save_user_input(user_input: str):

    ensure_project_dir()
    path = log_path()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(path, "a") as f:
            f.write(f"{timestamp} | {user_input}\n")
    except Exception as e:
        print(f"Failed to write to log file: {e}")

def start_new_session_log():
    ensure_project_dir()
    path = log_path()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n--- New Session Started at {timestamp} ---\n")

def list_saved_projects():
    project_paths.ensure_project_dir()
    project_dir = project_paths.get_project_dir()
    try:
        files [f for f in os.listdir(project_dir) if f.endswith((".xml", ".m21data"))]
        return sorted(files)
    except Exception as e:
        print(f"Error listing projects: {e}")
        return []