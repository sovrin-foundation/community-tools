from aiohttp import web
import os
from dotenv import load_dotenv

async def index(request):
    load_dotenv()

    REDIRECT = os.environ.get('REDIRECT')
    REDIRECT_URL = os.environ.get('REDIRECT_URL')

    if REDIRECT == 'True':
        return web.HTTPTemporaryRedirect(REDIRECT_URL)
    else:
        return web.FileResponse('./static/endorser.html')
