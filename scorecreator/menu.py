import os
from music21 import stream
from scorecreator import (
    io_manager,
    instrument_tools,
    note_tools,
    harmony_tools,
    edit_tools,
    export_tools
)

def main():
    print("Welcome to Salieri")
    print("(powered by music21)")

    score = stream.Score()
    io_manager.save_user_input("Session started: new blank score")

    while True:
        print("\n--- Main Menu ---")
        print("1. Add a new instrument part")
        print("2. Add notes, rests, and chords to an existing instrument")
        print("3. Harmony tools")
        print("4. Edit/Delete notes or harmonies in existing instruments")
        print("5. Delete an instrument part")
        print("6. Reorder instruments")
        print("7. Show current score")
        print("8. Play score (Experimental: MIDI)")
        print("9. Save project")
        print("10. Export to MusicXML")
        print("11. Load existing project")
        print("12. Exit")

        choice = input("Enter your choice (1-12): ").strip()
        io_manager.save_user_input(f"Main menu choice: {choice}")

        if choice == "1":
            part = instrument_tools.instrument_maker_menu()
            score.append(part)
        
        elif choice == "2":
            note_tools.add_notes_to_part(score)
        
        elif choice == "3":
            harmony_tools.harmony_menu(score)
        
        elif choice == "4":
            edit_tools.edit_notes(score)
        
        elif choice == "5":
            instrument_tools.delete_instrument(score)
        
        elif choice == "6":
            instrument_tools.reorder_instruments(score)
        
        elif choice == "7":
            export_tools.show_score(score)
        
        elif choice == "8":
            export_tools.export_midi(score)
        
        elif choice == "9":
            io_manager.save_project(score)
        
        elif choice == "10":
            export_tools.export_musicxml(score)
        
        elif choice == "11":
            project_dir = os.path.join(os.getcwd(), "projects")
            os.makedirs(project_dir, exist_ok=True)
            files = [
                f for f in os.listdir(project_dir)
                if f.endswith((".m21data", ".xml"))
            ]
            
            if not files:
                print("No saved projects found.")
                continue
            
            print("\nAvailable projects:")
            for i, f in enumerate(files, 1):
                print(f"{i}. {f}")
            
            filename = input("Select project by number or name: ").strip()
            io_manager.save_user_input(f"Load filename: {filename}")

            if filename.isdigit() and i <= int(filename) <= len(files):
                filename = files[int(filename) - 1]
            
            score = io_manager.load_project(filename)
            print(f"Loaded project: {filename}")
        
        elif choice == "12":
            print("\nDiletto straordinario!")
            io_manager.save_user_input("Exit program")
            quit()

        else:
            print("Invalid choice. Try again.")
            io_manager.save_user_input(f"Invalid choice: {choice}")
            
if __name__ == "__main__":
    main()