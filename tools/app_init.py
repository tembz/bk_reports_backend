from typing import Callable, TypeAlias, Optional

from fastapi import FastAPI, APIRouter
from starlette.middleware.base import BaseHTTPMiddleware

ExcHandler: TypeAlias = tuple[type[Exception], Callable]

class App:

    def __init__(self,
                 middlewares: list[type[BaseHTTPMiddleware]],
                 routers: list[APIRouter],
                 exc_handlers: list[ExcHandler],
                 lifespan: Optional[Callable] = None):
        
        self.app = FastAPI(lifespan=lifespan)
        self.middlewares = middlewares
        self.routers = routers
        self.exc_handlers = exc_handlers

    def _add_middlewares(self):
        for m in self.middlewares:
            self.app.add_middleware(m)
    
    def _add_routers(self):
        for h in self.routers:
            self.app.include_router(h)

    def _add_exc_handlers(self):
        for e in self.exc_handlers:
            self.app.add_exception_handler(e[0], e[1])

    def init(self) -> FastAPI:
        self._add_middlewares()
        self._add_exc_handlers()
        self._add_routers()
        return self.app