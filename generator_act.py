import datetime, configparser
from pathlib import Path
from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docx import Document

_cfg = configparser.ConfigParser(); _cfg.read("config.ini")
_TPL = Path(_cfg["files"]["TEMPLATE_PATH"])
_OUT = Path("output"); _OUT.mkdir(exist_ok=True)

def build_act(packs: list[dict]) -> Path:        # ← обычная def
    first, composer = True, None
    for p in packs:
        tpl = DocxTemplate(_TPL)
        tpl.render(
            dict(
                material=p["material"],
                naimenovanie=p["naimenovanie"],
                obosnovanost="обоснованно",
                nalichie="отсутствие",
                vozmoznost=p["vozmoznost"],
                rekomendacii=p["rekomendacii"],
            )
        )
        tmp = _OUT / f"_tmp_{p['material']}.docx"
        tpl.save(tmp)

        if first:
            master = Document(tmp)
            composer = Composer(master)
            first = False
        else:
            composer.append(Document(tmp))
        tmp.unlink()

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = _OUT / f"Акт_{ts}.docx"
    composer.save(out)
    return out
