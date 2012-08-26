from datetime import datetime, date

from flask import Flask, render_template, abort

app = Flask(__name__)
app.config.from_object(__name__ + '.config')


class Post(object):

    def __init__(self, title, slug, published_on, path):
        self.title = title
        self.slug = slug
        self.published_on = published_on
        self.path = path


class PostManager(list):

    def get_by_slug(self, slug):
        for post in self:
            if post.slug == slug:
                return post

        return None

    def clear(self):
        del self[:]


posts = PostManager()


def find_posts():
    posts.clear()

    for path in app.jinja_env.list_templates(filter_func=lambda t: t.startswith('posts/') and t.endswith('.html')):
        template = app.jinja_env.get_template(path)
        published_on = datetime.strptime(getattr(template.module, 'published_on', str(date.today())), '%Y-%m-%d').date()
        posts.append(Post(title=template.module.title, slug=path[6:-5], published_on=published_on, path=path))

    posts.sort(key=lambda post: post.published_on, reverse=True)


if app.debug:
    app.before_request(find_posts)
else:
    app.before_first_request(find_posts)


@app.route('/')
def index():
    return render_template('index.html', posts=posts)


@app.route('/blog/<slug>')
def post(slug):
    post = posts.get_by_slug(slug) or abort(404)
    return render_template('post.html', **locals())


from . import filters