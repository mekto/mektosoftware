from flask import Flask, render_template, abort

from .manager import PostManager


app = Flask(__name__)
app.config.from_object(__name__ + '.config')

posts = PostManager(app)

if app.debug:
    app.before_request(posts.find_posts)
else:
    app.before_first_request(posts.find_posts)

from . import filters


@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/blog/<slug>.html')
def post(slug):
    post = posts.get_by_slug(slug) or abort(404)
    return render_template('post.html', **locals())
