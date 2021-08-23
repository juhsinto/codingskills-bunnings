# Coding Skills Challenge - Solution

I have attempted [this](https://github.com/tosumitagrawal/codingskills) code challenge using Python

### Pre-requisites:
In order to run the solution, the user must have python 3 installed on their machine, and the library pandas installed as well.

In order to install `pandas` you can use pip like `pip3 install pandas` 

### Run the project:
Assuming the input files 'barcodesA.csv', 'barcodesB.csv', 'catalogA.csv', 'catalogB.csv' are in the 'input' directory, and there exists a directory 'output'

Run the project via `python merge_catalogues.py`

## Expected output vs sample output

On successful execution, an output file called 'output.csv' will be generated in the 'output' directory

I found that the order of the 'products' seems to differ just slightly, I'm hoping that this isn't a problem.

## Tests
In order to run the tests, I used unittest
This can be tested via `python -m unittest test_merge_catalogues.TestMergeCatalogues`

## Additional Information

I first started off by writing pseudocode, based off my understanding of the problem - this took a bit of time because I wanted to go through the example data, and sample output.

I then used Jupyter Notebooks to prototype on the problem iteratively.

Then, for debugging - I used PyCharm.
