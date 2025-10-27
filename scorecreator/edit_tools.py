from music21 import stream, note, chord
from scorecreator import io_manager

def edit_notes(score: stream.Score):

    if not len(score.parts):
        print("No instruments available to edit.")
        return
    
    print("\n--- Edit / Delete Tools ---")
    print("Available parts:")
    for i, part in enumerate(score.parts, 1):
        print(f"{i}. {part.partName or f'Part {i}'}")
    
    choice = input("Select a part number: ").strip()
    io_manager.save_user_input(f"Edit menu part selection: {choice}")

    try:
        part = score.parts[int(choice) - 1]
    except (IndexError, ValueError):
        print("Invalid part selection.")
        return
    
    while True:
        print(f"\nSelected part: {part.partName or 'Unnamed'}")
        print("Options: (v)iew (a)ction (m)odify single (d)elete single (q)uit to main")
        opt = input("Choose option: ").strip().lower()
        io_manager.save_user_input(f"Edit option: {opt}")
        
        if opt in ("q", "quit", "exit"):
            return
        elif opt in ("m", "modify"):
            modify_element(part)
        elif opt in ("v", "view"):
            view_part_contents(part)
        elif opt in ("d", "delete"):
            delete_element(part)
        elif opt in ("a", "action"):
            action_input = input(
                "Enter index spec and action (e.g. '3-5 delete', '2 transpose 2', '1,4 restify'): "
            ).strip()
            io_manager.save_user_input(f"Edit action input: {action_input}")
            if not action_input:
                continue

            tokens = action_input.split()
            if len(tokens) < 2:
                print("Invalid input. Must include index/spec and action.")
                continue

            index_spec = tokens[0]
            action = tokens[1].lower()
            action_value = tokens[2] if len(tokens) > 2 else None
            
            elements = list(part.recurse().notesAndRests)
            indices = parse_index_spec(index_spec, len(elements))
            if not indices:
                print("No valid indices parsed.")
                continue
            
            targets = [elements[i - 1] for i in indices]
            
            print(f"Action '{action}' will be applied to {len(targets)} element(s):")
            for i, t in zip(indices, targets):
                if isinstance(t, note.Note):
                    desc = f"Note {t.nameWithOctave}"
                elif isinstance(t, chord.Chord):
                    desc = f"Chord {'+'.join(p.nameWithOctave for p in t.pitches)}"
                else:
                    desc = "Rest"
                print(f"  {i}: {desc} (dur={t.duration.quarterLength})")
            
            confirm = input("Proceed? (y/N): ").strip().lower()
            io_manager.save_user_input(f"Edit action confirm: {confirm}")
            if confirm != "y":
                print("Cancelled.")
                continue

            try:
                apply_action_to_targets(part, targets, action, action_value)
                print(f"Action '{action}' applied to {len(targets)} element(s).")
            except Exception as e:
                print(f"Error applying action: {e}")
        else:
            print("Unknown option. Choose v/a/m/d/q.")

def view_part_contents(part: stream.Part):
    print("\n--- Current Elements ---")
    
    notes_array = [
        el.nameWithOctave if isinstance(el, note.Note)
        else "+".join(p.nameWithOctave for p in el.pitches) if isinstance(el, chord.Chord)
        else "Rest"
        for el in part.recurse().notesAndRests
    ]
    print("\nAs array:", notes_array)
    
    for i, el in enumerate(part.recurse().notesAndRests, 1):
        if isinstance(el, note.Note):
            desc = f"Note: {el.nameWithOctave}"
        elif isinstance(el, chord.Chord):
            desc = f"Chord: {'+'.join(p.nameWithOctave for p in el.pitches)}"
        else:
            desc = "Rest"
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
        target = elements[int(index) - 1]
        part.remove(target)
        print("Element removed.")
    except (IndexError, ValueError):
        print("Invalid index.")
    except Exception as e:
        print(f"Error removing element: {e}")
        
def parse_index_spec(spec: str, max_len: int):
    out = set()
    pieces = [p.strip() for p in spec.split(",") if p.strip()]
    try:
        for p in pieces:
            if "-" in p:
                a, b = p.split("-", 1)
                start = int(a)
                end = int(b)
                if start < 1 or end < start:
                    return []
                for i in range(start, end + 1):
                    if 1 <= i <= max_len:
                        out.add(i)
            else:
                i = int(p)
                if 1 <= i <= max_len:
                    out.add(i)
        return sorted(out)
    except Exception:
        return []

def apply_action_to_targets(part: stream.Part, targets: list, action: str, value: str = None):
    if action == "delete":
        for el in list(targets):
            try:
                parent = el.getContextByClass(stream.Part) or part
                parent.remove(el)
            except Exception:
                try:
                    part.remove(el)
                except Exception:
                    pass

    elif action == "transpose":
        if value is None:
            raise ValueError("Missing semitone value for transpose.")
        semis = int(value)
        for el in targets:
            try:
                el.transpose(semis, inPlace=True)
            except Exception:
                pass

    elif action == "restify":
        for el in list(targets):
            try:
                parent = el.getContextByClass(stream.Part) or part
                offset = el.offset
                dur = el.duration
                r = note.Rest()
                r.duration = dur
                parent.remove(el)
                parent.insert(offset, r)
            except Exception as e:
                print(f"Warning: could not restify element: {e}")
            
        part.coreGatherMissingSpanners()
        part._elements = [el for el in part._elements if el is not None]
        part.elementsChanged()
    
    else:
        raise ValueError(f"Unsupported action: {action}")