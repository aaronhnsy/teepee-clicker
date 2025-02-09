from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin, SwaggerRenderPlugin


__all__ = ["openapi_config"]


openapi_config: OpenAPIConfig = OpenAPIConfig(
    title="teepee-clicker",
    version="1.0.0",
    path="/schema",
    render_plugins=[
        SwaggerRenderPlugin(),
        ScalarRenderPlugin(),
    ],
)
