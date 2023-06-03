from flask import Flask
import urllib, urllib.request

app = Flask(__name__)

@app.route('/')
def index():
    qlora_id = 
    url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'
    data = urllib.request.urlopen(url)
    xml = data.read().decode('utf-8')
    print(data.read().decode('utf-8'))
    return xml

@app.route('/papers/<string:title>', methods=['GET'])
def process_papers(title):
    return f'Paper: {title}'


if __name__ == '__main__':
    app.run()


# flask --app app run --debug
