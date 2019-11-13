# Selenium Demo App

This Splunk app provides a demonstration of what is possible using the [selenium_web_transactions_generator](https://github.com/justinatpnnl/splunk_web_transactions_generator).  



## Installation

Download the latest release and install using the **Install app from file** feature of Splunk's **Manage Apps** page.

https://github.com/justinatpnnl/selenium_demo_app/releases



## Capabilities

This app is meant to be a template for creating your own website performance monitoring service in Splunk. The main capabilities are:

### User interface for configuring Selenium tests

A simple-to-use UI in the **Monitoring Configuration** dashboard allows you to:

1. Create complex Selenium tests
2. Choose the browser you want the test to run in (Chrome or Firefox)
3. Verify the tests function as expected from within the dashboard
4. Set up email recipients for alerting
5. Save your tests to a KVStore in Splunk

### Website Performance Details Dashboard

 This dashboard allows you to see the details for the sites that you have added to monitoring in a timeline visualization.  If there are failures, you can view screenshots, network waterfalls, and details of the tests that failed.

### Scripted Input

The scripted input pulls all of your tests at a specified interval (defaults to 15 minutes) and runs them in real browser, sending the results to Splunk.



## Splunk Visualizations

There are three non-standard visualizations used in these dashboards, which will need to be installed for it to work correctly.  Two are available from the Splunk app store, and one was custom developed and I have made it available on GitHub.

**Timeline - Custom Visualization**

Used to display the network waterfall information on a timeline when using Chrome to run your Selenium tests.

https://splunkbase.splunk.com/app/3120/



**Event Timeline Viz**

Excellent timeline visualization that allows for highlighting Passed vs Failed tests over time.

https://splunkbase.splunk.com/app/4370/



**ImageViewer**

Custom visualization that displays Base64 encoded screenshots captured from failed Selenium tests

https://github.com/justinatpnnl/imageviewer_for_splunk/releases



## Python Modules

**Selenium Web Transactions Generator** - https://github.com/justinatpnnl/splunk_web_transactions_generator

The primary module used to run these dashboards, custom Selenium splunk command, and scripted inputs.  In the Selenium Demo App it is located under `./bin/website_monitoring` and is used by `selenium_command.py` and `testrunner.py`.  It depends on the python modules below.

### Dependencies

**Selenium** - https://pypi.org/project/selenium/

**Splunk SDK for Python** - https://github.com/splunk/splunk-sdk-python/releases

**UA Parser** - https://github.com/ua-parser/uap-python/releases

**User Agents** - https://pypi.org/project/user-agents/



## Special Thanks

Special thanks to Elias Haddad, whose Splunk app inspired this work.

https://splunkbase.splunk.com/app/1880/



## Notice

This material was prepared as an account of work sponsored by an agency of the United States Government. Neither the United States Government nor the United States Department of Energy, nor the Contractor, nor any or their employees, nor any jurisdiction or organization that has cooperated in the development of these materials, *makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness or any information, apparatus, product, software, or process disclosed, or represents that its use would not infringe privately owned rights*.

Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof, or Battelle Memorial Institute. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.

**PACIFIC NORTHWEST NATIONAL LABORATORY**
*operated by*
**BATTELLE**
*for the*
**UNITED STATES DEPARTMENT OF ENERGY**
*under Contract DE-AC05-76RL01830*