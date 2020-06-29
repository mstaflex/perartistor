import tornado.ioloop
import tornado.web
import argparse
import os
import datetime
import logging


def get_datetime():
    now = datetime.datetime.now()
    day = now.strftime("%Y%m%d")
    t = now.strftime("%H%M%S")
    return day, t


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, path):
       self.path = path

    def post(self):
        cipher = self.get_argument('cipher', None)
        day, t = get_datetime()
        if self.request.files.get('uploadfile', None):
            uploadFile = self.request.files['uploadfile'][0]
            filename = uploadFile['filename']
            file_folder_path = os.path.join(self.path, day)
            os.makedirs(file_folder_path, mode=0o750, exist_ok=True)
            with open(os.path.join(file_folder_path, "{}_{}".format(t, filename)), 'wb') as fileObj:
                fileObj.write(uploadFile['body'])


def make_app(args):
    return tornado.web.Application([
        (r"/{}".format(args.token), MainHandler, {'path': args.path}),
    ])


def main(args):
    if not os.path.isdir(args.path):
        logging.error("Given path doesn't exist!")
        return

    app = make_app(args)
    app.listen(args.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Webserver for personal artifact storage micro service.')
    parser.add_argument('--port', action="store", default=8888, help="Port for webserver.")
    parser.add_argument('--token', required=True, action="store", help="Token for secret access.")
    parser.add_argument('--path', action="store", default="", help="Path to store artifacts.")
    args = parser.parse_args()
    main(args)
