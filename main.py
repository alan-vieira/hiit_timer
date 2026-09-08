"""HIIT Timer - Aplicação Principal (v1.1.4 - Correção Tela Preta)."""
import flet as ft
from screens.config_screen import ConfigScreen
from screens.exercise_editor_screen import ExerciseEditorScreen
from screens.finish_screen import FinishScreen
from screens.timer_screen import TimerScreen
from store import store


def navegar(page: ft.Page, rota: str):
    """Navegação segura, centralizada e sem warnings de depreciação."""
    page.route = rota
    page.update()


def on_route_change(e: ft.RouteChangeEvent):
    """Gerenciador central de rotas. Limpa a pilha para evitar 'telas pretas'."""
    page = e.page
    page.views.clear()

    if page.route == "/editor":
        page.views.append(
            ExerciseEditorScreen(
                page=page,
                on_save=lambda: navegar(page, "/config"),
                on_cancel=lambda: navegar(page, "/config"),
            )
        )
    elif page.route == "/timer":
        page.views.append(
            TimerScreen(
                page=page,
                etapas=store.etapas,
                on_finalizar=lambda: navegar(page, "/finish"),
                on_voltar_config=lambda: navegar(page, "/config"),
            )
        )
    elif page.route == "/finish":
        page.views.append(
            FinishScreen(
                page=page,
                tempo_total_seg=store.tempo_total_seg,
                num_ciclos=store.num_ciclos,
                on_repetir=lambda: navegar(page, "/timer"),
                on_configurar=lambda: navegar(page, "/config"),
            )
        )
    else:
        # Rota Raiz (Default): ConfigScreen
        page.views.append(
            ConfigScreen(
                page=page,
                on_iniciar=lambda nc: navegar(page, "/timer"),
                num_ciclos_inicial=store.num_ciclos,
                on_navegar_editor=lambda: navegar(page, "/editor"),
            )
        )
        page.route = "/config"

    page.update()


def on_view_pop(e: ft.ViewPopEvent):
    """Intercepta o botão físico 'Voltar' do Android."""
    page = e.page
    if page.route in ["/timer", "/editor", "/finish"]:
        navegar(page, "/config")
    else:
        e.prevent_default = False
        return
    e.prevent_default = True


async def main(page: ft.Page):
    page.title = "HIIT Timer"
    page.theme_mode = ft.ThemeMode.DARK

    # CRUCIAL: Anexa a página ao store para carregar dados salvos
    store.attach_page(page)

    page.on_route_change = on_route_change
    page.on_view_pop = on_view_pop

    navegar(page, "/config")


# ⚠️ ESTA LINHA É A ÚNICA CAUSA DA TELA PRETA ⚠️
# Tem que ter EXATAMENTE dois underscores de cada lado: __name__ e __main__
if __name__ == "__main__":
    ft.run(main, assets_dir="assets")