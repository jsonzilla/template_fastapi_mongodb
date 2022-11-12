import asyncio
from uvicorn import Config, Server


class ProactorServer(Server):
    def run(self, sockets=None):
        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)
        asyncio.run(self.serve(sockets=sockets))


if __name__ == "__main__":
    config = Config(app="app.main:app", host="0.0.0.0", port=80, reload=True)
    server = ProactorServer(config=config)
    server.run()
