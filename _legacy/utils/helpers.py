"""
Funções utilitárias compartilhadas.
"""

import asyncio
from typing import Callable, Awaitable


async def run_with_cancellation(
    coro: Awaitable,
    cancel_event: asyncio.Event,
    on_cancel: Callable | None = None
) -> any:
    """
    Executa uma corrotina com suporte a cancelamento via Event.
    
    Args:
        coro: Corrotina para executar
        cancel_event: Event que sinaliza cancelamento
        on_cancel: Callback opcional ao cancelar
        
    Returns:
        Resultado da corrotina ou None se cancelado
    """
    task = asyncio.create_task(coro)
    
    try:
        # Aguarda either a task terminar ou o cancel_event ser setado
        done, pending = await asyncio.wait(
            [task, asyncio.create_task(cancel_event.wait())],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        if cancel_event.is_set():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            if on_cancel:
                on_cancel()
            return None
        
        return task.result()
        
    except Exception:
        task.cancel()
        raise


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Limita um valor entre min e max."""
    return max(min_val, min(value, max_val))


def lerp(a: float, b: float, t: float) -> float:
    """Interpolação linear entre a e b."""
    return a + (b - a) * t