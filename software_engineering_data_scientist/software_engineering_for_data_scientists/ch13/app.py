from flask import Flask

app = Flask(__name__)

@app.route('/')
def main_page():
    html = """
      <h1>Dashboard main page</h1>
      <li><a href="/core-metrics">View core metrics</a></li>
      <li><a href="/data-view">View underlying data</a></li>
      <li><a href="/ml-app">ML app</a></li>
    """

    return html


@app.route('/core-metrics')
def core_metrics():
    return "<h1>Core metrics</h1>"


@app.route('/data-view')
def data_view():
    return "<h1>Data view</h1>"


if __name__ == '__main__':
    app.run()