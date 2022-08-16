from distutils.log import debug
from venv import create
from Website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)