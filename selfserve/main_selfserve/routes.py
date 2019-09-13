from views import index
from nym import handle_nym_req

PROJECT_ROOT=""

def setup_routes(app):
    app.router.add_post('/nym', handle_nym_req)
    app.router.add_get('/', index)

def setup_static_routes(app):
    app.router.add_static('/static/',
                          path=PROJECT_ROOT + 'static',
                          name='static')
