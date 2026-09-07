"""HIIT Timer - Aplicação Principal (Refatorado v1.1.0)"""

import flet as ft
import asyncio

from screens.config_screen import ConfigScreen
from screens.timer_screen import TimerScreen
from screens.finish_screen import FinishScreen
from screens.exercise_editor_screen import ExerciseEditorScreen
from store import store


def build_theme():
    return ft.Theme(
        color_scheme_seed=ft.Colors.INDIGO,
        use_material3=True,
        text_theme=ft.TextTheme(
            display_large=ft.TextStyle(size=32, weight=ft.FontWeight.BOLD),
            headline_medium=ft.TextStyle(size=24, weight=ft.FontWeight.W_600),
            title_large=ft.TextStyle(size=20, weight=ft.FontWeight.W_500),
            body_large=ft.TextStyle(size=16),
            body_medium=ft.TextStyle(size=14),
            label_small=ft.TextStyle(size=12),
        ),
    )


def build_dark_theme():
    return ft.Theme(
        color_scheme_seed=ft.Colors.INDIGO,
        use_material3=True,
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.INDIGO,
            on_primary=ft.Colors.WHITE,
            primary_container=ft.Colors.INDIGO_100,
            on_primary_container=ft.Colors.INDIGO_900,
            secondary=ft.Colors.ORANGE,
            on_secondary=ft.Colors.WHITE,
            secondary_container=ft.Colors.ORANGE_100,
            on_secondary_container=ft.Colors.ORANGE_900,
            tertiary=ft.Colors.PURPLE,
            on_tertiary=ft.Colors.WHITE,
            tertiary_container=ft.Colors.PURPLE_100,
            on_tertiary_container=ft.Colors.PURPLE_900,
            surface=ft.Colors.GREY_900,
            on_surface=ft.Colors.WHITE,
            surface_container=ft.Colors.GREY_800,
            surface_container_high=ft.Colors.GREY_800,
            surface_container_highest=ft.Colors.GREY_700,
            surface_container_low=ft.Colors.GREY_800,
            surface_container_lowest=ft.Colors.GREY_900,
            outline=ft.Colors.GREY_600,
            outline_variant=ft.Colors.GREY_700,
            error=ft.Colors.RED_400,
            on_error=ft.Colors.WHITE,
            error_container=ft.Colors.RED_900,
            on_error_container=ft.Colors.RED_100,
        ),
        text_theme=ft.TextTheme(
            display_large=ft.TextStyle(size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            headline_medium=ft.TextStyle(size=24, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
            title_large=ft.TextStyle(size=20, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
            body_large=ft.TextStyle(size=16, color=ft.Colors.WHITE),
            body_medium=ft.TextStyle(size=14, color=ft.Colors.GREY_300),
            label_small=ft.TextStyle(size=12, color=ft.Colors.GREY_400),
        ),
    )


# --- Navegação Centralizada ---
_current_timer_screen = None  # ref para cleanup


def _build_config_view(page: ft.Page):
    return ft.View(
        route="/",
        controls=[ft.SafeArea(ConfigScreen(
            page=page,
            on_iniciar=lambda nc: _navegar_timer(page, nc),
            num_ciclos_inicial=store.num_ciclos,
            on_navegar_editor=lambda: _navegar_editor(page),
        ))],
    )


def _build_timer_view(page: ft.Page, num_ciclos: int):
    global _current_timer_screen
    store.reiniciar_treino(num_ciclos)
    _current_timer_screen = TimerScreen(
        page=page,
        etapas=store.etapas,
        indice_inicial=0,
        on_finalizar=lambda: _navegar_finish(page),
        on_voltar_config=lambda: _navegar_config(page),
    )
    return ft.View(route="/timer", controls=[_current_timer_screen])


def _build_finish_view(page: ft.Page):
    return ft.View(
        route="/finish",
        controls=[ft.SafeArea(FinishScreen(
            page=page,
            tempo_total_seg=store.tempo_total_seg,
            num_ciclos=store.num_ciclos,
            on_repetir=lambda: _navegar_timer(page, store.num_ciclos),
            on_configurar=lambda: _navegar_config(page),
        ))],
    )


def _build_editor_view(page: ft.Page):
    return ft.View(
        route="/editor",
        controls=[ft.SafeArea(ExerciseEditorScreen(
            page=page,
            on_save=lambda: _navegar_config(page),
            on_cancel=lambda: _navegar_config(page),
        ))],
    )


def _navegar_config(page: ft.Page):
    page.views.clear()
    page.views.append(_build_config_view(page))
    page.update()


def _navegar_timer(page: ft.Page, num_ciclos: int):
    page.views.clear()
    page.views.append(_build_timer_view(page, num_ciclos))
    page.update()


def _navegar_finish(page: ft.Page):
    store.finalizar_treino()
    page.views.clear()
    page.views.append(_build_finish_view(page))
    page.update()


def _navegar_editor(page: ft.Page):
    page.views.append(_build_editor_view(page))
    page.update()


# --- Back Button / View Pop ---
async def _mostrar_confirmacao_saida(page: ft.Page) -> bool:
    """Retorna True se usuário confirmou sair"""
    confirmed = False
    
    def on_confirm(_):
        nonlocal confirmed
        confirmed = True
        page.close_dialog()
    
    def on_cancel(_):
        page.close_dialog()
    
    await page.show_dialog_async(ft.AlertDialog(
        modal=True,
        title=ft.Text("Sair do HIIT Timer?"),
        content=ft.Text("Seu progresso não será salvo."),
        actions=[
            ft.TextButton("CANCELAR", on_click=on_cancel),
            ft.FilledButton("SAIR", on_click=on_confirm),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    ))
    return confirmed


async def _mostrar_confirmacao_sair_timer(page: ft.Page) -> bool:
    """No timer: pausa + confirma"""
    # Pausar timer se rodando
    if _current_timer_screen and hasattr(_current_timer_screen, "estado"):
        _current_timer_screen.estado["pausado"] = True
    
    confirmed = False
    
    def on_confirm(_):
        nonlocal confirmed
        confirmed = True
        page.close_dialog()
    
    def on_cancel(_):
        # Retomar timer
        if _current_timer_screen and hasattr(_current_timer_screen, "estado"):
            _current_timer_screen.estado["pausado"] = False
        page.close_dialog()
    
    await page.show_dialog_async(ft.AlertDialog(
        modal=True,
        title=ft.Text("Sair do treino?"),
        content=ft.Text("O cronômetro será pausado. Deseja realmente sair?"),
        actions=[
            ft.TextButton("CONTINUAR TREINO", on_click=on_cancel),
            ft.FilledButton("SAIR E PERDER PROGRESSO", on_click=on_confirm),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    ))
    return confirmed


async def main(page: ft.Page):
    page.title = "HIIT Timer"
    page.theme_mode = ft.ThemeMode.DARK

    # 1. SPLASH SCREEN IMEDIATO — primeiro frame < 100ms
    splash = ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        bgcolor=ft.Colors.SURFACE,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            controls=[
                ft.ProgressRing(width=48, height=48, stroke_width=4, color=ft.Colors.PRIMARY),
                ft.Text("HIIT Timer", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE),
                ft.Text("Carregando...", size=14, color=ft.Colors.ON_SURFACE_VARIANT),
            ],
        ),
    )
    page.add(splash)
    page.update()  # Força renderização imediata do splash
    
    # 2. Setup pesado em background (não bloqueia UI)
    try:
        page.window.width = 400
        page.window.height = 850
        page.window.min_width = 360
        page.window.min_height = 700
        await page.window.center()
    except Exception:
        pass  # Ignorado no Android
    
    page.theme = build_theme()
    page.dark_theme = build_dark_theme()
    
    # 3. Anexar page ao store (para persistência futura)
    store.attach_page(page)
    
    # 4. Handler de Back Button para Android
    def on_back_button(e: ft.ViewPopEvent):
        if page.route == "/timer":
            _navegar_config(page)
            e.prevent_default = True  # Impede o fechamento do app
        elif page.route == "/editor":
            _navegar_config(page)
            e.prevent_default = True
        else:
            # Na tela inicial: permite o fechamento padrão do Android
            pass

    page.on_back_button = on_back_button

    # 5. Substituir splash pela tela real
    page.controls.clear()
    page.views.append(_build_config_view(page))
    page.update()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")