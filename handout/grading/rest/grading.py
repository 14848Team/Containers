import sys, requests, unittest
from ConfigTests import ConfigTests
from LaunchTests import LaunchTests
from ContainerTests import ContainerTests
from CGITests import CGITests

def run_full(hostname, port):
    total = 0
    results = []

    ConfigTests.HOSTNAME = hostname
    ConfigTests.PORT = port
    LaunchTests.HOSTNAME = hostname
    LaunchTests.PORT = port
    ContainerTests.HOSTNAME = hostname
    ContainerTests.PORT = port
    CGITests.HOSTNAME = hostname
    CGITests.PORT = port
    runner = unittest.TextTestRunner()

    # to not run tests, comment them out here
    # you probably want to do this in-order
    results.append(runner.run(ConfigTests.suite()))
    results.append(runner.run(LaunchTests.suite()))
    results.append(runner.run(ContainerTests.suite()))
    results.append(runner.run(CGITests.suite()))

    for result in results:
        print(result)

    return total

if __name__ == "__main__":
    hostname = "localhost"
    port = "8080"
    run_full(hostname, port)

