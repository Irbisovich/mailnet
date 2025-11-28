from emailtools.server.emailrequests import route, start_all_handlers
import asyncio

@route(
    email='your_email',
    password='your_password',
    page='/',
    toret=[200, 'OK']
)
def hello_wwworld():
    return '<h1>Hello, WWWorld!</h1>'

asyncio.run(start_all_handlers())
