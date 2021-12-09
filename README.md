**Running a single test from a test file**

`docker-compose exec backend pytest api/tests/name_of_test_file.py::name_of_test -vv`

**Run all tests in a single test file**

`docker-compose exec backend pytest api/tests/name_of_test_file.py -vv`

**Run all test files in a single directory**
`docker-compose exec backend pytest api/tests/ -vv`