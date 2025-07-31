from docx import Document
from pathlib import Path

def parse_request_docx(path: Path) -> list[dict]:
    """Возвращает список уникальных ЗИПов (по material+name)."""
    doc = Document(path)
    rows = []
    seen = set()          # (material, name) → исключаем дубликаты

    for tbl in doc.tables:
        header = [c.text.strip() for c in tbl.rows[0].cells]
        if not any("Код материала" in h for h in header):
            continue

        mat_idx  = header.index(next(h for h in header if "Код материала" in h))
        name_idx = header.index(next(h for h in header if "Предмет" in h))

        for r in tbl.rows[1:]:
            cells = [c.text.strip() for c in r.cells]
            if len(cells) <= max(mat_idx, name_idx):
                continue
            code = cells[mat_idx]
            name = cells[name_idx]
            key = (code, name)
            if key in seen:
                continue
            seen.add(key)
            rows.append({"material": code, "naimenovanie": name})
        break

    return rows
