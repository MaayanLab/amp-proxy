# This is only for development.
#
# In production, Flask is run by mod_wsgi, which imports the via wsgi.py.


from app.app import app
app.debug = False
app.run(port=52496, host='0.0.0.0')