# bootstraps the application
# copyright (c) 2018 wildduck.io


from app_src import app


if __name__ == '__main__':
    debug = app.config['DEBUG']
    host = app.config['HOST']
    app.run(debug=debug, host=host)
