# HackMotion full-stack test task

> [!IMPORTANT]  
> In creation of this text file NO LLM WAS USED. So it might be worth reading. :)

## Table of Contents
1. [How to run](#how-to-run)
2. [Run in development mode](#run-in-development-mode)
3. [Some details](#some-details)
4. [Tech used](#tech-used)

## How to run
Make sure [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/install/) are installed.

In the project root run:
```bash
docker-compose up --build
```

> [!WARNING]  
> Environment should be configured so that `ANALYTICS_SERVER_URL` is url accesible from frontend container and `ANALYTICS_CLIENT_URL` should be accessible from the browser.
> In default configuration: `ANALYTICS_SERVER_URL=http://analytics:42069` and `ANALYTICS_CLIENT_URL=http://localhost:42069`

By default services are ran on:
- Frontend [http://localhost:42042](http://localhost:42042)
- Analytics [http://localhost:42069](http://localhost:42069)

Visiting [http://localhost:42069](http://localhost:42069) from the browser will display basic info about users visited the site.
Clicking on user ID will display detailed info that was gathered about this specific user. Those pages are just for demonstration, data gathered and the way it is displayed can be changed according to business needs.

## Run in developement mode
1. Edit `.env` files in corresponding folders according to your needs
2. Make sure `Python 3.12` is installed
3. Create a virtual env (`python -m venv env`)
4. Install dependencies `pip install -r requirements.txt`
5. Run `start.sh` script (default location for venv is `./env/`)

## Some details

On request to frontend server it checks if `user-id` cookie is present, if not adds it based on `User-Agent` and IP.
And then sends following data to analytics server:
- uid
- request_path
- host
- ip
- session
- user_agent
- sec_ch_ua
- sec_ch_ua_mobile
- sec_ch_ua_platform
- accept_language
- timestamp

On frontend button click video starts playing and following data is sent to analytics server:
- uid (User ID)
- event (Event name)
- received_at
- user_agent
- language
- cookies_enabled
- do_not_track
- online
- screen_width
- screen_height
- screen_avail_width
- screen_avail_height
- screen_color_depth
- screen_pixel_depth
- screen_orientation
- window_inner_width
- window_inner_height
- window_outer_width
- window_outer_height
- device_memory
- hardware_concurrency
- max_touch_points
- connection_effective_type
- connection_downlink
- connection_rtt
- connection_save_data
- timezone
- timezone_offset
- feature_local_storage
- feature_session_storage
- feature_web_gl
- feature_web_workers
- feature_notifications
- feature_geolocation

## Tech used

For both web and analytics server [Python Flask](https://flask.palletsprojects.com/en/stable/) is used.
For data storage [sqlite3](https://www.sqlite.org/index.html) is used due to its simplicity, for prod different options should be considered.
Database is stored in Docker Volume, so data does not disappear when container is stopped.
Docker volumes also used for log files of both services.
For the client plain HTML/CSS/JS is used, again for the simplicity, imo no need to pull 700MB of React for task this small.
