import tornado.web
import tornado.wsgi

class BaseHandler(tornado.web.RequestHandler):
 
    def initialize(self, db):
        self.db = config.database['path']
        
class IndexHandler(BaseHandler):
 
    def get(self):
        #get random news from database
        blog = self.db.blogs.find_one({"_id":int(blogid)})
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(blog))

    def post(self):
        _id = () + 1
        timestamp = datetime.now()
        body = urlparse.parse_qs(self.request.body)
        for key in body:
                body[key] = body[key][0]
        blog = {
                "_id": _id,
                "title": body['title'],
                "tags": body['tags'],
                "category": body['category'],
                "timestamp": timestamp
        }
        self.db.blogs.insert(blog)
        location = "/blog/"+ str(_id)
        self.set_header('Content-Type', 'application/json')
        self.set_header('Location', location)
        self.set_status(201)
        self.write(dumps(blog))
 
    def put(self, blogid):
        ## Convert unicode to int
        _id = int(blogid)
        timestamp = datetime.now()
        body = urlparse.parse_qs(self.request.body)
        for key in body:
                body[key] = body[key][0]
        blog = {
                "title": body['title'],
                "tags": body['tags'],
                "category": body['category'],
                "timestamp": timestamp
        }
        self.db.blogs.update({"_id":_id}, {"$set":blog})
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(blog))
 
    def delete(self,blogid):
        ## Convert unicode to int
        _id = int(blogid)
        blog = {
                "title": None,
                "tags": [],
                "category": [],
                "timestamp": None,
        }
        self.db.blogs.update({"_id":_id}, {"$set":blog})
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(blog))



application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/transaksi/([0-9]+)", Blog, dict(connection = Connection()) ),
    (r"/transaksi/", Blog, dict(connection =  Connection()) ),
    (r"/blogs/", Blogs, dict(connection =  Connection()) ),
], debug=True)

