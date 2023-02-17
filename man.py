#qpy:webapp:я живой!
#qpy://127.0.0.1:8080/
"""
ну как-то так
"""
from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template

######### веб сервак ###############
class MyWSGIRefServer(ServerAdapter):
    server = None
    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        import threading
        threading.Thread(target=self.server.shutdown).start()
        self.server.server_close()

######### роутерсы ###############
@route('/__exit', method=['GET','HEAD'])
def __exit():
    global server
    server.stop()

@route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='/sdcard')


######### роутерс сайт код ###############
@route('/')
def home():
    return template('<h1>САЙТ РАБОТАЕТ {{name}} !</h1><a href="HTMLstroke/index.html">:домашняя страница:</a><br /><br /> <a href="HTMLstroke/sss.html">>>СПИСОК АДМИНОВ ПО РАНГУ </a>',name='404')

######### ROUTERS ###############
app = Bottle()
app.route('/', method='GET')(home)
app.route('/__exit', method=['GET','HEAD'])(__exit)
app.route('/assets/<filepath:path>', method='GET')(server_static)
############### на ешглише проще,########
try:
    server = MyWSGIRefServer(host="127.0.0.1", port="8080")
    app.run(server=server,reloader=False)
except Exception as ex:
    errs = "Exception: %s" % repr(ex)
    print(errs)
