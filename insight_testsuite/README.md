# Testing

### Pre-requisite:

Make sure you have the following installed before testing:

* Python
* Pandas (Python package)
* Datetime (Python package)

Create a new folder `test_n` in `insight_testsuite\tests` folder. Create two more folders as `input` and `output` in the folder `test_n`. Put your version of both the input files (`log.csv` and `inactivity_period.txt`) and output file (`sessionization.txt`) in these folder.

### On Linux:

To test on Linux,

Open the shell and traverse to the path of `insight_testsuite` folder and run the following statement:

	insight_testsuite~$ ./run_tests.sh

On a failed test, the output of `run_tests.sh` should look like:

    [FAIL]: test_n
    [Mon Apr 2 16:28:01 PDT 2018] 0 of 11 tests passed

On success:

    [PASS]: test_n
    [Mon Apr 2 16:25:57 PDT 2018] 11 of 11 tests passed
	
### On Windows:

To test the program on Windows,

Open the command prompt and traverse to the path of `insight_testsuite\tests\test_n` and run the following statement:

	insight_testsuite\tests\test_n> python ../../../src/sessionization.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt

The output file `sessionization.txt` can be checked in output folder.