from typing import Callable, Coroutine, Any

from aiogram import Dispatcher, BaseMiddleware, Router
from aiogram.handlers import ErrorHandler
from aiogram.filters import ExceptionTypeFilter

class TGBot:

    def __init__(self,
                 middlewares: list[type[BaseMiddleware]],
                 routers: list[Router],
                 exc_handlers: list[tuple[type[ErrorHandler], tuple[type[Exception], ...]]],
                 on_startup: Callable[..., Coroutine[Any, Any, None]],
                 on_shutdown: Callable[..., Coroutine[Any, Any, None]]):
        
        self.dp = Dispatcher()
        self.middlewares = middlewares
        self.routers = routers
        self.exc_handlers = exc_handlers
        self.on_startup = on_startup
        self.on_shutdown = on_shutdown

    def _add_middlewares(self):
        for m in self.middlewares:
            self.dp.update.middleware(m())

    def _add_routers(self):
        self.dp.include_routers(*self.routers)

    def _add_exc_handlers(self):
        for handler, exc_types in self.exc_handlers:
            self.dp.errors.register(handler, ExceptionTypeFilter(*exc_types))
    
    def _register_functions(self):
        self.dp.startup.register(self.on_startup)
        self.dp.shutdown.register(self.on_shutdown)

    def init(self) -> Dispatcher:
        self._add_middlewares()
        self._add_exc_handlers()
        self._add_routers()
        self._register_functions()

        return self.dp