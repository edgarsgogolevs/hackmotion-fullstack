import os
import logging
from concurrent.futures import ThreadPoolExecutor
import traceback

from modules import setup_logger
from modules import analytics

lg = logging.getLogger()
setup_logger.init_log(lg)

NUM_WORKERS = int(os.getenv("ANALYTICS_WORKERS", 2))
lg.info(f"Creating thread pool with {NUM_WORKERS} workers..")
executor = ThreadPoolExecutor(max_workers=NUM_WORKERS)

from flask import Flask, send_from_directory, render_template, request, make_response, redirect

app = Flask(__name__)

HELP_BREAK_MAPPING = {
  "break-80": "break&nbsp;80",
  "break-90": "break&nbsp;90",
  "break-100": "break&nbsp;100",
  "break-par": "break&nbsp;par"
}


@app.route("/")
def default_route():
  return redirect("/break-80")


@app.route("/<string:help_break>")
def landing_page(help_break: str):
  if help_break == "":
    return redirect("/break-80")
  if help_break not in HELP_BREAK_MAPPING:
    return "Page not found", 404
  resp = make_response(render_template("index.html", help_break=HELP_BREAK_MAPPING[help_break]))
  try:
    uid = request.cookies.get(analytics.UID_COOKIE)
    if not uid:
      lg.info("Setting uid cookie")
      uid = analytics.create_user_id(request)
      resp.set_cookie(analytics.UID_COOKIE, uid, max_age=analytics.UID_COOKIE_MAX_AGE)
    executor.submit(analytics.send_analytics_data,
                    analytics.prepare_analytics_data_from_request(uid, request))
  except Exception:
    lg.error(f"Analytics error: ", exc_info=True)
  return resp


@app.route("/api/analytics", methods=["GET"])
def get_analytics_server_url():
  return {"url": analytics.CLIENT_EVENT_ENDPOINT}


@app.route("/static/<path:filename>")
def static_dir(filename):
  return send_from_directory(app.static_folder, filename)


@app.errorhandler(500)
def server_error(_):
  lg.critical(traceback.format_exc())
  return {'error': 'Processing error'}, 500


# run developement server
if __name__ == '__main__':
  # run debug app
  app.run(debug=True, port=int(os.getenv("PORT", 8080)))
