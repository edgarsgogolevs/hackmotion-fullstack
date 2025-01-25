import logging
import sqlite3

logging.basicConfig(level="INFO")
lg = logging.getLogger()

lg.info("Connectin to DB")
conn = sqlite3.connect("database/analytics.db")

cur = conn.cursor()

lg.info("Creating server_events (if not exists)...")
cur.execute("""
CREATE TABLE IF NOT EXISTS server_events (
  uid CHAR(32) NOT NULL,
  request_path TEXT NOT NULL,
  host TEXT NOT NULL,
  session TEXT NULL,
  user_agent TEXT NULL,
  sec_ch_ua TEXT NULL,
  sec_ch_ua_mobile TEXT NULL,
  sec_ch_ua_platform TEXT NULL,
  accept_language TEXT NULL,
  timestamp INTEGER NOT NULL
)
""")

lg.info("Creating client_events (if not exists)...")
cur.execute("""
CREATE TABLE IF NOT EXISTS server_events (
  uid CHAR(32) NOT NULL,
  event TEXT NOT NULL,
  received_at TEXT NOT NULL,
  
  -- Browser data
  user_agent TEXT,
  language TEXT,
  cookies_enabled BOOLEAN,
  do_not_track TEXT,
  online BOOLEAN,
    
  -- Screen data
  screen_width INTEGER,
  screen_height INTEGER,
  screen_avail_width INTEGER,
  screen_avail_height INTEGER,
  screen_color_depth INTEGER,
  screen_pixel_depth INTEGER,
  screen_orientation TEXT,
    
  -- Window data
  window_inner_width INTEGER,
  window_inner_height INTEGER,
  window_outer_width INTEGER,
  window_outer_height INTEGER,
  
  -- Hardware data
  device_memory INTEGER,
  hardware_concurrency INTEGER,
  max_touch_points INTEGER,
  
  -- Connection data
  connection_effective_type TEXT,
  connection_downlink REAL,
  connection_rtt INTEGER,
  connection_save_data BOOLEAN,
  
  -- Timezone data
  timezone TEXT,
  timezone_offset INTEGER,
  
  -- Features data
  feature_local_storage BOOLEAN,
  feature_session_storage BOOLEAN,
  feature_web_gl BOOLEAN,
  feature_web_workers BOOLEAN,
  feature_notifications BOOLEAN,
  feature_geolocation BOOLEAN
)
""")

lg.info("Closing connection..")
cur.close()
conn.close()
lg.info("Connection closed.")
