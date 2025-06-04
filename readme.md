# PDF Slicer

PDF Slicer is a small utility for extracting page ranges from PDF files. It ships with a simple graphical interface built with `customtkinter` but the slicing logic can also be imported and used programmatically.

## Features

- Select a PDF and export a range of pages
- Lightweight GUI
- Reusable `slice_pdf` function for scripting

## Requirements

- Python 3.x
- PyPDF2
- customtkinter
- reportlab (only required for tests)

## Installation

```sh
pip install -r requirements.txt
```

## Usage

Run the application:

```sh
python main.py
```

From the GUI select the source PDF, choose the initial and final page and click **Export File**.

## Project Structure

```
src/pdf_slicer/   # package modules
main.py           # application entry point
requirements.txt
```

The package exposes a `slice_pdf` function which can be imported from `pdf_slicer`.

## License

MIT