from website_monitoring import TestSuite, TestGenerator
import os, sys, unittest, json, argparse
import splunklib.client as client

parser = argparse.ArgumentParser(description='Build a Selenium test suite from a saved list of test cases')
parser.add_argument('--offset', type=int, default=0, help="Start position. Default is 0.")
parser.add_argument('--groups', type=int, default=1, help="Number of groups to break the list into. Default is 1.")
args = parser.parse_args()

if __name__ == "__main__":
 
    sessionKey = ""
    
    for line in sys.stdin:
        sessionKey = line
    
    HOST = "127.0.0.1"
    PORT = 8089

    def getCollection(name):
        service = client.connect(token=sessionKey, host=HOST, port=PORT, owner="nobody", app="selenium_demo_app")
        collection = service.kvstore[name]
        return collection.data.query()

    # Get tests from kvstore
    testData = getCollection("selenium_monitoring_list")
    count = 0

    # Empty the output.log file for new test results
    outputfile = os.path.join(os.path.dirname(__file__), '..{0}local{0}output.json'.format(os.path.sep))
    f = open(outputfile, 'w')
    f.close()

    for test in testData[args.offset::args.groups]:
        if str(test.get('ENABLED', False)).lower() in ['true', '1']:
            # Convert TESTS to list if stored as a string
            if not isinstance(test['TESTS'], list):
                test['TESTS'] = json.loads(test['TESTS'])
            count = count + 1

            # DEV OPTIONS
            # OVERRIDE BROWSER
            # test['BROWSER'] = "Chrome"
            
            # DEBUG
            # test['DEBUG'] = True

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