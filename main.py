import customtkinter as ctk

def create_gui():
    # Create main application window
    root = ctk.CTk()
    root.title("PDF Exporter")
    root.geometry("300x400")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Create a frame to centralize the content with inner padding
    frame = ctk.CTkFrame(master=root, corner_radius=10)
    frame.grid(row=0, column=0, sticky="")
    frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Add widgets with inner padding inside the frame
    select_button = ctk.CTkButton(
        master=frame, 
        text="Select PDF File",
        command=lambda: print("Select PDF button clicked")  # Placeholder command
    )
    select_button.grid(row=0, column=0, pady=10, padx=20)

    initial_page_label = ctk.CTkLabel(frame, text="Initial Page:")
    initial_page_label.grid(row=1, column=0, pady=5, padx=20)
    initial_page_entry = ctk.CTkEntry(frame)
    initial_page_entry.grid(row=2, column=0, pady=5, padx=20)

    final_page_label = ctk.CTkLabel(frame, text="Final Page:")
    final_page_label.grid(row=3, column=0, pady=5, padx=20)
    final_page_entry = ctk.CTkEntry(frame)
    final_page_entry.grid(row=4, column=0, pady=5, padx=20)

    output_title_label = ctk.CTkLabel(frame, text="Output File Title:")
    output_title_label.grid(row=5, column=0, pady=5, padx=20)
    output_title_entry = ctk.CTkEntry(frame)
    output_title_entry.grid(row=6, column=0, pady=5, padx=20)

    export_button = ctk.CTkButton(
        master=frame, 
        text="Export File",
        command=lambda: print("Export File button clicked")  # Placeholder command
    )
    export_button.grid(row=7, column=0, pady=10, padx=20)

    # Center frame within the window
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    frame.grid(padx=20, pady=20)

    # Run the application
    root.mainloop()

# Call the function to create the GUI
create_gui()
