from music21 import stream, note, chord
from scorecreator import io_manager

def edit_notes(score: stream.Score):

    if not len(score.parts):
        print("No instruments available to edit.")
        return
    
    print("\n--- Edit / Delete Tools ---")
    print("Available parts:")
    for i, part in enumerate(score.parts, 1):
        print(f"{i}. {partName or f'Part {i}'}")
    
    choice = input("Select a part number: ").strip()
    io_manager.save_user_input(f"Edit menu part selection: {choice}")

    try:
        part = score.parts[int(choice) - 1]
    except (IndexError, ValueError):
        print("Invalid part selection.")
        return
    
    print(f"\nSelected part: {part.partName or 'Unnamed'}")
    print("1. View notws and chords")
    print("2. Edit a note or chord")
    print("3. Delete a note or chord")
    print("4. Return to main menu")

    action = input("Enter choice (1-4): ").strip()
    io_manager.save_user_input(f"Edit action: {action}")

    if action == "1":
        view_part_contents(part)
    elif action == "2":
        modify_element(part)
    elif action == "3":
        delete_element(part)
    elif action == "4":
        return
    else:
        print("Invalid choice.")

def view_part_contents(part: stream.Part):
    print("\n--- Current Elements ---")
    for i, el in enumerate(part.recurse().notesAndRests, 1):
        desc = f"Note: {el.nameWithOctave}"
    elif isinstance(el, chord.Chord):
        desc = f"Chord: {'+'.join(p.nameWithOctave for p in el.pitches)}"
    else:
        desc = f"Rest"
    print(f"{i}. {desc}, duration={el.duration.quarterLength}")

def modify_element(part: stream.Part):
    elements = list(part.recurse().notesAndRests)
    if not elements:
        print("This part is empty.")
        return
    
    view_part_contents(part)
    index = input("Enter number of element to edit: ").strip()
    io_manager.save_user_input(f"Edit index: {index}")

    try:
        target = elements[int(index) - 1]
    except (IndexError, ValueError):
        print("Invalid index.")
        return
    
    if isinstance(target, note.Note):
        new_pitch = input(f"New pitch for {target.nameWithOctave}: ").strip()
        io_manager.save_user_input(f"Edit pitch: {new_pitch}")
        try:
            target.nameWithOctave = new_pitch
            print(f"Updated note to {target.nameWithOctave}")
        except Exception as e:
            print(f"Error updating note: {e}")
        
    elif isinstance(target, chord.Chord):
        new_chord_input = input(
            f"New chord for {'+'.join(p.nameWithOctave for p in target.pitches)} (e.g., C4 E4 G4): "
        ).strip()
        io_manager.save_user_input(f"Edit chord: {new_chord_input}")
        try:
            new_notes = [note.Note(p) for p in new_chord_input.split()]
            target.pitches = [n.pitch for n in new_notes]
            print(f"Updated chord to {target.pitchNames}")
        except Exception as e:
            print(f"Error updating chord: {e}")
        
    else:
        print("Rests cannot be modified (delete and reinsert instead).")

def delete_element(part: stream.Part):
    elements = list(part.recurse().notesAndRests)
    if not elements:
        print("This part is empty.")
        return
    
    view_part_contents(part)
    index = input("Enter number of element to delete: ").strip()
    io_manager.save_user_input(f"Delete index: {index}")

    try:
        target = element[int(index) - 1]
        part.remove(target)
        print("Element removed.")
    except (IndexError, ValueError):
        print("Invalid index.")
    except Exception as e:
        print(f"Error removing element: {e}")