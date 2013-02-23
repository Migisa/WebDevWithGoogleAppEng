import os
import webapp2
import jinja2
from google.appengine.ext import db
import re


# put jinja_env here
template_dir = os.path.join(os.path.dirname(__file__),"templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)



def blog_key(name='default'):
	return db.Key.from_path('blogs', name)



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
	last_modified = db.DateTimeProperty(auto_now = True)

	def render(self):
		self.render_text = self.content.replace('\n', '<br>')
		return render_str("showall.html", p = self)



class AllPosts(Handler):
		def get(self):
			#allposts = db.GqlQuery("SELECT * FROM Posts ORDER BY created DESC ") #LIMIT 10
			allposts = Posts.all().order('-created')			
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
			p = Posts(parent = blog_key(), subject = subject, content = content)
			b_key = p.put()
			#print b_key.id()
			self.redirect("/blog/%s" % b_key.id())

		else:
			error = "subject and content, please!"
			self.render_newpost(error=error, subject=subject, content=content)




class Permalink(Handler):
		def get(self, postId):
			#lastpost = db.GqlQuery("SELECT * FROM Posts ORDER BY created DESC LIMIT 1")
			key = db.Key.from_path('Posts', int(postId), parent=blog_key())
			post = db.get(key)			
			
			if not post:
				self.error(404)
				return

			self.render('submitted.html', lastpost=[post])




class About(Handler):
		def get(self):
			self.render('about.html')




app = webapp2.WSGIApplication([(r'/blog', AllPosts),
															 (r'/blog/newpost',NewPost),
															 (r'/blog/(\d+)', Permalink),
															 (r'/blog/about', About)							 
															], debug=True)
