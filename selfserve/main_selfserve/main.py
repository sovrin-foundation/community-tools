import asyncio
from aiohttp import web
from routes import setup_routes
from routes import setup_static_routes

app = web.Application()
app['pool_lock'] = asyncio.Lock()
setup_routes(app)
setup_static_routes(app)
web.run_app(app, host='localhost', port=8080)
