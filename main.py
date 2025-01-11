import customtkinter as ctk
from tkinter import filedialog
import os
from PyPDF2 import PdfReader, PdfWriter

def validate_inputs(initial_page_entry, final_page_entry, export_button, total_pages):
    try:
        initial_page = int(initial_page_entry.get())
        final_page = int(final_page_entry.get())

        if (1 <= initial_page <= total_pages and
            1 <= final_page <= total_pages and
            final_page >= initial_page):
            export_button.configure(state="normal")
        else:
            export_button.configure(state="disabled")
    except ValueError:
        export_button.configure(state="disabled")

def select_pdf_file(output_title_entry, initial_page_entry, final_page_entry, export_button):
    global current_file_path, total_pages
    file_path = filedialog.askopenfilename(
        title="Select a PDF File",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if file_path:
        print(f"Selected file: {file_path}")
        current_file_path = file_path
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        output_title_entry.delete(0, ctk.END)
        output_title_entry.insert(0, f"{file_name}_sliced.pdf")

        # Read the PDF to get the total number of pages
        pdf_reader = PdfReader(file_path)
        total_pages = len(pdf_reader.pages)

        # Bind validation to input events
        initial_page_entry.bind("<KeyRelease>", lambda e: validate_inputs(initial_page_entry, final_page_entry, export_button, total_pages))
        final_page_entry.bind("<KeyRelease>", lambda e: validate_inputs(initial_page_entry, final_page_entry, export_button, total_pages))
    else:
        print("No file selected.")

def export_pdf(output_title_entry, initial_page_entry, final_page_entry):
    initial_page = int(initial_page_entry.get()) - 1  # Convert to zero-based index
    final_page = int(final_page_entry.get()) - 1
    output_file_name = output_title_entry.get()
    output_dir = os.path.dirname(current_file_path)
    output_path = os.path.join(output_dir, output_file_name)

    pdf_reader = PdfReader(current_file_path)
    pdf_writer = PdfWriter()

    for page_num in range(initial_page, final_page + 1):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    with open(output_path, "wb") as output_file:
        pdf_writer.write(output_file)

    print(f"Exported file saved at: {output_path}")

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
    output_title_entry = ctk.CTkEntry(frame)

    select_button = ctk.CTkButton(
        master=frame, 
        text="Select PDF File",
        command=lambda: select_pdf_file(output_title_entry, initial_page_entry, final_page_entry, export_button)
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
    output_title_entry.grid(row=6, column=0, pady=5, padx=20)

    export_button = ctk.CTkButton(
        master=frame, 
        text="Export File",
        state="disabled",
        command=lambda: export_pdf(output_title_entry, initial_page_entry, final_page_entry)
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
