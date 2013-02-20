import os
import webapp2
import jinja2
from google.appengine.ext import db


# put jinja_env here
template_dir = os.path.join(os.path.dirname(__file__),"templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)



class Handler(webapp2.RequestHandler):
	def write(self, *a, **params):
		self.response.out.write(*a, **params)

	def render_str(self, template, **params_r):
		t = jinja_env.get_template(template)
		return t.render(**params_r)

	def render(self, template, **params):
		self.write(self.render_str(template, **params))




class Posts(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)




class AllPosts(Handler):
		def get(self):
			allposts = db.GqlQuery("SELECT * FROM Posts ORDER BY created DESC LIMIT 10")
			self.render('showall.html', allposts=allposts)




class NewPost(Handler):
	def render_newpost(self, subject="", content="", error=""):
		self.render("postnewpost.html", subject=subject, content=content, error=error)
		
	def get(self):
		self.render_newpost()

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")
		
		if subject and content:
			self.redirect("/blog/newpost/1234")
			record = Posts(subject = subject, content = content)
			record.put()

		else:
			error = "subject and content, please!"
			self.render_newpost(error=error, subject=subject, content=content)




class Submitted(Handler):
		def get(self):
			lastpost = db.GqlQuery("SELECT * FROM Posts ORDER BY created DESC LIMIT 1")
			self.render('submitted.html', lastpost=lastpost)






app = webapp2.WSGIApplication([('/blog', AllPosts),
															 ('/blog/newpost',NewPost),
															 ('/blog/newpost/1234', Submitted)							 
															], debug=True)
