from flask import Flask

application = Flask(__name__)


@application.route(f"/{__file__.split('/')[-1]}")
def demo_flask() -> str:
    return "Hello Flask!"
