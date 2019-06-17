import unittest
import flask 


class TestWeatherman(unittest.TestCase):
    '''
        Test Class Definition: Tests the weatherman package class
    '''
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.app = flask.Flask(__name__)

    # targets weatherman.py
    def testMainStatus(self):
        '''
            Test method definition: tests the main page routing path
        '''
        with self.app.test_request_context('/?name=ScaryMary'):
            assert flask.request.path == '/'
            assert flask.request.args['name'] == 'ScaryMary'

    def testSummaryRoute(self):
        '''
            Test method definition: tests the results table view
        '''
        with self.app.test_client() as c:
            c.get('/?result=summary')
            assert flask.request.args['result'] == 'summary'


    def tearDown(self):
        del self.app

    @classmethod
    def tearDownClass(cls):
        pass
