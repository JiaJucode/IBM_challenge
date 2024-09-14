from flask import Flask, render_template, request
from ai_session import Session

class WebSite:
    def __init__(self) -> None:
        pass
    
app = Flask(__name__)
site = WebSite()
session = Session()

@app.route('/', methods=['GET', 'POST'])    # main page
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

