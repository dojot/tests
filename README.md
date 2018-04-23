# Tests
High level tests on dojot

## Jmeter Test properties
1. SERVER - back end server ( default: localhost)
2. PORT - back end server port (default: 8000)
3. PROTOCOL - protocol (default: http)
4. THREADS - number of parallel threads (default: 1)
5. LOOPS - number of loops in a thread (default: 1)

### Performance test:
1. remove the kong api rate limit
   1. file [kong.config.sh](dojot/docker-compose/blob/master/kong.config.sh): __rate plugin limit to avoid brute-force atacks__
1. start the test configuring the THREADS property (default: 2), for example:
   1. ```bash
         docker run --name jmeter-test -i -v ${PWD}:${PWD} -w ${PWD} dojot/docker-jmeter:latest -n -t crud-perf.jmx -l run-crud.xml -e -o run-crud -Jserver=10.202.1.1
      ```
   1. ```bash
         ./run.sh -n -t crud-perf.jmx -l run-crud.xml -e -o run-crud -Jserver=10.202.1.1
      ```
   1. ```bash
         ./run.sh -n -t crud-perf.jmx -l run-crud.xml -e -o run-crud -JTHREADS=5 -Jserver=10.202.1.1
      ```
1. cleanup before next run:
   1. ```bash sudo rm -rf run-crud* jmeter.log```
1. __Note__: _Jserver_ must be an IP reached by the jmeter container

### Functional test:
1. start the test configuring the LOOPS property (default: 1), for example:
   1. ```bash
         docker run --name jmeter-test -i -v ${PWD}:${PWD} -w ${PWD} dojot/docker-jmeter:latest -n -t crud.jmx -l run-crud.xml -e -o run-crud -Jserver=10.202.1.1
      ```
   1. ```bash
         ./run.sh -n -t crud.jmx -l run-crud.xml -e -o run-crud -Jserver=10.202.1.1
      ```
   1. ```bash
         ./run.sh -n -t crud.jmx -l run-crud.xml -e -o run-crud -Jloops=5 -Jserver=10.202.1.1
      ```
1. cleanup before next run:
   1. ```bash sudo rm -rf run-crud* jmeter.log```
1. __Note__: _Jserver_ must be an IP reached by the jmeter container
