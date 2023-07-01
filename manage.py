# manage.py

__author__ = "Christopher Wolfe"
__copyright__ = "Copyright 2018, Christopher Wolfe"
__license__ = "MIT"
__maintainer__ = "Christopher Wolfe"
__email__ = "noone234@gmail.com"
__status__ = "Beta"

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
