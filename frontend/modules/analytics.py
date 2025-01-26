import logging
import os
import datetime
from hashlib import md5
import requests
from flask import Request

lg = logging.getLogger("modules.analytics")

UID_COOKIE = "user-id"
UID_COOKIE_MAX_AGE = 3600 * 24

ANALYTICS_SERVER = str(os.getenv("ANALYTICS_SERVER_URL"))
ANALYTICS_CLIENT = str(os.getenv("ANALYTICS_CLIENT_URL"))
lg.info(f"Analytics server set to: {ANALYTICS_SERVER}")
SERVER_EVENT_ENDPOINT = f"{ANALYTICS_SERVER}/register_event/server"
CLIENT_EVENT_ENDPOINT = f"{ANALYTICS_CLIENT}/register_event/client"


def create_user_id(req: Request):
  lg.info(f"Headers: {req.headers}")
  user_data_str = f"{req.remote_addr}__{req.headers.get('User-Agent')}"
  return md5(user_data_str.encode()).hexdigest()


def prepare_analytics_data_from_request(uid: str, req: Request) -> dict:
  return {
    "uid": uid,
    "request_path": req.path,
    "ip": req.remote_addr,
    "host": req.headers.get("host"),
    "session": req.cookies.get("_maybe_session"),
    "user_agent": req.headers.get("User-Agent"),
    "sec_ch_ua": req.headers.get("Sec-Ch-Ua"),
    "sec_ch_ua_mobile": req.headers.get("Sec-Ch-Ua-Mobile"),
    "sec_ch_ua_platform": req.headers.get("Sec-Ch-Ua-Platform"),
    "accept_language": req.headers.get("Accept-Language"),
    "timestamp": datetime.datetime.now().isoformat()
  }


def send_analytics_data(data: dict):
  url = SERVER_EVENT_ENDPOINT
  lg.info(f"Send analytics data: {data} -> {url}")
  resp = requests.post(url, json=data)
  if resp.status_code in (200, 201):
    lg.info("Analytics data sent successfully")
  else:
    lg.error(f"Failed to send analytics data, status: {resp.status_code}, response: {resp.content.decode()}")
