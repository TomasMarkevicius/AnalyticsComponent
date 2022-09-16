import asyncio
from tornado.web import Application, RequestHandler
from analyticscomponent.handlers.api_handlers import AnalyticsReportHandler
import logging
from analyticscomponent import cfg


PORT = cfg["Port"]
DOCS_PATH = "../templates/docs.html"

logger = logging.getLogger(__name__)


def init():
    logging.basicConfig(level=cfg["Log_Level"])


class DocsHandler(RequestHandler):
    async def get(self):
        self.render(DOCS_PATH)


class WebApp(Application):
    def __init__(self):
        self.app_handlers = [
            (r"/docs", DocsHandler),
            (r"/report", AnalyticsReportHandler),
        ]
        super(WebApp, self).__init__(self.app_handlers)


def make_app():
    return WebApp()


async def main():
    init()
    logger.info("Starting analytics component")
    app = make_app()
    app.listen(PORT)
    logger.info(f"Analytics component is running on port {PORT}")
    await asyncio.Event().wait()
