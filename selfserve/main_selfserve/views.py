from aiohttp import web


async def index(request):
    web.FileResponse('./static/endorser.html')
