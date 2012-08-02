""" Handles question store service. """

import webapp2
import logging

from google.appengine.ext import db

import sys
sys.path.append('./gen-py')

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.transport import TIOStreamTransport

from quizlord import QuestionStore
from quizlord.ttypes import *


class GAEQuestion(db.Model):
    """Model for persisting question objects."""

    question = db.StringProperty()
    answer = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def new_key(user_id=None):
        return db.Key.from_path('Question', user_id or 'default')


class QuestionStoreHandler(QuestionStore.Iface):
    """Handles question service requests."""

    def getQuestions(self):
        rows = db.GqlQuery(
            "SELECT * FROM GAEQuestion ORDER BY date LIMIT 100")
        questions =  [Question(row.question, row.answer) for row in rows]
        logging.info(questions)
        return questions

    def addQuestion(self, question):
        logging.info("addQuestion: " + str(question))
        row = GAEQuestion(parent=GAEQuestion.new_key())
        row.question = question.question
        row.answer = question.answer
        row.put()
       

class MainHandler(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/x-thrift'
        
        handler = QuestionStoreHandler()
        processor = QuestionStore.Processor(handler)
        
        input_stream = self.request.environ['wsgi.input']
        output_stream = self.response.out

        transport = TIOStreamTransport.TIOStreamTransport(input_stream,
                                                          output_stream)

        protocol = TBinaryProtocol.TBinaryProtocol(transport, True, True)
        transport.open()
        processor.process(protocol, protocol)
        transport.close()


app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
