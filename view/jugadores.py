import streamlit as st
import streamlit.components.v1 as components
import base64
import os


def get_image_base64(path: str) -> str:
    """Convierte una imagen local a base64 para usar en HTML."""
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    ext = path.rsplit(".", 1)[-1].lower()
    mime = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "webp": "image/webp",
        "gif": "image/gif",
    }.get(ext, "image/png")
    return f"data:{mime};base64,{data}"


def jugadores_page(db):

    st.header("⚽ Jugadores disponibles")

    jugadores = list(
        db.jugadores.find().sort("puntosTotales", -1)
    )

    if not jugadores:
        st.warning("No hay jugadores registrados.")
        return

    iconos_equipo = {
        "Manchester City": "assets/manchesterCity.jpg",
        "Real Madrid":     "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg",
        "Barcelona":       "https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg",
        "Bayern Munich":   "https://upload.wikimedia.org/wikipedia/commons/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg",
        "PSG":             "https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg",
        "Liverpool":       "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg",
        "Arsenal":         "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg",
        "Chelsea":         "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg",
        "Atletico Madrid": "https://upload.wikimedia.org/wikipedia/en/f/f4/Atletico_Madrid_2017_logo.svg",
        "Juventus":        "https://upload.wikimedia.org/wikipedia/commons/1/15/Juventus_FC_2017_icon_%28black%29.svg",
        "Inter Milan":     "https://upload.wikimedia.org/wikipedia/commons/0/05/FC_Internazionale_Milano_2021.svg",
        "AC Milan":        "https://upload.wikimedia.org/wikipedia/commons/d/d0/Logo_of_AC_Milan.svg",
        "Borussia Dortmund": "https://upload.wikimedia.org/wikipedia/commons/6/67/Borussia_Dortmund_logo.svg",
    }

    PLACEHOLDER = "https://placehold.co/150x150/1a2a5e/888?text=?"

    def resolve_imagen(jugador) -> str:
        """
        Intenta cargar la imagen del jugador desde assets/.
        El campo 'imagen' puede ser:
          - "assets/haaland.png"    → ruta relativa
          - "haaland.png"           → solo nombre, se busca en assets/
          - una URL http            → se usa directo
        """
        imagen = jugador.get("imagen", "")
        nombre = jugador.get("nombre", "jugador").lower().replace(" ", "_")

        # Si ya es URL externa, úsala directo
        if imagen.startswith("http"):
            return imagen

        # Construir rutas candidatas
        candidatas = []
        if imagen:
            candidatas.append(imagen)
            candidatas.append(f"assets/{imagen}")
            candidatas.append(f"assets/{os.path.basename(imagen)}")

        # También intentar por nombre del jugador
        for ext in ["png", "jpg", "jpeg", "webp"]:
            candidatas.append(f"assets/{nombre}.{ext}")

        for ruta in candidatas:
            b64 = get_image_base64(ruta)
            if b64:
                return b64

        return PLACEHOLDER

    def build_card(jugador):
        nombre   = jugador.get("nombre", "")
        equipo   = jugador.get("equipo", "-")
        posicion = jugador.get("posicion", "-")
        puntos   = jugador.get("puntosTotales", 0)
        imagen   = resolve_imagen(jugador)

        icono_ruta = iconos_equipo.get(equipo)
        if icono_ruta:
            if not icono_ruta.startswith("http"):
                icono_url = get_image_base64(icono_ruta)
            else:
                icono_url = icono_ruta
            icono_html = f'<img class="club-icon" src="{icono_url}" />'
        else:
            icono_html = '<span style="font-size:20px">⚽</span>'


        return f"""
        <div class="player-card">
            <img class="player-photo"
                 src="{imagen}"
                 onerror="this.src='{PLACEHOLDER}'"
            />
            <div class="player-name-row">
                {icono_html}
                <span class="player-name">{nombre}</span>
            </div>
            <hr class="player-divider" />
            <table class="player-info">
                <tr>
                    <td>🏟️ Equipo</td>
                    <td>{equipo}</td>
                </tr>
                <tr>
                    <td>⚽ Posición</td>
                    <td>{posicion}</td>
                </tr>
                <tr>
                    <td>🏆 Puntos totales</td>
                    <td>{puntos}</td>
                </tr>
            </table>
        </div>
        """

    filas_html = ""
    for i in range(0, len(jugadores), 3):
        fila = jugadores[i:i + 3]
        cards = "".join(build_card(j) for j in fila)
        cards += '<div class="player-card invisible"></div>' * (3 - len(fila))
        filas_html += f'<div class="players-grid">{cards}</div>'

    html_completo = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8"/>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            background-color: #0d1b3e;
            font-family: 'Segoe UI', sans-serif;
            padding: 10px 4px;
        }}

        .info-box {{
            background-color: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 10px;
            padding: 14px 18px;
            margin-bottom: 24px;
            color: #c8d6f0;
            font-size: 15px;
        }}

        .info-box b {{
            color: #ffffff;
            display: block;
            margin-bottom: 4px;
            font-size: 16px;
        }}

        .players-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;
            margin-bottom: 18px;
        }}

        .player-card {{
            background: linear-gradient(160deg, #112060 0%, #0a1540 100%);
            border: 1px solid rgba(255,255,255,0.13);
            border-radius: 18px;
            padding: 24px 18px 20px 18px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }}

        .player-card.invisible {{
            visibility: hidden;
        }}

        .player-photo {{
            width: 150px;
            height: 150px;
            object-fit: cover;
            object-position: top center;
            border-radius: 12px;
            border: 2px solid rgba(255,255,255,0.18);
            margin-bottom: 14px;
            display: block;
        }}

        .player-name-row {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-bottom: 14px;
        }}

        .club-icon {{
            width: 26px;
            height: 26px;
            object-fit: contain;
        }}

        .player-name {{
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
        }}

        .player-divider {{
            width: 100%;
            border: none;
            border-top: 1px solid rgba(255,255,255,0.13);
            margin: 4px 0 14px 0;
        }}

        .player-info {{
            width: 100%;
            border-collapse: collapse;
        }}

        .player-info tr td {{
            padding: 6px 2px;
            font-size: 15px;
            vertical-align: middle;
        }}

        .player-info tr td:first-child {{
            color: #9fb3d8;
            text-align: left;
            white-space: nowrap;
            padding-right: 10px;
        }}

        .player-info tr td:last-child {{
            color: #ffffff;
            font-weight: 700;
            text-align: right;
        }}
    </style>
    </head>
    <body>
        <div class="info-box">
            <b>Selecciona jugadores para armar tu equipo</b>
            Los jugadores vienen del torneo oficial; aquí solo se muestran como tarjetas.
        </div>
        {filas_html}
    </body>
    </html>
    """

    num_filas = (len(jugadores) + 2) // 3
    altura = 120 + (num_filas * 360)

    components.html(html_completo, height=altura, scrolling=False)