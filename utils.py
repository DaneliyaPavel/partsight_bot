import re, inspect, collections
from functools import lru_cache
from pymorphy2 import MorphAnalyzer
from stop_words import get_stop_words

# --- shim для Python ≥3.11 --------------------------------
if not hasattr(inspect, "getargspec"):
    def _getargspec(func):  # type: ignore
        spec = inspect.getfullargspec(func)
        ArgSpec = collections.namedtuple(
            "ArgSpec", "args varargs keywords defaults"
        )
        return ArgSpec(spec.args, spec.varargs, spec.varkw, spec.defaults)
    inspect.getargspec = _getargspec        # type: ignore
# ----------------------------------------------------------

_morph = MorphAnalyzer()
_stop  = set(get_stop_words("ru"))
_brand_stop = {
    "movelex", "krauf", "zommer", "fair", "parts",
    "cummins", "foton", "mx"
}

_NUM_RE = re.compile(r"\d{4,}")      # цепочки ≥4 цифр
_WORD_RE = re.compile(r"[a-zа-яё]+")

@lru_cache(maxsize=20_000)
def _lemma(w: str) -> str:
    return _morph.parse(w)[0].normal_form

def normalize(text: str) -> str:
    txt = text.lower()
    numbers = _NUM_RE.findall(txt)            # оставляем длинные коды
    words   = _WORD_RE.findall(_NUM_RE.sub(" ", txt))
    lemmas  = [
        _lemma(w) for w in words
        if w not in _stop and w not in _brand_stop
    ]
    return " ".join(numbers + lemmas)         # порядок: [коды] + [лексика]
