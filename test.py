from schemaless import Database
from schemaless import Index, Model, Fql, Cleaner
import json
import os
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
      class ComplexInnerModel(Model):
        fields = {'new' : 'new', 'email' : {'token' : 'test'}}
        table = 'complex_inner_model'
        indexes = [Index(["email.token"], "simple_token_index", "simple_id"), Index(["new"], "simple_new_index", "simple_id")]


      model = ComplexInnerModel()
      model.set(new='this_new_is_old')
      model.put()
      sql = "SELECT body FROM  %(table)s  WHERE id = %(id)s" % {'table' : model.table, 'id' : '%s' }
      result = Database.get().get(sql, model._id)
      print json.loads(result['body'])['new']
      print json.loads(result['body'])['email']['token']

      # model = ComplexInnerModel()
      # model.put()
      # sql = "SELECT updated FROM %(table)s WHERE id = %(arg)s" % {'table' : model.table, 'arg' : "%s"}
      # result = Database.get().get(sql, model.get('id'))
      # print model.get('updated'), result['updated']

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()