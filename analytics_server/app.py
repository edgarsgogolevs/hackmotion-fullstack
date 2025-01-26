from waitress import serve
import flaskapp
import os

serve(flaskapp.app, host='0.0.0.0', port=os.getenv('PORT'))

