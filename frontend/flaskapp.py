import os
import logging
from modules import setup_logger

lg = logging.getLogger()
setup_logger.init_log(lg)

from flask import Flask, send_from_directory, render_template, request, make_response

app = Flask(__name__)


@app.route("/")
def landing_page():
  # TODO: register page view
  resp = make_response(render_template("index.html"))
  resp.set_cookie()
  return resp


@app.route("/static/<path:filename>")
def static_dir(filename):
  return send_from_directory(app.static_folder, filename)


# run developement server
if __name__ == '__main__':
  # run debug app
  app.run(debug=True, port=os.getenv("PORT"))
