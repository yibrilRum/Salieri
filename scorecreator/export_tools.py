import os
from music21 import stream, converter
from scorecreator import io_manager, project_paths
import pickle

def show_score(score: stream.Score):
    print("\n--- Display Score ---")
    print("1. Text view (console notation summary)")
    print("2. Open in MuseScore or default viewer")
    choice = input("Choose display mode (1 or 2): ").strip()
    io_manager.save_user_input(f"Display choice: {choice}")

    if choice == "1":
        try:
            score.show("text")
        except Exception as e:
            print(f"Error displaying score as text: {e}")
    elif choice == "2":
        try:
            score.show()
        except Exception as e:
            print(f"Error opening score: {e}")
    else:
        print("Invalid choice.")

def save_project(score: stream.Score):
    print("\n--- Save Project ---")
    filename = input("Enter filename (e.g., piece.m21data or piece.xml): ").strip()
    if not filename:
        print("Save cancelled (no filename given).")
        return
    
    io_manager.save_user_input(f"Save project filename: {filename}")
    path = project_paths.project_path(filename)

    try:
        if filename.endswith(".xml"):
            score.write("musicxml", fp=path)
            print(f"Saved as MusicXML: {path}")
        elif filename.endswith(".m21data"):
            with open(path, "wb") as f:
                pickle.dump(score, f)
            print(f"Saved as binary project: {path}")
        else:
            print("Unsupported format. Use .xml or .m21data")
    except Exception as e:
        print(f"Error saving project: {e}")

def export_musicxml(score: stream.Score):
    print("\n--- Export to MusicXML ---")
    filename = input("Enter filename (e.g., score.xml): ").strip()
    io_manager.save_user_input(f"Export XML filename: {filename}")

    if not filename:
        print("Export cancelled.")
        return
    
    path = project_paths.project_path(filename)
    try:
        score.write("musicxml", fp=path)
        print(f"Exported MusicXML file: {path}")
    except Exception as e:
        print(f"Error exporting MusicXML: {e}")

def export_midi(score: stream.Score):
    print("\n--- MIDI Tools ---")
    print("1. Play MIDI (requires local MIDI playback support)")
    print("2. Export to .mid file")
    print("3. Cancel")

    choice = input("Enter your choice (1-3): ").strip()
    io_manager.save_user_input(f"MIDI choice: {choice}")

    if choice == "1":
        try:
            print("Playing score as MIDI...")
            score.show("midi")
        except Exception as e:
            print(f"Error playing MIDI: {e}")
        
    elif choice == "2":
        filename = input("Enter MIDI filename (e.g., song.mid): ").strip()
        io_manager.save_user_input(f"MIDI export filename: {filename}")
        if not filename:
            print("Cancelled (no filename).")
            return
        path = project_paths.project_path(filename)
        try:
            score.write("midi", fp=path)
            print(f"Exported MIDI to {path}")
        except Exception as e:
            print(f"Error exporting MIDI: {e}")
    
    elif choice == "3":
        print("Cancelled.")
    else:
        print("Invalid choice.")

def load_project(filename: str) -> stream.Score:
    io_manager.save_user_input(f"Load project requested: {filename}")
    path = project_paths.project_path(filename)

    try:
        if filename.endswith(".m21data"):
            with open(path, "rb") as f:
                score = pickle.load(f)
            print(f"Loaded project from {path}")
            return score
        elif filename.endswith(".xml"):
            score = converter.parse(path)
            print(f"Loaded MusicXML score from {path}")
            return score
        else:
            print("Unsupported file format.")
            return stream.Score()
    except FileNotFoundError:
        print(f"No file found at {path}. Starting new score.")
        return stream.Score()
    except Exception as e:
        print(f"Error loading project: {e}")
        return stream.Score()