from babel import Locale
from fastapi import Request, Response
from fastapi_babel import BabelMiddleware #type: ignore
from fastapi_babel.core import Babel, _context_var #type: ignore
from starlette.middleware.base import RequestResponseEndpoint
from typing import Optional

class MultiLingualMiddleware(BabelMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
        locale: Optional[str] = None
    ) -> Response:
        """dispatch function

        Args:
            request (Request): ...
            call_next (RequestResponseEndpoint): ...

        Returns:
            Response: ...
        """
        lang_code = request.cookies.get('CurLang', None)
        if lang_code:
            locale = repr(Locale(lang_code.lower()))
        else:
            locale = request.headers.get("Accept-Language")
        
        request.state.babel = Babel(configs=self.babel_configs)
        request.state.babel.locale = self.get_language(request.state.babel, locale)
        _context_var.set(
            request.state.babel.gettext
        )
        if self.jinja2_templates:
            request.state.babel.install_jinja(self.jinja2_templates)

        response: Response = await call_next(request)
        return response
