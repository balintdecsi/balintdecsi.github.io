import fitz


def extract_text_general(pdf_path: str) -> str:
    """Extract all text blocks from a PDF in reading order."""
    doc = fitz.open(pdf_path)
    all_text = []

    for page in doc:
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (b[1], b[0]))

        page_text = []
        for b in blocks:
            x0, y0, x1, y1, text, block_no, block_type = b
            if block_type != 0:
                continue
            stripped = text.strip()
            if len(stripped) < 2:
                continue
            page_text.append(stripped)

        if page_text:
            all_text.append("\n\n".join(page_text))

    doc.close()
    return "\n\n".join(all_text)


def extract_text_column(pdf_path: str) -> str:
    """Extract main-column text using left/right heuristic for two-column scanned layouts.

    Odd pages (0-indexed even): main column on the left  (~x0<100, x1<345).
    Even pages (0-indexed odd):  main column on the right (~x0>140).
    """
    doc = fitz.open(pdf_path)
    all_text = []

    for i, page in enumerate(doc):
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: b[1])

        page_text = []
        for b in blocks:
            x0, y0, x1, y1, text, block_no, block_type = b
            if block_type != 0:
                continue
            width = x1 - x0
            if width > 350 or width < 20 or len(text.strip()) < 2:
                continue

            is_main = False
            if i % 2 == 0:
                if x0 < 100 and x1 < 345:
                    is_main = True
            else:
                if x0 > 140:
                    is_main = True

            if is_main:
                page_text.append(text.strip())

        if page_text:
            all_text.append("\n\n".join(page_text))

    doc.close()
    return "\n\n".join(all_text)


def extract_text(pdf_path: str, use_column_detection: bool = False) -> str:
    if use_column_detection:
        return extract_text_column(pdf_path)
    return extract_text_general(pdf_path)
