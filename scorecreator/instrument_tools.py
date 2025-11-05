from music21 import instrument, stream, clef, key, meter, tempo, stream
from scorecreator import io_manager

def instrument_maker_menu() -> stream.Part:

    print("\n--- Instrument Creation ---")
    available = list_available_instruments()
    print("Available instruments:")
    for i, name in enumerate(available, 1):
        print(f"{i}. {name}")
    
    choice = input("Select an instrument by number or name: ").strip()
    io_manager.save_user_input(f"Instrument choice: {choice}")

    instr_class = resolve_instrument(choice, available)
    if instr_class is None:
        print("Invalid choice. Defaulting to GenericInstrument.")
        instr_class = instrument.Instrument
    
    part = stream.Part()
    part.insert(0, instr_class())

    part_name = input("Enter a name for this part (e.g., 'Violin I'): ").strip()
    io_manager.save_user_input(f"Part name: {part_name}")
    if part_name:
        part.partName = part_name
    
    clef_choice = input("Choose clef (treble, bass, alto, none): ").strip().lower()
    io_manager.save_user_input(f"Clef choice: {clef_choice}")
    if clef_choice == "treble":
        part.insert(0, clef.TrebleClef())
    elif clef_choice == "bass":
        part.insert(0, clef.BassClef())
    elif clef_choice == "alto":
        part.insert(0, clef.AltoClef())
    elif clef_choice == "none":
        pass
    
    ks_input = input("Enter key signature (number or sharps/flats, e.g., 0, -3, 2): ").strip()
    if ks_input:
        try:
            ks = key.KeySignature(int(ks_input))
            part.insert(0, ks)
        except Exception:
            print("Invalid key signature. Skipping.")
    
    ts_input = input("Enter time signature (e.g., 4/4, 3/4): ").strip()
    if ts_input:
        try:
            ts = meter.TimeSignature(ts_input)
            part.insert(0, ts)
        except Exception:
            print("Invalid time signature. Skipping.")
        
    tempo_input = input("Enter tempo (BPM, e.g., 120): ").strip()
    if tempo_input:
        try:
            mm = tempo.MetronomeMark(number=float(tempo_input))
            part.insert(0, mm)
        except Exception:
            print("Invalid tempo. Skipping.")
    
    print(f"Created part: {part.partName or instr_class.__name__}")
    return part

def list_available_instruments():
    available = []
    for attr_name in dir(instrument):
        obj = getattr(instrument, attr_name)
        if isinstance(obj, type) and issubclass(obj, instrument.Instrument):
            available.append(attr_name)
    
    excluded = {"Instrument", "InstrumentSubclass", "Conductor", "UnpitchedInstrument"}
    clean_list = sorted([name for name in available if name not in excluded])
    return clean_list

def resolve_instrument(choice, available_list):
    try:
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(available_list):
                return getattr(instrument, available_list[idx])
        for name in available_list:
            if choice.lower() == name.lower():
                return getattr(instrument, name)
    except Exception:
        pass
    return None

def add_more_notes_to_existing(score: stream.Score):
    print("Almost there")
    
def delete_instrument(score: stream.Score):
    if not len(score.parts):
        print("No instrument parts available to delete.")
        return
    
    print("\n--- Delete Instrument Part ---")
    for i, part in enumerate(score.parts, 1):
        print(f"{i}. {part.partName or f'Part {i}'}")
    
    choice = input("Select part number to delete: ").strip()
    io_manager.save_user_input(f"Delete instrument selection: {choice}")
    
    try:
        index = int(choice) - 1
        part = score.parts[index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return
    
    confirm = input(f"Delete '{part.partName or f'Part {index+1}'}'? (y/N): ").strip().lower()
    io_manager.save_user_input(f"Delete instrument confirm: {confirm}")
    if confirm != "y":
        print("Cancelled.")
        return
    
    try:
        score.remove(part, recurse=True)
        score.coreGatherMissingSpanners()
        score.coreElementsChanged()
        
        print(f"Deleted: {part.partName or f'Part {index+1}'}")
    except Exception as e:
        print(f"Error deleting instrument: {e}")
        
    for i, p in enumerate(score.parts, 1):
        if not p.partName:
            p.partName = f"Part {i}"
            
def reorder_instruments(score: stream.Score):
    if not len(score.parts):
        print("No instrumnt parts available to reorder.")
        
        print("\n--- Reoder instrument parts ---")
        print("Current order:")
        for i, part in enumerate(score.parts, 1):
            print(f"{i}. {part.partName or f'Part{i}'}")
        
    print("\nEnter the new order as a comma-space-separated list of indices (e.g. 2, 1, 3)")
    new_order_input = input("New order: ").strip()
    io_manager.save_user_input(f"Reorder instrument order: {new_order_input}")
    
    try:
        new_indices = [int(x) - 1 for x in new_order_input.split(", ")]
        if sorted(new_indices) != list(range(len(score.parts))):
            print("Invalid order. Must include all part numbers exactly once.")
            return
    except Exception:
        print("Invalid input format.")
        return
    
    try:
        new_parts = [score.parts[i] for i in new_indices]
        
        score.parts.clear()
        for p in new_parts:
            score.insert(0, p)
        
        score.coreGatherMissingSpanners()
        score.coreElementsChanged()
        
        print("\nReordered instruments successfully! New order:")
        for i, part in enumerate(score.parts, 1):
            print(f"{i}.  {part.partName or f'Part{i}'}")
    except Exception as e:
        print(f"Error reordering the instruments: {e}")