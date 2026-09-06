"""
Tela do Cronômetro Ativo.
"""

import flet as ft
import asyncio
from workout import fmt
from components.ring_timer import RingTimer
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

    # Controles mutáveis
    txt_nome = ft.Text("", size=22, weight=ft.FontWeight.W_600, color=ft.Colors.ON_SURFACE, text_align=ft.TextAlign.CENTER, max_lines=2)
    txt_tempo = ft.Text("", size=56, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE, font_family="RobotoMono")
    ring_progress = ft.ProgressRing(value=0.0, width=280, height=280, stroke_width=14, bgcolor=ft.Colors.TRANSPARENT)
    ring_track = ft.ProgressRing(value=1.0, width=280, height=280, stroke_width=14, bgcolor=ft.Colors.TRANSPARENT)
    txt_badge = ft.Text("", size=12, weight=ft.FontWeight.BOLD)
    badge_container = ft.Container(padding=ft.padding.Padding.symmetric(horizontal=16, vertical=6), margin=ft.margin.Margin(left=0, top=0, right=0, bottom=16), border_radius=20, content=txt_badge)
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
        padding=ft.padding.Padding.symmetric(horizontal=24, vertical=16),
    )

    def refresh_ui():
        idx = estado["idx"]
        tempo = estado["tempo"]
        if idx >= len(etapas):
            return
        ep = etapas[idx]
        prox = etapas[idx + 1] if idx + 1 < len(etapas) else None

        # Cores do ring
        cores = {"exercicio": ("#9C27B0", "#4A148C"), "descanso": ("#FF9800", "#E65100"), "descanso_ciclo": ("#FF9800", "#E65100")}
        cr, cf = cores.get(ep.tipo, ("#9C27B0", "#4A148C"))
        ring_progress.color = cr
        ring_track.color = cf
        progresso = 1.0 - (tempo / ep.duracao) if ep.duracao > 0 else 0.0
        ring_progress.value = max(0.0, min(1.0, progresso))

        txt_nome.value = ep.nome
        txt_tempo.value = fmt(tempo)

        # Badge
        if ep.tipo == "exercicio":
            txt_badge.value = "EXERCÍCIO"
            txt_badge.color = ft.Colors.ON_PRIMARY_CONTAINER
            badge_container.bgcolor = ft.Colors.PRIMARY_CONTAINER
        else:
            txt_badge.value = "DESCANSO"
            txt_badge.color = ft.Colors.ON_SECONDARY_CONTAINER
            badge_container.bgcolor = ft.Colors.SECONDARY_CONTAINER

        # Top stats
        tempo_total_restante = sum(e.duracao for e in etapas[idx:]) - ep.duracao + tempo
        ciclo_atual = ep.ciclo
        total_ciclos = max(e.ciclo for e in etapas)
        top_stats_container.content = TopStats(
            tempo_total_fmt=fmt(sum(e.duracao for e in etapas)),
            ciclo_atual=ciclo_atual, total_ciclos=total_ciclos,
            etapa_atual=idx + 1, total_etapas=len(etapas),
            tempo_restante_fmt=fmt(tempo_total_restante),
        )

        # Banner
        if prox:
            banner_container.content = ProximoExercicioBanner(prox.nome, prox.emoji, prox.tipo)
        else:
            banner_container.content = ft.Container(height=56)

        # Controls
        controls_container.content = ControlsBar(
            on_voltar=retroceder, on_pausar=alternar_pausa, on_pular=pular,
            esta_pausado=estado["pausado"],
        )
        page.update()

    async def timer_loop():
        while not estado["cancel"].is_set() and estado["idx"] < len(etapas):
            if not estado["pausado"]:
                await asyncio.sleep(1)
                if estado["cancel"].is_set():
                    break
                estado["tempo"] -= 1
                if estado["tempo"] <= 0:
                    await avancar()
                else:
                    refresh_ui()
            else:
                await asyncio.sleep(0.1)
        if estado["idx"] >= len(etapas) and not estado["finalizado"]:
            estado["finalizado"] = True
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
            refresh_ui()
        else:
            estado["finalizado"] = True
            if on_finalizar:
                on_finalizar()

    def retroceder():
        if estado["idx"] > 0:
            estado["idx"] -= 1
            estado["tempo"] = etapas[estado["idx"]].duracao
            refresh_ui()
        elif on_voltar_config:
            on_voltar_config()

    def pular():
        if estado["idx"] + 1 < len(etapas):
            estado["idx"] += 1
            estado["tempo"] = etapas[estado["idx"]].duracao
            refresh_ui()

    def alternar_pausa():
        estado["pausado"] = not estado["pausado"]
        refresh_ui()

    # Iniciar loop
    refresh_ui()
    estado["task"] = asyncio.ensure_future(timer_loop())

    # Window operations only work on desktop; wrap in try/except for Android compatibility
    try:
        page.window.full_screen = True
        page.window.prevent_close = True
    except Exception:
        pass  # Ignored on mobile/Android where window operations are not supported

    return ft.View(
        route="/timer", bgcolor=ft.Colors.SURFACE,
        controls=[ft.SafeArea(content=ft.Column(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
            top_stats_container, banner_container, ring_area, badge_container, controls_container,
        ]))],
    )