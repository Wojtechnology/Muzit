import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

# First web app
# Only makes poems for now :(

from tornado.options import define, options
define("port", default = 8000, help = "run on the given port", type = int)

# This shit makes some poems bruh

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

class PoemPageHandler(tornado.web.RequestHandler):
	def post(self):
		noun1 = self.get_argument('noun1')
		noun2 = self.get_argument('noun2')
		verb = self.get_argument('verb')
		noun3 = self.get_argument('noun3')
		self.render('poem.html', roads = noun1, wood = noun2, made = verb, difference = noun3)

class BookPageHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"book.html",
			title = "Home Page",
			header = "Books that are great",
			books = [
				"Learning Python",
				"Programming Collective Intelligence",
				"Restful Web Services"
				]
			)

# Only run this if it was ran as the main file

if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers = [
			(r"/", IndexHandler),
			(r"/poem", PoemPageHandler),
			(r"/book", BookPageHandler)
		],
		template_path = os.path.join(os.path.dirname(__file__), "templates")
	)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()