"""
upload_imagens.py
-----------------
Sobe todas as imagens da pasta ./imagens/ para o imgbb
e retorna os links diretos prontos para colar no site.

COMO USAR:
1. Pegue sua chave gratuita da API em: https://api.imgbb.com/
2. Cole a chave na variável API_KEY abaixo (ou crie o arquivo .env)
3. Coloque suas imagens na pasta ./imagens/
4. Rode:  python ferramentas/upload_imagens.py
"""

import os
import sys
import base64
import json
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# ── CONFIGURAÇÃO ───────────────────────────────────────────
# Cole sua chave aqui ou defina a variável de ambiente IMGBB_KEY
API_KEY = os.environ.get("IMGBB_KEY", "COLE_SUA_CHAVE_AQUI")

# Pasta onde você coloca as imagens
PASTA_IMAGENS = Path(__file__).parent.parent / "imagens"

# Extensões aceitas
EXTENSOES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# ── UPLOAD ─────────────────────────────────────────────────
def upload(caminho: Path) -> dict:
    """Envia uma imagem para o imgbb e retorna o resultado."""
    with open(caminho, "rb") as f:
        dados_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = urllib.parse.urlencode({
        "key": API_KEY,
        "name": caminho.stem,
        "image": dados_b64,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.imgbb.com/1/upload",
        data=payload,
        method="POST"
    )
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    if API_KEY == "COLE_SUA_CHAVE_AQUI":
        print("\n❌ Configure a API_KEY primeiro!")
        print("   1. Acesse https://api.imgbb.com/")
        print("   2. Crie conta gratuita e copie a chave")
        print("   3. Cole no arquivo ferramentas/upload_imagens.py")
        print("      ou rode:  IMGBB_KEY=suachave python ferramentas/upload_imagens.py\n")
        sys.exit(1)

    if not PASTA_IMAGENS.exists():
        PASTA_IMAGENS.mkdir(parents=True)
        print(f"\n📁 Pasta criada: {PASTA_IMAGENS}")
        print("   Coloque suas imagens lá e rode o script novamente.\n")
        sys.exit(0)

    imagens = [
        p for p in sorted(PASTA_IMAGENS.iterdir())
        if p.is_file() and p.suffix.lower() in EXTENSOES
    ]

    if not imagens:
        print(f"\n⚠️  Nenhuma imagem encontrada em: {PASTA_IMAGENS}")
        print(f"   Formatos aceitos: {', '.join(EXTENSOES)}\n")
        sys.exit(0)

    print(f"\n🚀 Subindo {len(imagens)} imagem(ns)...\n")
    resultados = []

    for img in imagens:
        print(f"  ⬆  {img.name} ...", end=" ", flush=True)
        try:
            r = upload(img)
            if r.get("success"):
                link_direto = r["data"]["url"]
                link_thumb  = r["data"].get("thumb", {}).get("url", link_direto)
                link_pagina = r["data"].get("url_viewer", link_direto)
                resultados.append({
                    "arquivo": img.name,
                    "link_direto": link_direto,
                    "link_thumb":  link_thumb,
                    "link_pagina": link_pagina,
                })
                print(f"✅")
            else:
                print(f"❌ Erro: {r}")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            print(f"❌ HTTP {e.code}: {body[:200]}")
        except Exception as e:
            print(f"❌ {e}")

    # ── SAÍDA ──────────────────────────────────────────────
    if not resultados:
        print("\n❌ Nenhuma imagem foi enviada com sucesso.\n")
        sys.exit(1)

    print("\n" + "═" * 60)
    print("  LINKS PARA COLAR NO SITE")
    print("═" * 60)

    for r in resultados:
        print(f"\n📷  {r['arquivo']}")
        print(f"    Link direto (use no src=): {r['link_direto']}")
        print(f"    Página imgbb:              {r['link_pagina']}")

    # Salva também em arquivo JSON e TXT
    saida_json = Path(__file__).parent / "links_gerados.json"
    saida_txt  = Path(__file__).parent / "links_gerados.txt"

    with open(saida_json, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    with open(saida_txt, "w", encoding="utf-8") as f:
        for r in resultados:
            f.write(f"{r['arquivo']}:\n")
            f.write(f"  src=\"{r['link_direto']}\"\n\n")

    print(f"\n✅ Links salvos em:")
    print(f"   {saida_json}")
    print(f"   {saida_txt}")
    print()


if __name__ == "__main__":
    main()
