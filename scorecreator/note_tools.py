from music21 import note, chord, duration, stream
from scorecreator import io_manager

def parse_durations(dur_input, n_elements):
    dur_list = []
    try:
        tokens = [t.strip() for t in dur_input.split(",")]
        for token in tokens:
            if "*" in token:
                val, times = token.split("*")
                dur_list.extend([duration.Duration(float(val))]*int(times))
            else:
                dur_list.append(duration.Duration(float(token)))
        while len(dur_list) < n_elements:
            dur_list.append(dur_list[-1])
    except Exception as e:
        print(f"Error parsing durations: {e}. Defaulting to quarter.")
        dur_list = [duration.Duration("quarter")]*n_elements
    return dur_list

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
        
        entry = entry.replace(",", " ").replace("  ", " ").strip()
        entries = entry.split()
        
        total_notes = 0
        for token in entries:
            if "*" in token:
                _, times = token.split("*")
                total_notes += int(times)
            else:
                total_notes += 1
        print(f"{total_notes} note element(s) will be added to instrument part.")
        
        dur_input = input("Enter duration (e.g., quarter, half, eighth, 1.0): ").strip()
        io_manager.save_user_input(f"Duration entry: {dur_input}")
        
        dur_list = parse_durations(dur_input, total_notes)
        
        print(f"{len(dur_list)} duration(s) added to instrument part note(s).")

        for token, d in zip(entries, dur_list):
            try:
                if "*" in token:
                    pitch_token, times = token.split("*")
                    times = int(times)
                else:
                    pitch_token = token
                    times = 1
                
                for _ in range(times):    
                    if pitch_token.lower() in ("rest", "r"):
                        element = note.Rest()
                    elif "+" in token:
                        pitches = [p.strip() for p in pitch_token.split("+")]
                        element = chord.Chord(pitches)
                    else:
                        element = note.Note(pitch_token)
                
                    element.duration = d
                    part.append(element)
                
                    if isinstance(element, note.Note):
                        print(f"Added note: {element.nameWithOctave} ({d.type})")
                    elif isinstance(element, chord.Chord):
                        print(f"Added chord: {'+'.join(p.nameWithOctave for p in element.pitches)} ({d.type})")
                    else:
                        print(f"Added rest ({d.type})")
                
            except Exception as e:
                print(f"Could not create element '{token}': {e}")           

    print(f"Finished editing {part.partName or 'Unnamed Part'}.")