import json
import urllib.parse
import urllib.request


def sugerir_en_desde_es(texto_es: str) -> str:
    t = (texto_es or "").strip()
    if not t:
        return ""
    try:
        q = urllib.parse.quote(t, safe="")
        url = (
            "https://translate.googleapis.com/translate_a/single"
            f"?client=gtx&sl=es&tl=en&dt=t&q={q}"
        )
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 ElaFood/1.0"},
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        data = json.loads(raw)
        # Respuesta esperada: [[["translated","original",...],...],...]
        chunks = data[0] if isinstance(data, list) and data else []
        out = "".join(part[0] for part in chunks if isinstance(part, list) and part)
        return out.strip() or ""
    except Exception:
        return ""
