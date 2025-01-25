import datetime
import logging

from modules import db

lg = logging.getLogger("modules.analytics")


def register_server_event(data: dict) -> bool:
  return db.insert_dict("server_events", data)


def register_client_event(data: dict) -> bool:
  data = prepare_client_data(data)
  data["received_at"] = datetime.datetime.now().isoformat()
  return db.insert_dict("client_events", data)


def prepare_client_data(data: dict) -> dict:
  db_data = {}

  if not data.get("uid"):
    raise ValueError("'uid' is mandatory for client event!")
  db_data["uid"] = data["uid"]

  if not data.get("event"):
    raise ValueError("'event' is mandatory for client event!")
  db_data["event"] = data["event"]

  # Browser data
  if data.get("browser"):
    browser = data["browser"]
    if browser.get("userAgent"):
      db_data["user_agent"] = browser["userAgent"]
    if browser.get("language"):
      db_data["language"] = browser["language"]
    if browser.get("cookiesEnabled") is not None:
      db_data["cookies_enabled"] = browser["cookiesEnabled"]
    if browser.get("doNotTrack"):
      db_data["do_not_track"] = browser["doNotTrack"]
    if browser.get("onLine") is not None:
      db_data["online"] = browser["onLine"]

  # Screen data
  if data.get("screen"):
    screen = data["screen"]
    if screen.get("width"):
      db_data["screen_width"] = screen["width"]
    if screen.get("height"):
      db_data["screen_height"] = screen["height"]
    if screen.get("availWidth"):
      db_data["screen_avail_width"] = screen["availWidth"]
    if screen.get("availHeight"):
      db_data["screen_avail_height"] = screen["availHeight"]
    if screen.get("colorDepth"):
      db_data["screen_color_depth"] = screen["colorDepth"]
    if screen.get("pixelDepth"):
      db_data["screen_pixel_depth"] = screen["pixelDepth"]
    if screen.get("orientation"):
      db_data["screen_orientation"] = screen["orientation"]

  # Window data
  if data.get("window"):
    window = data["window"]
    if window.get("innerWidth"):
      db_data["window_inner_width"] = window["innerWidth"]
    if window.get("innerHeight"):
      db_data["window_inner_height"] = window["innerHeight"]
    if window.get("outerWidth"):
      db_data["window_outer_width"] = window["outerWidth"]
    if window.get("outerHeight"):
      db_data["window_outer_height"] = window["outerHeight"]

  # Hardware data
  if data.get("hardware"):
    hardware = data["hardware"]
    if hardware.get("deviceMemory"):
      db_data["device_memory"] = hardware["deviceMemory"]
    if hardware.get("hardwareConcurrency"):
      db_data["hardware_concurrency"] = hardware["hardwareConcurrency"]
    if hardware.get("maxTouchPoints"):
      db_data["max_touch_points"] = hardware["maxTouchPoints"]

  # Connection data
  if data.get("connection"):
    connection = data["connection"]
    if connection.get("effectiveType"):
      db_data["connection_effective_type"] = connection["effectiveType"]
    if connection.get("downlink"):
      db_data["connection_downlink"] = connection["downlink"]
    if connection.get("rtt"):
      db_data["connection_rtt"] = connection["rtt"]
    if connection.get("saveData") is not None:
      db_data["connection_save_data"] = connection["saveData"]

  # Timezone data
  if data.get("timezone"):
    timezone = data["timezone"]
    if timezone.get("timezone"):
      db_data["timezone"] = timezone["timezone"]
    if timezone.get("timezoneOffset") is not None:
      db_data["timezone_offset"] = timezone["timezoneOffset"]

  # Features data
  if data.get("features"):
    features = data["features"]
    if features.get("localStorage") is not None:
      db_data["feature_local_storage"] = features["localStorage"]
    if features.get("sessionStorage") is not None:
      db_data["feature_session_storage"] = features["sessionStorage"]
    if features.get("webGL") is not None:
      db_data["feature_web_gl"] = features["webGL"]
    if features.get("webWorkers") is not None:
      db_data["feature_web_workers"] = features["webWorkers"]
    if features.get("notifications") is not None:
      db_data["feature_notifications"] = features["notifications"]
    if features.get("geolocation") is not None:
      db_data["feature_geolocation"] = features["geolocation"]

  return db_data


def get_users_page_view_data():
  data = db.select(
    "SELECT uid, COUNT(uid) as event_count, MAX(timestamp) last_event FROM server_events GROUP BY uid")
  return data


def get_total_page_views():
  return db.select("SELECT COUNT(*) as total FROM server_events")[0]["total"]


def get_user_summary(uid: str) -> dict:
  d = db.select("SELECT COUNT(*) as total FROM server_events WHERE uid=?", (uid,))
  lg.info(f"Client events: {d}")
  ret = {
    "uid": uid,
    "client_event_count":
      db.select("SELECT COUNT(*) as total FROM client_events WHERE uid=?", (uid,))[0]["total"],
    "server_event_count":
      db.select("SELECT COUNT(*) as total FROM server_events WHERE uid=?", (uid,))[0]["total"],
    "server_events": []
  }
  latest_client_event = db.select("SELECT * FROM client_events WHERE uid=? ORDER BY received_at DESC LIMIT 1", (uid,))
  lg.info(f"LATEST CLIENT EVENT: {latest_client_event}")
  if latest_client_event:
    ret["client_data"] = latest_client_event[0]
  server_events = db.select("SELECT * FROM server_events WHERE uid=?", (uid,))
  if server_events:
    ret["server_events"] = server_events
  return ret
