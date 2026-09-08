"""Tela do Cronômetro Ativo (Otimizado — Granular Updates)"""

import flet as ft
import asyncio
from workout import fmt
from components.top_stats import TopStats, ProximoExercicioBanner
from components.controls_bar import ControlsBar


def TimerScreen(page: ft.Page, etapas, indice_inicial=0, on_finalizar=None, on_voltar_config=None):
    estado = {
        "idx": indice_inicial,
        "tempo": etapas[indice_inicial].duracao if etapas else 0,
        "pausado": False,
        "finalizado": False,
        "task": None,
        "cancel": asyncio.Event(),
    }
    
    # Manter tela ativa durante o treino (Wake Lock)
    try:
        if hasattr(page, 'keep_screen_on'):
            page.keep_screen_on = True
    except Exception:
        pass
    
    def _cleanup_wake_lock():
        try:
            if hasattr(page, 'keep_screen_on'):
                page.keep_screen_on = False
        except Exception:
            pass
    
    # Controles mutáveis
    txt_nome = ft.Text("", size=22, weight=ft.FontWeight.W_600, color=ft.Colors.ON_SURFACE, text_align=ft.TextAlign.CENTER, max_lines=2)
    txt_tempo = ft.Text("", size=56, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE, font_family="RobotoMono")
    ring_progress = ft.ProgressRing(value=0.0, width=280, height=280, stroke_width=14, bgcolor=ft.Colors.TRANSPARENT)
    ring_track = ft.ProgressRing(value=1.0, width=280, height=280, stroke_width=14, bgcolor=ft.Colors.TRANSPARENT)
    
    txt_badge = ft.Text("", size=12, weight=ft.FontWeight.BOLD)
    badge_container = ft.Container(padding=ft.Padding(16, 6, 16, 6), margin=ft.Margin(0, 0, 0, 16), border_radius=20, content=txt_badge)
    
    top_stats_container = ft.Container()
    banner_container = ft.Container()
    controls_container = ft.Container()

    ring_stack = ft.Stack(width=280, height=280, controls=[ring_track, ring_progress])
    centro = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4, controls=[txt_nome, txt_tempo])
    ring_area = ft.Container(
        content=ft.Stack(width=280, height=280, controls=[
            ring_stack,
            ft.Container(content=centro, alignment=ft.Alignment(0, 0), width=280, height=280),
        ]),
        alignment=ft.Alignment(0, 0), expand=True,
        padding=ft.Padding(24, 16, 24, 16),
    )

    # Cores por tipo
    _CORES = {
        "exercicio": ("#9C27B0", "#4A148C", ft.Colors.PRIMARY_CONTAINER, ft.Colors.ON_PRIMARY_CONTAINER, "EXERCÍCIO"),
        "descanso": ("#FF9800", "#E65100", ft.Colors.SECONDARY_CONTAINER, ft.Colors.ON_SECONDARY_CONTAINER, "DESCANSO"),
        "descanso_ciclo": ("#FF9800", "#E65100", ft.Colors.SECONDARY_CONTAINER, ft.Colors.ON_SECONDARY_CONTAINER, "DESCANSO"),
    }

    def update_static_ui():
        """Atualiza apenas os componentes que mudam quando a ETAPA muda, não a cada segundo."""
        idx = estado["idx"]
        if idx >= len(etapas): 
            return
        ep = etapas[idx]
        prox = etapas[idx + 1] if idx + 1 < len(etapas) else None

        cr, cf, badge_bg, badge_fg, badge_label = _CORES.get(ep.tipo, _CORES["exercicio"])
        
        # Badge
        txt_badge.value = badge_label
        txt_badge.color = badge_fg
        badge_container.bgcolor = badge_bg
        txt_badge.update()
        badge_container.update()

        # Top stats
        tempo_total_restante = sum(e.duracao for e in etapas[idx:]) - ep.duracao + estado["tempo"]
        ciclo_atual = ep.ciclo
        total_ciclos = max(e.ciclo for e in etapas)
        top_stats_container.content = TopStats(
            tempo_total_fmt=fmt(sum(e.duracao for e in etapas)),
            ciclo_atual=ciclo_atual, total_ciclos=total_ciclos,
            etapa_atual=idx + 1, total_etapas=len(etapas),
            tempo_restante_fmt=fmt(tempo_total_restante),
        )
        top_stats_container.update()

        # Banner
        if prox:
            banner_container.content = ProximoExercicioBanner(prox.nome, prox.emoji, prox.tipo)
        else:
            banner_container.content = ft.Container(height=56)
        banner_container.update()

        # Controls
        controls_container.content = ControlsBar(
            retroceder, alternar_pausa, pular, estado["pausado"]
        )
        controls_container.update()

    def refresh_ui():
        """Chamada a cada 1s. Atualiza APENAS o que muda a cada segundo."""
        idx = estado["idx"]
        tempo = estado["tempo"]
        if idx >= len(etapas): 
            return
        ep = etapas[idx]
        cr, cf, _, _, _ = _CORES.get(ep.tipo, _CORES["exercicio"])
        
        ring_progress.color = cr
        ring_track.color = cf
        progresso = max(0.0, min(1.0, 1.0 - (tempo / ep.duracao))) if ep.duracao > 0 else 0.0
        ring_progress.value = progresso
        
        txt_nome.value = ep.nome
        txt_tempo.value = fmt(tempo)

        # UPDATE GRANULAR: Apenas os controles que mudam a cada segundo
        txt_tempo.update()
        ring_progress.update()

    async def timer_loop():
        update_static_ui()  # Build inicial completo
        refresh_ui()        # Timer inicial
        
        while not estado["cancel"].is_set() and estado["idx"] < len(etapas):
            if not estado["pausado"]:
                await asyncio.sleep(1)
                if estado["cancel"].is_set():
                    break
                estado["tempo"] -= 1
                if estado["tempo"] <= 0:
                    await avancar()
                else:
                    refresh_ui()  # ← GRANULAR: só txt_tempo + ring_progress
            else:
                await asyncio.sleep(0.1)
        
        if estado["idx"] >= len(etapas) and not estado["finalizado"]:
            estado["finalizado"] = True
            _cleanup_wake_lock()
            if on_finalizar:
                on_finalizar()

    async def avancar():
        try:
            page.window.vibrate(200)
        except Exception:
            pass
        
        if estado["idx"] + 1 < len(etapas):
            estado["idx"] += 1
            estado["tempo"] = etapas[estado["idx"]].duracao
            update_static_ui()  # Nova etapa = update completo dos estáticos
            refresh_ui()        # Timer inicial da nova etapa
        else:
            estado["finalizado"] = True
            if on_finalizar:
                on_finalizar()

    def retroceder():
        if estado["idx"] > 0:
            estado["idx"] -= 1
            estado["tempo"] = etapas[estado["idx"]].duracao
            update_static_ui()
            refresh_ui()
        elif on_voltar_config:
            _cleanup_wake_lock()
            on_voltar_config()

    def pular():
        if estado["idx"] + 1 < len(etapas):
            estado["idx"] += 1
            estado["tempo"] = etapas[estado["idx"]].duracao
            update_static_ui()
            refresh_ui()

    def alternar_pausa():
        estado["pausado"] = not estado["pausado"]
        controls_container.content = ControlsBar(
            retroceder, alternar_pausa, pular, estado["pausado"]
        )
        controls_container.update()

    # Iniciar loop
    estado["task"] = asyncio.ensure_future(timer_loop())

    # Window ops (Android-safe)
    try:
        page.window.full_screen = True
        page.window.prevent_close = True
    except Exception:
        pass

    return ft.View(
        route="/timer", bgcolor=ft.Colors.SURFACE,
        controls=[ft.SafeArea(content=ft.Column(
            expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[top_stats_container, banner_container, ring_area, badge_container, controls_container],
        ))],
    )