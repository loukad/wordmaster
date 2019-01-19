import sys, os

# Switch to the virtualenv if we're not already there
INTERP = os.path.expanduser("~/python/bin/python")
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

# Change to the app's absolute path
sys.path.append('<path>')
from app.wm import app as application

if __name__ == '__main__':
    application.config['TEMPLATES_AUTO_RELOAD'] = True
    application.run(debug=False)

