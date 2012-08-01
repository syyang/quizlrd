#!/usr/bin/python

import random
import sys
sys.path.append('./gen-py')

import gflags

from quizlord import QuestionStore
from quizlord.ttypes import *

from thrift import Thrift
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.transport import THttpClient

FLAGS = gflags.FLAGS

gflags.DEFINE_string('host', 'localhost', 'host name', short_name='h')
gflags.DEFINE_integer('port', 8080, 'port number', short_name='p')


def test_client(host, port):
    try:
        transport = THttpClient.THttpClient("http://%s:%d" % (host, port))
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = QuestionStore.Client(protocol)

        transport.open()

        a = random.randint(1, 100)
        b = random.randint(1, 100)
        c = a + b
        question = Question("%s + %s" % (a, b), str(c))

        client.addQuestion(question)

        print client.getQuestions()

        transport.close()
    except Thrift.TException, tx:
        print '%s' % (tx.message)


def main(argv):
    try:
        argv = FLAGS(argv) # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)        
    
    test_client(FLAGS.host, FLAGS.port)

if __name__ == '__main__':
    main(sys.argv)
