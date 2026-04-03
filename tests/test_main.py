import asyncio

def test_app_lifespan_initializes_runtime(monkeypatch):
    from app import main

    calls = {"count": 0}

    def fake_init_runtime():
        calls["count"] += 1

    monkeypatch.setattr(main, "init_runtime", fake_init_runtime)
    app = main.create_app()

    async def run_lifespan():
        async with app.router.lifespan_context(app):
            return None

    asyncio.run(run_lifespan())

    assert calls["count"] == 1
