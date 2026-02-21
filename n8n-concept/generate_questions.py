"""
Branch 2: Generate Questions
- Parse PDFs
- Send text to gpt-4.1-mini to generate 3 questions per document
- Write results to a local text file
"""

from pathlib import Path

from PyPDF2 import PdfReader
from openai import OpenAI

import config


def extract_text_from_pdf(file_path: str) -> str:
    """Extract all text from a PDF file, joining pages."""
    reader = PdfReader(file_path)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def generate_questions(client: OpenAI, document_text: str) -> list[str]:
    """Use LLM to generate 3 questions from document text."""
    response = client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=[
            {"role": "system", "content": config.QUESTION_SYSTEM_PROMPT},
            {"role": "user", "content": f'The given document:\n"""\n{document_text}\n"""'},
        ],
    )

    raw_output = response.choices[0].message.content or ""
    questions = [
        line.strip()
        for line in raw_output.split("\n")
        if line.strip()
    ]
    return questions


def process(file_paths: list[str]):
    """Process a list of PDF files: extract text, generate questions, save to file."""
    print("\n=== Branch 2: Generate Questions ===")

    # Validate API key
    api_key = config.OPENAI_API_KEY
    if api_key.startswith("PLACEHOLDER"):
        print("ERROR: Set OPENAI_API_KEY environment variable before running.")
        return

    client = OpenAI(api_key=api_key)
    output_path = Path(config.OUTPUT_FILE)

    # Overwrite file on each run (mirrors n8n TRUNCATE behavior)
    with open(output_path, "w", encoding="utf-8") as f:
        for file_path in file_paths:
            file_name = Path(file_path).name
            print(f"\nProcessing: {file_name}")

            # 1. Extract text
            text = extract_text_from_pdf(file_path)
            if not text.strip():
                print(f"  WARNING: No text extracted from {file_name}, skipping.")
                continue
            print(f"  Extracted {len(text)} characters")

            # 2. Generate questions via LLM
            print(f"  Generating questions with {config.LLM_MODEL}...")
            questions = generate_questions(client, text)
            print(f"  Generated {len(questions)} questions")

            # 3. Write to output file
            f.write(f"[Document: {file_name}]\n")
            for q in questions:
                f.write(f"- {q}\n")
            f.write("\n")

    print(f"\nDone. Questions saved to: {output_path.resolve()}")
