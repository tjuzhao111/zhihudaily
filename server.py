import os
import tornado
import httplib2
import json

import tornado.ioloop
import tornado.web
import StringIO
import PIL
import Image
import hashlib

##uilt
def zhihuMain():
    h = httplib2.Http()  
    resp, content = h.request("http://news-at.zhihu.com/api/3/news/latest", "GET")
    #resp, content = h.request("http://daily.zhihu.com/story/4210189", "GET")
    return resp, content

def zhihuFetch(urlto):
    h = httplib2.Http('.cache')
    resp, content = h.request(urlto, "GET")
    return resp, content

class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        urlto = "http://daily.zhihu.com/story/" + noun1
        h = httplib2.Http()
        resp, content = h.request(urlto, "GET")
        self.write(content)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        page = MainPage()
        #page = json.loads(content)
        #self.write("<form method='post' action='/do'><input type=\"text\" name=\"noun1\"><input type=\"submit\"></form>")
        self.write(page)

def GetImage(url):
    h = httplib2.Http()
    resp, content = h.request(url, "GET")
    md5=hashlib.md5(content).hexdigest()
    filepath = './static/'+md5
    f = open(filepath,'wb')
    f.write(content)
    f.close()
    return filepath


def MainPage():
    page = "<head><title>知乎小报</title></head><body><h1>知乎小报简陋测试版 Zhihu daily Beta ver 0.00000001</h1><hr/>"
    resp, content = zhihuMain()
    # json
    jworker1 = json.loads(content)
    stories = jworker1['stories']
    for item in stories:
        div = "<div>"
        title = item['title']
        images = item['images'][0]
        share_url = item['share_url']
        div = div + "<h3><a href=\""+ share_url+"\">" + title + "</a></h3>"
        localimage = GetImage(images)
        div = div + "<a href=\""+ share_url+"\"><img src=\""+ localimage +"\"></a></div><hr/>"
        page += div
    page += "<hr/><p>Contact with me: tjuzhao111@gmail.com</p></body>"
    return page

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "xsrf_cookies": True,
}

application = tornado.web.Application([
    (r"/", MainHandler ), (r'/do', PoemPageHandler)
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    print 'Server started..'
    tornado.ioloop.IOLoop.instance().start()
