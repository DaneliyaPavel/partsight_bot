from __future__ import annotations

from pathlib import Path
from typing import List, Dict

from docx import Document


def parse_request_docx(path: Path) -> List[Dict[str, str]]:
    """
    Читает DOCX-запрос и возвращает список уникальных позиций:
      {"material": "...", "naimenovanie": "..."}
    """
    doc = Document(path)
    rows, seen = [], set()

    for tbl in doc.tables:
        header = [c.text.strip() for c in tbl.rows[0].cells]
        if not any("Код материала" in h for h in header):
            continue

        mat_idx = header.index(next(h for h in header if "Код материала" in h))
        name_idx = header.index(next(h for h in header if "Предмет" in h))

        for r in tbl.rows[1:]:
            cells = [c.text.strip() for c in r.cells]
            if len(cells) <= max(mat_idx, name_idx):
                continue
            code, name = cells[mat_idx], cells[name_idx]
            key = (code, name)
            if key in seen:
                continue
            seen.add(key)
            rows.append({"material": code, "naimenovanie": name})
        break  # нашли нужную таблицу

    return rows


__all__ = ["parse_request_docx"]
