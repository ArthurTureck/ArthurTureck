"""Gera os SVGs do perfil (avatar, banner e cartões de impacto) nos temas claro e escuro."""
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FONT = "'Inter', 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"

TEMAS = {
    "dark": dict(bg1="#0A1F1A", bg2="#133B31", grid="#1E4A3E", card="#0F2A23", borda="#1F4A3E",
                 texto="#F2F5F3", suave="#A7BDB4", fraco="#6E8A80", laranja="#F0892B", menta="#5CC8A0",
                 barra_antes="#F0892B"),
    "light": dict(bg1="#F6F9F7", bg2="#E3EEE8", grid="#CFDED6", card="#FFFFFF", borda="#D3E0D9",
                  texto="#0D2620", suave="#3D5A50", fraco="#6A8379", laranja="#C9650E", menta="#1C7A5A",
                  barra_antes="#E07A1F"),
}


def monograma(x, y, s, t, id_):
    """Selo 'AT': quadrado arredondado verde, letras brancas e traço laranja."""
    k = s / 500
    return f'''<g transform="translate({x},{y}) scale({k})">
  <defs><linearGradient id="{id_}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0E3B2F"/><stop offset="1" stop-color="#1B5E4A"/></linearGradient></defs>
  <rect width="500" height="500" rx="112" fill="url(#{id_})"/>
  <text x="250" y="318" text-anchor="middle" font-family="{FONT}" font-size="236" font-weight="800" fill="#FFFFFF" letter-spacing="-10">AT</text>
  <rect x="112" y="356" width="150" height="22" rx="11" fill="#F0892B"/>
</g>'''


def avatar():
    """Quadrado cheio: o GitHub e o LinkedIn recortam em círculo, então o conteúdo fica no centro."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" viewBox="0 0 500 500" role="img" aria-label="Monograma AT">
  <defs><linearGradient id="av" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0E3B2F"/><stop offset="1" stop-color="#1B5E4A"/></linearGradient></defs>
  <rect width="500" height="500" fill="url(#av)"/>
  <text x="250" y="290" text-anchor="middle" font-family="{FONT}" font-size="200" font-weight="800" fill="#FFFFFF" letter-spacing="-8">AT</text>
  <rect x="150" y="326" width="120" height="18" rx="9" fill="#F0892B"/>
</svg>'''


def banner(nome):
    t = TEMAS[nome]
    # Barras: minutos por relatório, antes (~25 min, só a montagem) e hoje (~3 min)
    base, x0, w, gap = 236, 842, 34, 14
    alturas = [140, 132, 146, 136, 142, 17, 17]
    barras = []
    for i, h in enumerate(alturas):
        depois = i >= 5
        cor = t["menta"] if depois else t["barra_antes"]
        op = 1 if depois else 0.35 + i * 0.1
        x = x0 + i * (w + gap) + (24 if depois else 0)
        d = f"{i * 0.08:.2f}s"
        barras.append(
            f'<rect x="{x}" y="{base - h}" width="{w}" height="{h}" rx="6" fill="{cor}" opacity="{op:.2f}">'
            f'<animate attributeName="height" from="0" to="{h}" dur=".8s" begin="{d}" fill="freeze"/>'
            f'<animate attributeName="y" from="{base}" to="{base - h}" dur=".8s" begin="{d}" fill="freeze"/></rect>')
    xa = x0 + 5 * (w + gap) + 24
    chips = [("Python", 78), ("JavaScript", 100), ("PDF · OCR", 96), ("Dashboards", 104), ("Testes automáticos", 150)]
    cx, chip_svg = 230, []
    for txt, cw in chips:
        chip_svg.append(f'<rect x="{cx}" y="222" width="{cw}" height="28" rx="14" fill="none" stroke="{t["borda"]}"/>'
                        f'<text x="{cx + cw / 2}" y="241" text-anchor="middle">{txt}</text>')
        cx += cw + 10
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-label="Arthur Tureck: automação e dados para Segurança do Trabalho">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>
  <pattern id="pt" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.4" fill="{t["grid"]}"/></pattern></defs>
  <rect width="1200" height="300" rx="20" fill="url(#g)"/>
  <rect x="800" y="0" width="400" height="300" fill="url(#pt)"/>
  <clipPath id="cl"><rect width="1200" height="300" rx="20"/></clipPath>
  <rect x="0" y="292" width="1200" height="8" fill="{t["laranja"]}" opacity=".9" clip-path="url(#cl)"/>
  {monograma(64, 64, 132, t, "mg")}
  <text x="230" y="112" font-family="{FONT}" font-size="54" font-weight="800" fill="{t["texto"]}" letter-spacing="-1.5">Arthur Tureck</text>
  <text x="232" y="152" font-family="{FONT}" font-size="23" font-weight="700" fill="{t["laranja"]}">Automação e dados para Segurança do Trabalho</text>
  <text x="232" y="188" font-family="{FONT}" font-size="17" fill="{t["suave"]}">Segurança do Trabalho · Copa Energia · Cascavel (PR)</text>
  <g font-family="{FONT}" font-size="13.5" font-weight="600" fill="{t["suave"]}">{"".join(chip_svg)}</g>
  <text x="842" y="52" font-family="{FONT}" font-size="13" font-weight="700" fill="{t["fraco"]}" letter-spacing="1.5">MINUTOS POR RELATÓRIO</text>
  <line x1="836" y1="{base + .5}" x2="1166" y2="{base + .5}" stroke="{t["fraco"]}" stroke-width="1.5"/>
  {"".join(barras)}
  <text x="842" y="262" font-family="{FONT}" font-size="13" fill="{t["fraco"]}">antes: ~25 min</text>
  <text x="1166" y="262" text-anchor="end" font-family="{FONT}" font-size="13" fill="{t["menta"]}" font-weight="700">hoje: ~3 min</text>
  <text x="{xa + 40}" y="{base - 40}" text-anchor="middle" font-family="{FONT}" font-size="34" font-weight="800" fill="{t["menta"]}" opacity="0">−88%<animate attributeName="opacity" from="0" to="1" dur=".5s" begin=".9s" fill="freeze"/></text>
</svg>'''


def impacto(nome):
    t = TEMAS[nome]
    cards = [("~3 min", "por relatório, era ~25", "5 a 6 relatórios por mês", t["laranja"]),
             ("~24 h", "por ano devolvidas", "à equipe de Segurança", t["menta"]),
             ("&lt; 1 s", "para juntar 121 PDFs", "testado com arquivos reais", t["menta"]),
             ("16/16", "formulários endireitados", "por OCR, sem internet", t["menta"])]
    out = []
    for i, (n, l1, l2, cor) in enumerate(cards):
        out.append(f'''<g transform="translate({24 + i * 290},24)"><rect width="270" height="132" rx="16" fill="{t["card"]}" stroke="{t["borda"]}"/>
      <rect x="24" y="22" width="36" height="5" rx="2.5" fill="{cor}"/>
      <text x="24" y="74" font-family="{FONT}" font-size="40" font-weight="800" fill="{t["texto"]}" letter-spacing="-1">{n}</text>
      <text x="24" y="100" font-family="{FONT}" font-size="15" font-weight="600" fill="{t["suave"]}">{l1}</text>
      <text x="24" y="120" font-family="{FONT}" font-size="13.5" fill="{t["fraco"]}">{l2}</text></g>''')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1184" height="180" viewBox="0 0 1184 180" role="img" '
            f'aria-label="Impacto: cada relatório de ~25 min para ~3 min; ~24 h por ano; 121 PDFs em menos de 1 s; '
            f'16 de 16 formulários endireitados">{"".join(out)}</svg>')


if __name__ == "__main__":
    (ASSETS / "avatar.svg").write_text(avatar(), encoding="utf-8")
    for tema in TEMAS:
        (ASSETS / f"banner-{tema}.svg").write_text(banner(tema), encoding="utf-8")
        (ASSETS / f"impacto-{tema}.svg").write_text(impacto(tema), encoding="utf-8")
    print("ok")
