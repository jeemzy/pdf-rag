"""
Main entry point for the n8n pipeline replacement.

Usage:
    python main.py                 # processes all PDFs in the 'PDF' folder
    python main.py file1.pdf ...   # processes specific files

Runs both branches:
  - Branch 1: Vectorize documents → Qdrant
  - Branch 2: Generate questions → text file
"""

import argparse
import sys
from pathlib import Path

import vectorize_documents
import generate_questions


def parse_args():
    """Parse CLI arguments and return validated file paths."""
    parser = argparse.ArgumentParser(
        description="Process PDF files: vectorize into Qdrant and generate questions.",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="One or more PDF file paths to process. Defaults to all PDFs in the 'PDF' folder.",
    )
    parser.add_argument(
        "--skip-vectorize",
        action="store_true",
        help="Skip Branch 1 (vector storage)",
    )
    parser.add_argument(
        "--skip-questions",
        action="store_true",
        help="Skip Branch 2 (question generation)",
    )

    args = parser.parse_args()

    files_to_process = args.files
    if not files_to_process:
        pdf_dir = Path("PDF")
        if pdf_dir.exists() and pdf_dir.is_dir():
            files_to_process = list(pdf_dir.glob("*.pdf"))
            if not files_to_process:
                print("ERROR: No PDF files found in the 'PDF' directory.")
                sys.exit(1)
        else:
            print("ERROR: No valid PDF files provided and 'PDF' directory not found.")
            sys.exit(1)

    # Validate all files exist and are PDFs
    validated = []
    for file_path in files_to_process:
        p = Path(file_path)
        if not p.exists():
            print(f"ERROR: File not found: {file_path}")
            sys.exit(1)
        if p.suffix.lower() != ".pdf":
            print(f"WARNING: {file_path} is not a PDF, skipping.")
            continue
        validated.append(str(p.resolve()))

    if not validated:
        print("ERROR: No valid PDF files provided.")
        sys.exit(1)

    return validated, args.skip_vectorize, args.skip_questions


def main():
    file_paths, skip_vectorize, skip_questions = parse_args()

    print(f"Files to process: {len(file_paths)}")
    for fp in file_paths:
        print(f"  - {fp}")

    # --- Branch 1: Vectorize Documents ---
    if not skip_vectorize:
        vectorize_documents.process(file_paths)
    else:
        print("\n--- Skipping Branch 1: Vector Storage ---")

    # --- Branch 2: Generate Questions ---
    if not skip_questions:
        generate_questions.process(file_paths)
    else:
        print("\n--- Skipping Branch 2: Question Generation ---")

    print("\n=== All done ===")


if __name__ == "__main__":
    main()
