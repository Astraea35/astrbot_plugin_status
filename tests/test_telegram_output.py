import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "_status_telegram_test"
package = type(sys)(PACKAGE)
package.__path__ = [str(ROOT)]
sys.modules[PACKAGE] = package
module_spec = importlib.util.spec_from_file_location(
    PACKAGE + ".core.status_service",
    ROOT / "core/status_service.py",
)
module = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(module)


@pytest.mark.asyncio
async def test_telegram_status_uses_metrics_text_without_rendering():
    renderer = SimpleNamespace(
        build_status_text=AsyncMock(return_value="CPU 10%\nMemory 20%"),
        render_status_image=AsyncMock(),
    )
    service = module.StatusService(
        config_manager=SimpleNamespace(llm_analysis=SimpleNamespace(enabled=False)),
        context=SimpleNamespace(),
        html_renderer=renderer,
    )
    event = SimpleNamespace(
        get_platform_name=lambda: "telegram",
        plain_result=lambda text: text,
    )
    assert [result async for result in service.show_status(event)] == [
        "CPU 10%\nMemory 20%"
    ]
    renderer.render_status_image.assert_not_awaited()
