#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Post

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")


class GuestHandler(BaseHandler):
    def get(self):
        post = Post.query().fetch()

        params = {"post": post}

        return self.render_template("guest.html", params=params)

    def post(self):
        name = self.request.get("name")
        surname = self.request.get("surname")
        email = self.request.get("email")
        message = self.request.get("message")

        if not name:
            name = "Anonymus"

        new_entry = Post(name=name.replace("<script>", ""), surname=surname.replace("<script>", ""),
                         email=email.replace("<script>", ""),
                         message=message.replace("<script>", ""))  # s tem definiramo v bazi
        new_entry.put()  # s tem vstavimo zapis

        return self.redirect_to("main_page")


class MessagesHandler(BaseHandler):
    def get(self):
        msg = Post.query().fetch()
        params = {"msg": msg}
        return self.render_template("messages.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main_page"),
    webapp2.Route('/guest', GuestHandler, name="guest"),
    webapp2.Route('/messages', MessagesHandler),
], debug=True)
