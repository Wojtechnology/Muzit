import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

# First web app
# Going to remake into Street Muse (Music Reddit)

from tornado.options import define, options
define("port", default = 8000, help = "run on the given port", type = int)

# Imagine I knew what this did LOL

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		greeting = self.get_argument('greeting', 'Hello')
		self.write(greeting + ', friendly user!')

# Only run this if it was ran as the main file

if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers = [(r"/", IndexHandler)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()