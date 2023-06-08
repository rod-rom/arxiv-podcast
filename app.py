from flask import Flask, request, url_for, render_template, make_response
from markupsafe import escape
import urllib, urllib.request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.

    url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'
    data = urllib.request.urlopen(url)
    xml = data.read().decode('utf-8')
    print(data.read().decode('utf-8'))
    return xml

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'do_the_login()'
    else:
        return 'show_the_login_form()'

@app.route('/user/<username>')
def profile(username):
    return f'{escape(username)}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

# url_for('static', filename='style.css')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    resp = make_response(render_template('upload.html'))
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')
    return resp

#If you want the file that was named on the client before it was uploaded:
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files['the_file']
#         file.save(f"/var/www/uploads/{secure_filename(file.filename)}")
def fetch_arxiv_paper(paper_id):
    url = f'http://export.arxiv.org/api/query?id_list={paper_id}'
    data = urllib.request.urlopen(url)
    xml = data.read().decode('utf-8')
    print(data.read().decode('utf-8'))
    return xml

@app.route('/paper/<int:paper_id>')
def get_paper(paper_id):
    paper = fetch_arxiv_paper(paper_id)
    if paper:
        return render_template('paper.html', paper=paper)
    else:
        return 'Paper not found'


if __name__ == '__main__':
    app.run()


# flask --app app run --debug
