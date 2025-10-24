from music21 import instrument, stream, clef
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