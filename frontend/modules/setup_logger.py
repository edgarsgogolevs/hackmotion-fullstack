import logging
import logging.handlers
import os
import sys
import __main__


def init_log(lg):
  #### setup logging
  lg.handlers.clear()
  LOGLEVEL = os.getenv("LOGLEVEL", "INFO")
  FILE_LOG_SIZE = int(os.getenv("FILE_LOG_SIZE", 1))  # type: ignore
  FILE_LOG_ROTATE = int(os.getenv("FILE_LOG_ROTATE", 3))  # type: ignore
  logging.basicConfig(level=LOGLEVEL, handlers=[])
  formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s]: %(message)s')
  log_file_path = os.path.dirname(os.path.realpath(__main__.__file__)) + "/logs/server.log"
  # output handler
  sh = logging.StreamHandler(sys.stdout)
  sh.setFormatter(formatter)
  sh.setLevel(LOGLEVEL)
  # file output handler
  fh = logging.handlers.RotatingFileHandler(log_file_path,
                                            maxBytes=FILE_LOG_SIZE * 1024 * 1024,
                                            backupCount=FILE_LOG_ROTATE)
  fh.setFormatter(formatter)
  fh.setLevel(LOGLEVEL)
  lg.addHandler(sh)
  lg.addHandler(fh)
