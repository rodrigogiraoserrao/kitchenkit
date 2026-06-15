from contextvars import ContextVar


started_at: ContextVar[float | None] = ContextVar("started_at", default=None)
ingredients: ContextVar[int] = ContextVar("ingredients", default=0)
