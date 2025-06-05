"""GUI for PDF Slicer using customtkinter."""

import os
import customtkinter as ctk
from tkinter import filedialog
from PyPDF2 import PdfReader
from .slicer import slice_pdf


class PdfSlicerApp:
    """Simple GUI application for slicing PDFs."""

    def __init__(self) -> None:
        self.current_file_path: str | None = None
        self.total_pages: int = 0

        self.root = ctk.CTk()
        self.root.title("PDF Exporter")
        self.root.geometry("600x400")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self._build_widgets()

    # ------------------------------------------------------------------
    def _build_widgets(self) -> None:
        frame = ctk.CTkFrame(master=self.root, corner_radius=10)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(tuple(range(11)), weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.output_title_entry = ctk.CTkEntry(frame, justify="center")

        select_button = ctk.CTkButton(
            master=frame,
            text="Select PDF File",
            command=lambda: self.select_pdf_file(),
        )
        select_button.grid(row=0, column=0, pady=10, padx=20)

        self.file_name_label = ctk.CTkLabel(frame, text="File: No PDF loaded")
        self.file_name_label.grid(row=1, column=0, pady=5, padx=20)

        self.pages_label = ctk.CTkLabel(frame, text="Total Pages: 0")
        self.pages_label.grid(row=2, column=0, pady=5, padx=20)

        initial_page_label = ctk.CTkLabel(frame, text="Initial Page:")
        initial_page_label.grid(row=3, column=0, pady=5, padx=20)
        self.initial_page_entry = ctk.CTkEntry(frame)
        self.initial_page_entry.grid(row=4, column=0, pady=5, padx=20)

        final_page_label = ctk.CTkLabel(frame, text="Final Page:")
        final_page_label.grid(row=5, column=0, pady=5, padx=20)
        self.final_page_entry = ctk.CTkEntry(frame)
        self.final_page_entry.grid(row=6, column=0, pady=5, padx=20)

        output_title_label = ctk.CTkLabel(frame, text="Output File Title:")
        output_title_label.grid(row=7, column=0, pady=5, padx=20)
        self.output_title_entry.grid(row=8, column=0, pady=5, padx=20, sticky="ew")
        frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(frame, text="")
        self.status_label.grid(row=9, column=0, pady=5, padx=20)

        self.export_button = ctk.CTkButton(
            master=frame,
            text="Export File",
            state="disabled",
            command=self.export_pdf,
        )
        self.export_button.grid(row=10, column=0, pady=10, padx=20)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        frame.grid(padx=20, pady=20)

    # ------------------------------------------------------------------
    def validate_inputs(self, *_args) -> None:
        try:
            initial_page = int(self.initial_page_entry.get())
            final_page = int(self.final_page_entry.get())
        except ValueError:
            self.export_button.configure(state="disabled")
            return

        if (
            1 <= initial_page <= self.total_pages
            and 1 <= final_page <= self.total_pages
            and final_page >= initial_page
        ):
            self.export_button.configure(state="normal")
            file_name = os.path.splitext(os.path.basename(self.current_file_path))[0] if self.current_file_path else "output"
            if initial_page == final_page:
                title = f"{file_name}_sliced_p{initial_page}.pdf"
            else:
                title = f"{file_name}_sliced_p{initial_page}_to_p{final_page}.pdf"
            self.output_title_entry.delete(0, ctk.END)
            self.output_title_entry.insert(0, title)
        else:
            self.export_button.configure(state="disabled")

    # ------------------------------------------------------------------
    def select_pdf_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Select a PDF File",
            filetypes=[("PDF Files", "*.pdf")],
        )
        if not file_path:
            self.file_name_label.configure(text="File: No PDF loaded")
            return

        self.current_file_path = file_path
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        self.output_title_entry.delete(0, ctk.END)
        self.output_title_entry.insert(0, f"{file_name}_sliced.pdf")

        reader = PdfReader(file_path)
        self.total_pages = len(reader.pages)

        self.pages_label.configure(text=f"Total Pages: {self.total_pages}")
        self.file_name_label.configure(text=f"File: {file_name}")

        self.initial_page_entry.bind("<KeyRelease>", self.validate_inputs)
        self.final_page_entry.bind("<KeyRelease>", self.validate_inputs)

    # ------------------------------------------------------------------
    def export_pdf(self) -> None:
        initial_page = int(self.initial_page_entry.get())
        final_page = int(self.final_page_entry.get())
        output_file_name = self.output_title_entry.get()
        output_dir = os.path.dirname(self.current_file_path)
        output_path = os.path.join(output_dir, output_file_name)

        try:
            slice_pdf(
                self.current_file_path,
                initial_page,
                final_page,
                output_path,
            )
        except Exception as exc:  # pragma: no cover - GUI feedback only
            self.status_label.configure(text=f"Error: {exc}", text_color="red")
        else:
            self.status_label.configure(
                text=f"File saved!", text_color="green"
            )
            self.root.after(3000, lambda: self.status_label.configure(text=""))

    # ------------------------------------------------------------------
    def run(self) -> None:
        self.root.mainloop()


def create_gui() -> None:
    """Launch the GUI application."""
    PdfSlicerApp().run()