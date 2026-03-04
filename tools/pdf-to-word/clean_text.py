import re


def clean_text(text: str) -> str:
    """Clean extracted text with Hungarian-optimised OCR corrections."""

    # Remove page markers
    text = re.sub(r"--- Page \d+ ---\n?", "", text)

    # ---- Hungarian OCR y-misreads ----
    text = re.sub(r"vág[)7rj]", "vagy", text)
    text = re.sub(r"hogy[7rj]", "hogy", text)
    text = re.sub(r"vagy[7rj]", "vagy", text)
    text = text.replace("szeméi}'", "személy")
    text = text.replace("gj^akran", "gyakran")
    text = text.replace("eg)7", "egy")
    text = text.replace("eg7", "egy")
    text = text.replace("hogy7", "hogy")
    text = text.replace("vagy7", "vagy")
    text = text.replace("vagy- ", "vagy ")
    text = text.replace("hogy- ", "hogy ")
    text = text.replace("nőnverbális", "nonverbális")
    text = text.replace("ísmerősség", "ismerősség")
    text = text.replace("ísmeret", "ismeret")

    text = re.sub(
        r"\b(hogy|vagy|mely|bármely|amily|valamily|oly|egypár|vág)[7r\)\}\]]",
        r"\1y",
        text,
    )
    text = re.sub(r"y7", "y", text)

    # ---- Paragraph joining & hyphen handling ----
    blocks = re.split(r"(\n\s*\n)", text)

    cleaned_blocks = []
    for block in blocks:
        if re.match(r"\n\s*\n", block):
            cleaned_blocks.append("\n\n")
            continue

        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if not lines:
            continue

        joined_para = ""
        for i, line in enumerate(lines):
            if line.endswith("\u00ad") or line.endswith("-"):
                if line.endswith("\u00ad"):
                    joined_para += line[:-1]
                else:
                    next_starts_lower = (
                        i + 1 < len(lines)
                        and lines[i + 1]
                        and (lines[i + 1][0].islower() or lines[i + 1][0] in "íéáűúóöő")
                    )
                    if next_starts_lower:
                        joined_para += line[:-1]
                    else:
                        joined_para += line + (" " if i < len(lines) - 1 else "")
            else:
                joined_para += line + (" " if i < len(lines) - 1 else "")

        # Strip in-text citations like (Author, 2020)
        joined_para = re.sub(
            r"\((?![0-9]\. fejezet)[^)]*(18|19|20)\d{2}[^)]*\)", "", joined_para
        )

        # Remove ampersand artefacts
        joined_para = re.sub(r"^& ", "", joined_para)
        joined_para = re.sub(r" & ", " ", joined_para)

        # Drop noisy symbol-only lines
        if re.match(r"^[^\w\s]{4,}$", joined_para):
            continue
        if len(re.findall(r"[/\^<>;:!_]", joined_para)) > len(joined_para) * 0.3:
            continue

        # Collapse whitespace
        joined_para = re.sub(r" +", " ", joined_para)
        joined_para = re.sub(r" ([.,;?!])", r"\1", joined_para)

        cleaned_blocks.append(joined_para.strip())

    result = "".join(cleaned_blocks)

    # Final cleanup
    result = re.sub(r"\n[^\w\s]{3,}\n", "\n\n", result)
    result = re.sub(r"\?tcl<[^\n]+", "", result)
    result = re.sub(r"\n\n+", "\n\n", result)

    return result.strip()
