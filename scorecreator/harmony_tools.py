from music21 import chord, harmony, note, stream
from scorecreator import io_manager

def harmony_menu(score: stream.Score):
    while True:
        print("\n--- Harmony Tools ---")
        print("1. Add chord to instrument")
        print("2. Harmonize an existing melodic line")
        print("3. Analyze harmony (Roman numerals)")
        print("4. Back to main menu")

        choice = input("Enter your choice (1-4): ").strip()
        io_manager.save_user_input(f"Harmony menu choice: {choice}")

        if choice == "1":
            add_chord_to_part(score)
        elif choice == "2":
            harmonize_existing_line(score)
        elif choice == "3":
            analyze_harmony(score)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")
    
def add_chord_to_part(score: stream.Score):
    if len(score.parts) ==  0:
        print("No instruments available. Add one first.")
        return

    print("\nSelect instrument to add chord to:")
    for i, part in enumerate(score.parts, 1):
        name = part.partName or f"Part {1}"
        print(f"{i}. {name}")
    
    choice = input("Choose by number: ").strip()
    io_manager.save_user_input(f"Chord add: instrument choice {choice}")

    try:
        part = score.parts[int(choice) - 1]
    except (IndexError, ValueError):
        print("Invalid instrument choice.")
        return
    
    chord_input = input("Enter chord pitches (e.g., C4 E4 G4): ").strip()
    io_manager.save_user_input(f"Chord pitches: {chord_input}")

    duration_input = input("Enter duration (e.g., 1.0 for quarter note): ").strip()
    io_manager.save_user_input(f"Chord duration: {duration_input}")

    try:
        notes = [note.Note(p) for p in chord_input.split()]
        dur = float(duration_input) if duration_input else 1.0
        ch = chord.Chord(notes)
        ch.duration.quarterLength = dur
        part.append(ch)
        print(f"Added chord {ch.pitchNames} to {part.Name or 'instrument'}.")
    except Exception as e:
        print(f"Error creating chord: {e}")

def harmonize_existing_line(score: stream.Score):
    if len(score.parts) < 1:
        print("No melodic part to harmonize.")
        return
    
    print("\nSelect melodic part to harmonize:")
    for i, part in enumerate(score.parts, 1):
        print(f"{i}. {part.partName or f'Part {i}'}")
    
    choice = input("Choose part number: ").strip()
    io_manager.save_user_input(f"Harmonize part choice: {choice}")

    try:
        part = score.parts[int(choice) - 1]
    except (IndexError, ValueError):
        print("Invalid choice.")
        return
    
    new_part_name = input("Enter name for harmony part: ").strip() or "Harmony"
    io_manager.save_user_input(f"Harmony part name: {new_part_name}")

    harmony_part = stream.Part()
    harmony_part.partName = new_part_name

    print("Enter harmonic intervals relative to each note (e.g., m3, P5, M6).")
    print("Leave blank to skip a note. Type 'done' when finished.")

    for element in part.recurse().notes:
        print(f"Base note: {element.nameWithOctave}")
        interval_str = input("Interval for this note: ").strip()
        io_manager.save_user_input(f"Interval for {element.nameWithOctave}: {interval_str}")

        if interval_str.lower() == "done":
            break
        elif not interval_str:
            continue
        
        try:
            intv: harmony.interval.Interval(interval_str)
            new_note = element.transpose(intv)
            harmony_part.append(new_note)
        except Exception as e:
            print(f"Invalid interval: {e}")
        
    score.append(harmony_part)
    print(f"Harmony part '{new_part_name}' added.")

def analyze_harmony(score: stream.Score):
    print("\n---Harmonic Analysis ---")

    try:
        key_guess = score.analyze("key")
        print(f"Detected key: {key_guess.tonic.name} {key_guess.mode}")

        rn_stream = stream.Stream()
        for ch in score.chordify().recurse().getElementsByClass("chord"):
            rn = harmony.chordSymbolFigureFromChord(ch, key_guess)
            rn_stream.append(rn)
            print(rn.figure, end=" ")
        
        print("\nHarmonic analysis complete.")
    except Exception as e:
        print(f"Error analyzing harmony: {e}")