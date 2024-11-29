from flask import Flask

def create_app():
    app = Flask (__name__)
    app.config['SECRET_KEY'] = 'vrr6tyufgyfxtr vhjgcye56ryfutyte4we56ry sw454nbjghj bhgydr67yufyrt'

    from .views import views
    app.register_blueprint (views, url_prefix='/')

    return app