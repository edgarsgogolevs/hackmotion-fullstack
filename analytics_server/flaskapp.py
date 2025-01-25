import os
import logging
import traceback
import json

from modules import setup_logger
from modules import analytics

lg = logging.getLogger()
setup_logger.init_log(lg)

from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/static/<path:filename>")
def static_dir(filename):
  return send_from_directory(app.static_folder, filename)


@app.route("/", methods=["GET"])
def home_page():
  data = analytics.get_users_page_view_data()
  total_views = analytics.get_total_page_views()
  return render_template("index.html", data=data, total_views=total_views)


@app.route("/user_data/<string:uid>", methods=["GET"])
def user_data_page(uid: str):
  return render_template("user_data.html", **analytics.get_user_summary(uid))


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
  if analytics.register_client_event(data):
    return "OK", 201
  return "Unknown error", 500


@app.errorhandler(500)
def server_error(_):
  lg.critical(traceback.format_exc())
  return {'error': 'Processing error'}, 500


# run developement server
if __name__ == '__main__':
  # run debug app
  app.run(debug=True, port=int(os.getenv("PORT", 8080)))
