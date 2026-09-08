"""HIIT Timer - Cronômetro HIIT simples e funcional."""
import json
import asyncio
from pathlib import Path
import flet as ft

# ==================== CONFIGURAÇÃO PADRÃO ====================
ARQUIVO_DADOS = "dados.json"

CONFIG_PADRAO = {
    "exercicios": [
        {"nome": "Polichinelo", "emoji": "🤸", "duracao": 60},
        {"nome": "Elevação de joelhos", "emoji": "🦵", "duracao": 60},
        {"nome": "Crucifixo", "emoji": "🦋", "duracao": 60},
        {"nome": "Extensão de braços", "emoji": "💪", "duracao": 60},
        {"nome": "Agachamento", "emoji": "🏋️", "duracao": 60},
    ],
    "descanso_curto": 30,
    "descanso_ciclo": 60,
    "num_ciclos": 3,
}

# ==================== PERSISTÊNCIA ====================
def get_path() -> Path:
    base = Path(__file__).parent.resolve()
    return base / ARQUIVO_DADOS

def carregar() -> dict:
    try:
        with get_path().open("r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return CONFIG_PADRAO.copy()

def salvar(dados: dict) -> bool:
    try:
        with get_path().open("w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        return False

# ==================== HELPERS ====================
def fmt(segundos: int) -> str:
    m = segundos // 60
    s = segundos % 60
    return f"{m:02d}:{s:02d}"

def gerar_etapas(config: dict, num_ciclos: int) -> list:
    etapas = []
    idx = 0
    for ciclo in range(1, num_ciclos + 1):
        for i, ex in enumerate(config["exercicios"]):
            idx += 1
            etapas.append({
                "indice": idx, "nome": ex["nome"], "emoji": ex["emoji"],
                "duracao": ex["duracao"], "tipo": "exercicio", "ciclo": ciclo,
            })
            idx += 1
            if i == len(config["exercicios"]) - 1:
                etapas.append({
                    "indice": idx, "nome": "Descanso de ciclo", "emoji": "☕",
                    "duracao": config["descanso_ciclo"], "tipo": "descanso_ciclo", "ciclo": ciclo,
                })
            else:
                etapas.append({
                    "indice": idx, "nome": "Descanso", "emoji": "⏸️",
                    "duracao": config["descanso_curto"], "tipo": "descanso", "ciclo": ciclo,
                })
    return etapas

def tempo_total(config: dict, num_ciclos: int) -> int:
    return sum(e["duracao"] for e in gerar_etapas(config, num_ciclos))

# ==================== CORES ====================
CORES = {
    "exercicio": ("#9C27B0", "#4A148C", ft.Colors.PRIMARY_CONTAINER, ft.Colors.ON_PRIMARY_CONTAINER, "EXERCÍCIO"),
    "descanso": ("#FF9800", "#E65100", ft.Colors.SECONDARY_CONTAINER, ft.Colors.ON_SECONDARY_CONTAINER, "DESCANSO"),
    "descanso_ciclo": ("#FF9800", "#E65100", ft.Colors.SECONDARY_CONTAINER, ft.Colors.ON_SECONDARY_CONTAINER, "DESCANSO LONGO"),
}

# ==================== NAVEGAÇÃO ====================
def navegar(page: ft.Page, tela_func, *args, **kwargs):
    page.views.clear()
    page.views.append(tela_func(page, *args, **kwargs))
    page.update()

# ==================== TELA 1: CONFIGURAÇÃO ====================
def tela_config(page: ft.Page):
    config = carregar()
    num_ciclos = config["num_ciclos"]
    etapas = gerar_etapas(config, num_ciclos)
    tempo = tempo_total(config, num_ciclos)

    def iniciar_treino(_):
        navegar(page, tela_timer, config, num_ciclos)

    def abrir_editor(_):
        navegar(page, tela_editor)

    linhas_etapas = []
    for ep in etapas[:10]:
        cor = ft.Colors.PRIMARY if ep["tipo"] == "exercicio" else ft.Colors.ON_SURFACE_VARIANT
        linhas_etapas.append(ft.Row([
            ft.Text(ep["emoji"], size=18),
            ft.Text(ep["nome"], size=14, color=cor, expand=True),
            ft.Text(fmt(ep["duracao"]), size=14, weight=ft.FontWeight.BOLD, color=cor),
        ]))
    if len(etapas) > 10:
        linhas_etapas.append(ft.Text(f"... e mais {len(etapas) - 10} etapas", size=12, color=ft.Colors.ON_SURFACE_VARIANT, italic=True))

    return ft.View(
        route="/config", bgcolor=ft.Colors.SURFACE,
        appbar=ft.AppBar(title=ft.Text("HIIT Timer", weight=ft.FontWeight.BOLD), center_title=True, bgcolor=ft.Colors.PRIMARY),
        controls=[ft.SafeArea(content=ft.Column(expand=True, controls=[
            ft.Container(padding=24, margin=ft.Margin(16, 16, 16, 8), border_radius=16, bgcolor=ft.Colors.SURFACE_CONTAINER,
                content=ft.Column(spacing=16, controls=[
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
                        _stat("CICLOS", str(num_ciclos), ft.Colors.PRIMARY),
                        _stat("EXERCÍCIOS", str(len(config["exercicios"])), ft.Colors.SECONDARY),
                        _stat("ETAPAS", str(len(etapas)), ft.Colors.TERTIARY),
                        _stat("TEMPO", fmt(tempo), ft.Colors.PRIMARY),
                    ]),
                ])),
            ft.Container(padding=16, margin=ft.Margin(16, 8, 16, 8), border_radius=16, bgcolor=ft.Colors.SURFACE_CONTAINER,
                content=ft.Column(spacing=8, controls=[
                    ft.Text("PREVIEW DO TREINO", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Column(linhas_etapas, spacing=4),
                ])),
            ft.Container(padding=ft.Padding(16, 16, 16, 16),
                content=ft.Column(spacing=12, controls=[
                    ft.FilledButton("▶ INICIAR TREINO", icon=ft.Icons.PLAY_ARROW, on_click=iniciar_treino,
                        style=ft.ButtonStyle(padding=ft.Padding(0, 16, 0, 16), shape=ft.RoundedRectangleBorder(radius=12)), expand=True),
                    ft.OutlinedButton(" PERSONALIZAR TREINO", icon=ft.Icons.EDIT, on_click=abrir_editor,
                        style=ft.ButtonStyle(padding=ft.Padding(0, 16, 0, 16), shape=ft.RoundedRectangleBorder(radius=12)), expand=True),
                ])),
        ]))],
    )

def _stat(label: str, value: str, color: str):
    return ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4, controls=[
        ft.Text(label, size=10, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE_VARIANT),
        ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=color),
    ])

# ==================== TELA 2: EDITOR ====================
def tela_editor(page: ft.Page):
    config = carregar()
    local = {
        "exercicios": [ex.copy() for ex in config["exercicios"]],
        "descanso_curto": config["descanso_curto"],
        "descanso_ciclo": config["descanso_ciclo"],
        "num_ciclos": config["num_ciclos"],
    }

    tf_curto = ft.TextField(value=str(local["descanso_curto"]), keyboard_type=ft.KeyboardType.NUMBER, width=100, text_align=ft.TextAlign.CENTER)
    tf_ciclo = ft.TextField(value=str(local["descanso_ciclo"]), keyboard_type=ft.KeyboardType.NUMBER, width=100, text_align=ft.TextAlign.CENTER)
    tf_ciclos = ft.TextField(value=str(local["num_ciclos"]), keyboard_type=ft.KeyboardType.NUMBER, width=100, text_align=ft.TextAlign.CENTER)
    lv_exercicios = ft.ListView(spacing=8, expand=True)

    def rebuild_list():
        lv_exercicios.controls.clear()
        for idx, ex in enumerate(local["exercicios"]):
            i = idx
            tf_emoji = ft.TextField(value=ex["emoji"], width=50, text_align=ft.TextAlign.CENTER)
            tf_nome = ft.TextField(value=ex["nome"], dense=True, expand=True)
            tf_dur = ft.TextField(value=str(ex["duracao"]), width=80, keyboard_type=ft.KeyboardType.NUMBER, text_align=ft.TextAlign.CENTER)
            btn_del = ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.ERROR, disabled=len(local["exercicios"]) <= 1, tooltip="Remover exercício")

            def on_emoji(e, idx=i): local["exercicios"][idx]["emoji"] = e.control.value or "🏃"
            def on_nome(e, idx=i): local["exercicios"][idx]["nome"] = e.control.value or "Exercício"
            def on_dur(e, idx=i):
                try: local["exercicios"][idx]["duracao"] = max(1, int(e.control.value) if e.control.value else 30)
                except ValueError: local["exercicios"][idx]["duracao"] = 30

            def on_del(_, idx=i):
                def confirmar(e):
                    local["exercicios"].pop(idx)
                    rebuild_list()
                    dlg.open = False
                    page.update()
                def cancelar(e):
                    dlg.open = False
                    page.update()
                dlg = ft.AlertDialog(
                    title=ft.Text("Remover exercício?"),
                    content=ft.Text(f"Remover '{local['exercicios'][idx]['nome']}'?"),
                    actions=[
                        ft.TextButton("Cancelar", on_click=cancelar),
                        ft.FilledButton("Remover", on_click=confirmar, style=ft.ButtonStyle(bgcolor=ft.Colors.ERROR)),
                    ],
                )
                dlg.open = True
                page.update()

            tf_emoji.on_change = on_emoji
            tf_nome.on_change = on_nome
            tf_dur.on_change = on_dur
            btn_del.on_click = on_del

            lv_exercicios.controls.append(ft.Card(content=ft.Container(padding=12,
                content=ft.Row(vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[tf_emoji, tf_nome, tf_dur, btn_del]))))
        page.update()

    def on_curto(e):
        try: local["descanso_curto"] = max(1, int(e.control.value) if e.control.value else 30)
        except ValueError: local["descanso_curto"] = 30
    def on_ciclo(e):
        try: local["descanso_ciclo"] = max(1, int(e.control.value) if e.control.value else 60)
        except ValueError: local["descanso_ciclo"] = 60
    def on_ciclos(e):
        try: local["num_ciclos"] = max(1, min(20, int(e.control.value) if e.control.value else 3))
        except ValueError: local["num_ciclos"] = 3

    tf_curto.on_change = on_curto
    tf_ciclo.on_change = on_ciclo
    tf_ciclos.on_change = on_ciclos

    def add_exercicio(_):
        local["exercicios"].append({"nome": "Novo Exercício", "emoji": "", "duracao": 45})
        rebuild_list()

    def salvar_tudo(_):
        novo_config = {
            "exercicios": local["exercicios"],
            "descanso_curto": local["descanso_curto"],
            "descanso_ciclo": local["descanso_ciclo"],
            "num_ciclos": local["num_ciclos"],
        }
        if salvar(novo_config):
            navegar(page, tela_config)
        else:
            snackbar = ft.SnackBar(content=ft.Text("Erro ao salvar!"), bgcolor=ft.Colors.ERROR)
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()

    def cancelar(_):
        navegar(page, tela_config)

    rebuild_list()

    return ft.View(
        route="/editor", bgcolor=ft.Colors.SURFACE,
        appbar=ft.AppBar(title=ft.Text("Personalizar Treino", weight=ft.FontWeight.BOLD), center_title=True, bgcolor=ft.Colors.SURFACE,
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Voltar", on_click=lambda _: cancelar(None))),
        controls=[ft.SafeArea(content=ft.Column(expand=True, controls=[
            ft.Container(padding=16, margin=ft.Margin(16, 16, 16, 8), border_radius=12, bgcolor=ft.Colors.SURFACE_CONTAINER,
                content=ft.Column(spacing=12, controls=[
                    ft.Text("INTERVALOS E CICLOS", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
                        ft.Column([ft.Text("Descanso Curto (s)", size=12), tf_curto]),
                        ft.Column([ft.Text("Descanso Longo (s)", size=12), tf_ciclo]),
                        ft.Column([ft.Text("Nº de Ciclos", size=12), tf_ciclos]),
                    ]),
                ])),
            ft.Container(padding=ft.Padding(16, 0, 16, 0),
                content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text("EXERCÍCIOS", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.TextButton("ADICIONAR", icon=ft.Icons.ADD, on_click=add_exercicio),
                ])),
            ft.Container(expand=True, padding=ft.Padding(16, 0, 16, 0), content=lv_exercicios),
            ft.Container(padding=16, bgcolor=ft.Colors.SURFACE,
                content=ft.Row(alignment=ft.MainAxisAlignment.END, spacing=12, controls=[
                    ft.TextButton("CANCELAR", on_click=lambda _: cancelar(None)),
                    ft.FilledButton("SALVAR", icon=ft.Icons.CHECK, on_click=salvar_tudo),
                ])),
        ]))],
    )

# ==================== TELA 3: TIMER ====================
def tela_timer(page: ft.Page, config: dict, num_ciclos: int):
    etapas = gerar_etapas(config, num_ciclos)
    if not etapas:
        navegar(page, tela_config)
        return ft.View(route="/timer", controls=[ft.Text("Erro: treino vazio")])

    estado = {"idx": 0, "tempo": etapas[0]["duracao"], "pausado": False, "finalizado": False, "task": None, "cancel": asyncio.Event()}

    txt_nome = ft.Text("", size=22, weight=ft.FontWeight.W_600, color=ft.Colors.ON_SURFACE, text_align=ft.TextAlign.CENTER, max_lines=2)
    txt_tempo = ft.Text("", size=56, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE, font_family="RobotoMono")
    ring_progress = ft.ProgressRing(value=0.0, width=260, height=260, stroke_width=14, bgcolor=ft.Colors.TRANSPARENT)
    ring_track = ft.ProgressRing(value=1.0, width=260, height=260, stroke_width=14, bgcolor=ft.Colors.TRANSPARENT)
    txt_badge = ft.Text("", size=12, weight=ft.FontWeight.BOLD)
    badge_container = ft.Container(padding=ft.Padding(16, 6, 16, 6), margin=ft.Margin(0, 0, 0, 16), border_radius=20, content=txt_badge)
    txt_stats = ft.Text("", size=12, color=ft.Colors.ON_SURFACE_VARIANT, text_align=ft.TextAlign.CENTER)
    txt_proximo = ft.Text("", size=14, color=ft.Colors.ON_SURFACE_VARIANT, text_align=ft.TextAlign.CENTER)
    controls_container = ft.Container()

    ring_stack = ft.Stack(width=260, height=260, controls=[
        ring_track, ring_progress,
        ft.Container(content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4, controls=[txt_nome, txt_tempo]),
            alignment=ft.Alignment(0, 0), width=260, height=260),
    ])
    ring_area = ft.Container(content=ring_stack, alignment=ft.Alignment(0, 0), expand=True, padding=ft.Padding(24, 16, 24, 16))

    def update_static_ui():
        idx = estado["idx"]
        if idx >= len(etapas): return
        ep = etapas[idx]
        prox = etapas[idx + 1] if idx + 1 < len(etapas) else None
        cr, cf, badge_bg, badge_fg, badge_label = CORES.get(ep["tipo"], CORES["exercicio"])
        txt_badge.value = badge_label
        txt_badge.color = badge_fg
        badge_container.bgcolor = badge_bg
        ciclo_atual = ep["ciclo"]
        total_ciclos = max(e["ciclo"] for e in etapas)
        txt_stats.value = f"Ciclo {ciclo_atual}/{total_ciclos} • Etapa {idx + 1}/{len(etapas)}"
        txt_proximo.value = f"Próximo: {prox['emoji']} {prox['nome']}" if prox else "Última etapa!"
        controls_container.content = _controls_bar(retroceder, alternar_pausa, pular, estado["pausado"])
        txt_badge.update()
        badge_container.update()
        txt_stats.update()
        txt_proximo.update()
        controls_container.update()

    def refresh_ui():
        idx = estado["idx"]
        tempo = estado["tempo"]
        if idx >= len(etapas): return
        ep = etapas[idx]
        cr, cf, _, _, _ = CORES.get(ep["tipo"], CORES["exercicio"])
        ring_progress.color = cr
        ring_track.color = cf
        progresso = max(0.0, min(1.0, 1.0 - (tempo / ep["duracao"]))) if ep["duracao"] > 0 else 0.0
        ring_progress.value = progresso
        txt_nome.value = f"{ep['emoji']} {ep['nome']}"
        txt_tempo.value = fmt(tempo)
        txt_tempo.update()
        ring_progress.update()

    async def timer_loop():
        update_static_ui()
        refresh_ui()
        while not estado["cancel"].is_set() and estado["idx"] < len(etapas):
            if not estado["pausado"]:
                await asyncio.sleep(1)
                if estado["cancel"].is_set(): break
                estado["tempo"] -= 1
                if estado["tempo"] <= 0: await avancar()
                else: refresh_ui()
            else: await asyncio.sleep(0.1)
        if estado["idx"] >= len(etapas) and not estado["finalizado"]:
            estado["finalizado"] = True
            on_finalizar()

    async def avancar():
        try: page.haptic_feedback()
        except Exception: pass
        if estado["idx"] + 1 < len(etapas):
            estado["idx"] += 1
            estado["tempo"] = etapas[estado["idx"]]["duracao"]
            update_static_ui()
            refresh_ui()
        else:
            estado["finalizado"] = True
            on_finalizar()

    def retroceder():
        if estado["idx"] > 0:
            estado["idx"] -= 1
            estado["tempo"] = etapas[estado["idx"]]["duracao"]
            update_static_ui()
            refresh_ui()
        else: voltar_config()

    def pular():
        if estado["idx"] + 1 < len(etapas):
            estado["idx"] += 1
            estado["tempo"] = etapas[estado["idx"]]["duracao"]
            update_static_ui()
            refresh_ui()

    def alternar_pausa():
        estado["pausado"] = not estado["pausado"]
        controls_container.content = _controls_bar(retroceder, alternar_pausa, pular, estado["pausado"])
        controls_container.update()

    def voltar_config():
        estado["cancel"].set()
        navegar(page, tela_config)

    def on_finalizar():
        navegar(page, tela_finish, tempo_total(config, num_ciclos), num_ciclos)

    estado["task"] = asyncio.ensure_future(timer_loop())

    return ft.View(
        route="/timer", bgcolor=ft.Colors.SURFACE,
        appbar=ft.AppBar(title=ft.Text("Treino em Andamento", weight=ft.FontWeight.BOLD), center_title=True, bgcolor=ft.Colors.SURFACE,
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Cancelar treino", on_click=lambda _: voltar_config())),
        controls=[ft.SafeArea(content=ft.Column(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[txt_stats, badge_container, ring_area, txt_proximo, controls_container]))],
    )

def _controls_bar(retroceder, alternar_pausa, pular, pausado):
    return ft.Container(padding=ft.Padding(16, 16, 16, 16),
        content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=16, controls=[
            ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS, icon_size=32, tooltip="Anterior", on_click=lambda _: retroceder()),
            ft.FilledButton("⏸ PAUSAR" if not pausado else "▶ CONTINUAR",
                icon=ft.Icons.PAUSE if not pausado else ft.Icons.PLAY_ARROW,
                on_click=lambda _: alternar_pausa(),
                style=ft.ButtonStyle(padding=ft.Padding(24, 12, 24, 12), shape=ft.RoundedRectangleBorder(radius=12))),
            ft.IconButton(icon=ft.Icons.SKIP_NEXT, icon_size=32, tooltip="Pular", on_click=lambda _: pular()),
        ]))

# ==================== TELA 4: FINALIZAÇÃO ====================
def tela_finish(page: ft.Page, tempo_total_seg: int, num_ciclos: int):
    tempo_fmt = fmt(tempo_total_seg)

    def repetir(_):
        config = carregar()
        navegar(page, tela_timer, config, config["num_ciclos"])

    def configurar(_):
        navegar(page, tela_config)

    return ft.View(route="/finish", bgcolor=ft.Colors.SURFACE,
        controls=[ft.SafeArea(content=ft.Container(expand=True, alignment=ft.Alignment(0, 0), padding=32,
            content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=24, controls=[
                ft.Container(padding=24, border_radius=60, bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    content=ft.Icon(ft.Icons.EMOJI_EVENTS, size=64, color=ft.Colors.ON_SECONDARY_CONTAINER)),
                ft.Text("Treino Concluído! ", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE, text_align=ft.TextAlign.CENTER),
                ft.Text(f"Você completou {num_ciclos} ciclo{'s' if num_ciclos > 1 else ''} em {tempo_fmt}",
                    size=16, color=ft.Colors.ON_SURFACE_VARIANT, text_align=ft.TextAlign.CENTER),
                ft.Container(padding=ft.Padding(16, 16, 16, 16), border_radius=16, bgcolor=ft.Colors.SURFACE_CONTAINER,
                    content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
                        _stat("TEMPO", tempo_fmt, ft.Colors.PRIMARY),
                        _stat("CICLOS", str(num_ciclos), ft.Colors.SECONDARY),
                        _stat("STATUS", "✅ OK", ft.Colors.TERTIARY),
                    ])),
                ft.Column(spacing=12, width=300, controls=[
                    ft.FilledButton("🔁 REPETIR TREINO", on_click=repetir,
                        style=ft.ButtonStyle(padding=ft.Padding(0, 16, 0, 16), shape=ft.RoundedRectangleBorder(radius=12)), expand=True),
                    ft.OutlinedButton("⚙ VOLTAR À CONFIGURAÇÃO", on_click=configurar,
                        style=ft.ButtonStyle(padding=ft.Padding(0, 16, 0, 16), shape=ft.RoundedRectangleBorder(radius=12)), expand=True),
                ]),
            ])))])


# ==================== ENTRY POINT ====================
async def main(page: ft.Page):
    page.title = "HIIT Timer"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed="#9C27B0", use_material3=True)

    def on_view_pop(e: ft.ViewPopEvent):
        if page.route in ["/timer", "/editor", "/finish"]:
            navegar(page, tela_config)
        else:
            e.prevent_default = False
            return
        e.prevent_default = True

    page.on_view_pop = on_view_pop
    navegar(page, tela_config)

if __name__ == "__main__":
    ft.run(main)