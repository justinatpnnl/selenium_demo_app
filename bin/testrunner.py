#from splunktests import splunkCollection
from website_monitoring import TestSuite, TestGenerator
import os, sys, unittest, json
import splunklib.client as client

if __name__ == "__main__":
 
    sessionKey = ""
    
    for line in sys.stdin:
        sessionKey = line
    
    HOST = "127.0.0.1"
    PORT = 8090

    def getCollection(name):
        service = client.connect(token=sessionKey, host=HOST, port=PORT, owner="nobody", app="selenium_demo_app")
        collection = service.kvstore[name]
        return collection.data.query()

    Get tests from kvstore
    testData = getCollection("selenium_monitoring_list")
    count = 0

    # Empty the output.log file for new test results
    outputfile = os.path.join(os.path.dirname(__file__), '..{0}local{0}output.json'.format(os.path.sep))
    f = open(outputfile, 'w')
    f.close()

    # Build tests from kvstore
    for test in testData:
        if test.get('ENABLED') in ['True', 'true', '1', 1, True]:
            # Convert TESTS to list if stored as a string
            if type(test['TESTS']) is not list:
                test['TESTS'] = json.loads(test['TESTS'])
            count = count + 1
            test_name = 'test_%03d' % count
            test_case = TestGenerator(test)
            setattr(TestSuite, test_name, test_case)

    class TextTestResultWithSuccesses(unittest.TextTestResult):
        def __init__(self, *args, **kwargs):
            super(TextTestResultWithSuccesses, self).__init__(*args, **kwargs)
            self.results = []
        def addSuccess(self, test):
            super(TextTestResultWithSuccesses, self).addSuccess(test)
            f = open(outputfile, 'a')
            f.write(json.dumps(test.test.results, sort_keys=True) + '\n')
            f.close()
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSuite)
    testrunner = unittest.TextTestRunner(verbosity=0, resultclass=TextTestResultWithSuccesses).run(suite)