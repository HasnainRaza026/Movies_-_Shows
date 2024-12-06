import eventlet
from website import create_app

app = create_app()

if __name__ == '__main__':
    from eventlet import wsgi
    wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app)

