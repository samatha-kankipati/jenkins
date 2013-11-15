Test Case Classification
########################

Introduction
************
The following are presented as general guidelines for test case package and/or tagging structure. These Test Cases Types are intended to 
represent specific testing focus of that test case package and will aid in reporting for both execution and overall test case coverage for 
any given project.

Gate
~~~~~
Gating tests are aimed specifically at providing a base validation of component level new code *before* check-in. They are meant to be executed by a 
developer wanting to ensure that their current check-out does not break the existing code base. These types of tests serve as a bridge between Developer 
based Unit Tests and Smoke tests, which are the most basic acceptance tests.

Smoke
~~~~~
Smoke tests are generally aimed at a minimal, happy path functionality in the overall application under test. The main objective here should be to provide 
a quick bell weather as to whether or not a given build is valid for further testing.

Functional
~~~~~~~~~~
Functional tests are generally aimed at a specific Feature, API Call, singular component (like stored procedures in a database) or specific stand-alone 
product within OpenStack. Functional Tests should be designed to validate a granular component of a specific feature area works as expected when 
called/used as described. For example a test package concerned with the List Server(s) functionality of Nova would be a type of Functional Test.

Integration
~~~~~~~~~~~
Functional style tests that are aimed specifically at interoperability between components. An example of this kind of test would be that the Nova Client 
tool from Compute can be used to properly make calls into the Cinder API.

Negative
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A Functional or Integration Test could be designed to provide invalid values, call a sequence in the wrong order, etc... This can be referred to as a 
Negative Test. A normal test of this type is focused on correct usage whereas a Negative version is purposefully attempting to use the feature in a way 
it was not designed.

End-To-End
~~~~~~
End-To-End tests are aimed at OpenStack as a whole system. The main objective here is to simulate real world, end-to-end usage of the total OpenStack 
product. An example End-To-End test could be backing up Nova Images to Swift using Glance.

Failover or Recovery
~~~~~~~~~~~~~~~~~~~~
Failover and Recovery tests are aimed at testing the resiliency feature of the overall system. These tests are to End-To-End Tests what Negative Tests are 
to Functional or Integration Tests. These tests are more in-depth than a simple Negative Test and are therefore categorized seperately. These are tests that 
are specifically designed to introduce massive failure at key points in the AUT and validate that the AUT recovers properly. Simulating device or server 
failures, powering down one or more devices or servers in the middle of an update and sending corrupt packet traffic along with clean packets over the network 
are all examples of Failover and Recovery based testing.

Performance Benchmark
~~~~~~~~~~~
Performance based tests, unlike Functional tests, are designed to generate a low but steady volume in the system. They are often aimed at a specific 
transaction or very specific measurement. This is used to validate a known performance benchmark or generate a performance benchmark for a new feature. 
For example, how long it takes on average to create a server, delete an object, run a backup, etc...

Burn-In
~~~~~~~
Many key problems in the software can only be detected after the system has been up and running under various levels of use for an extended period of time. 
Most testing activities involve frequent (if not continuous) setup and tear down of experiments. This can often mask the type of issue that only shows up in 
a system that has been running for days or weeks continuously. Burn-In testing is aimed directly at running basic Smoke or Functional tests in a loop 
against fixed versions of the system for extended periods of time. The goal here is to validate that the system behaves properly when applications or 
processes are running for an extended period of time, detect any memory leaks in longer running processes and watch out for performance degradation.
