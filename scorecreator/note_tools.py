from music21 import note, chord, duration, stream
from scorecreator import io_manager

def add_notes_to_part(score: stream.Score):

    if not len(score.parts):
        print("No instruments in the score. Add one first.")
        return
    
    print("\n--- Add Notes / Rests / Chords ---")
    print("Available parts:")
    for i, part in enumerate(score.parts, 1):
        print(f"{i}. {part.partName or 'Unnamed Part'}")
    
    choice = input("Select part by number: ").strip()
    io_manager.save_user_input(f"Note entry part selection: {choice}")

    if not choice.isdigit() or not (1 <= int(choice) <= len(score.parts)):
        print("Invalid choice.")
        return
    
    part = score.parts[int(choice) - 1]

    print("\nEntering note input mode.")
    print("Enter Symbolds like:")
    print("  • single note → C4, G#3, F5")
    print("  • rest → rest") #ideally we want rests represented as simply r
    print("  • chord → C4+E4+G4")
    print("  • type 'done' when finished\n")

    while True:
        entry = input("Enter note/chord/rest (or 'done'): ").strip()
        io_manager.save_user_input(f"Note entry: {entry}")

        if entry.lower() == "done":
            print("Existing note entry mode.")
            break
        
        if not entry:
            continue
        
        dur_input = input("Enter duration (e.g., quarter, half, eighth, 1.0): ").strip()
        io_manager.save_user_input(f"Duration entry: {dur_input}")

        try:
            d = duration.Duration(dur_input)
        except Exception:
            print("Invalid duration. Defaulting to quarter.")
            d = duration.Duration("quarter")

        element = None
        try:
            if entry.lower() == "rest":
                element = note.Rest()
            elif "+" in entry:
                pitches = [p.strip() for p in entry.split("+")]
                element = chord.Chord(pitches)
            else:
                element = note.Note(entry)
            
            element.duration = d
            part.append(element)
            print(f"Added: {element} ({d.type})")
        except Exception as e:
            print(f"Could not create element: {e}")
    
    print(f"Finished editing {part.partName or 'Unnamed Part'}.")

def edit_notes(score: stream.Score):
    print("\nEditing tools will come in Stage 4.")