from datetime import datetime, date


class Post(object):

    def __init__(self, title, slug, published_on, path):
        self.title = title
        self.slug = slug
        self.published_on = published_on
        self.path = path

class PostManager(list):

    def __init__(self, app):
      self.app = app

    def get_by_slug(self, slug):
        for post in self:
            if post.slug == slug:
                return post
        return None

    def clear(self):
        del self[:]

    def find_posts(self):
        """Finds and reads templates in `/posts` directory and extracts info about them.
        The template filenames shoud be in `YYMMDD-slug.html` format.
        """

        self.clear()

        for path in self.app.jinja_env.list_templates(filter_func=lambda t: t.startswith('posts/') and t.endswith('.html')):
            template = self.app.jinja_env.get_template(path)

            filename = path[6:-5]
            slug = filename[7:]
            date_fragment = filename[0:6]
            published_on = datetime.strptime(date_fragment, '%y%m%d').date()

            self.append(Post(title=template.module.title, slug=slug, published_on=published_on, path=path))

        self.sort(key=lambda post: post.published_on, reverse=True)
