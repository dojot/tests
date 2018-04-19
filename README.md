# tests
High level tests on dojot

## Jmeter Test properties
1. SERVER - back end server ( default: localhost)
2. PORT - back end server port (default: 8000)
3. PROTOCOL - protocol (default: http)
4. THREADS - number of parallel threads (default: 1)
5. LOOPS - number of loops in a thread (default: 1)

For performance test:
1. remove the kong api rate limit
2. use the crud-perf.jmx file
3. start the test configuring the THREADS property (default: 2)

