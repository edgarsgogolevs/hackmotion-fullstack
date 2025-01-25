import os
import logging
import traceback
import json

from modules import setup_logger
from modules import analytics

lg = logging.getLogger()
setup_logger.init_log(lg)

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home_page():
  return "OK"


@app.route("/user_data/<string:uid>", methods=["GET"])
def user_data_page(uid: str):
  return "Ok " + uid


@app.route("/register_event/server", methods=["POST"])
def register_server_event():
  try:
    data = request.get_json(force=True)
  except Exception:
    lg.warning("JSON validatio error", exc_info=True)
    return "JSON validation error", 400
  if analytics.register_server_event(data):
    return "Saved", 201
  return "Unknown error", 500


@app.route("/register_event/client", methods=["POST"])
def register_client_event():
  try:
    data = request.get_json(force=True)
  except Exception:
    lg.warning("JSON validatio error", exc_info=True)
    return "JSON validation error", 400
  lg.info(f"Client event data: {data}")
  return "OK"


@app.errorhandler(500)
def server_error(_):
  lg.critical(traceback.format_exc())
  return {'error': 'Processing error'}, 500


# run developement server
if __name__ == '__main__':
  # run debug app
  app.run(debug=True, port=int(os.getenv("PORT", 8080)))
