The current implementation of libinput uses a simple averaging filter that takes the previous
four samples and averages them. This provides nice smoothing and predictable behaviour, but
ensures there is a latency of 1.5 samples.

This repository exists as a way to experiment with alternative filtering methods in the hope
of finding one that nicely balances reponse rate, accuracy and smoothness. The secondary
goal is to have the filter provide a single value that can be used to control the smoothing factor.

The code is written in python, and it generates graphs of the filter operating over a "n" shape
with some noise applied. This provides a test case where the straight-line tracking and the behaviour
around corners can be observed.


## Running the Code
To run the code you need:

 - python3
 - matplotlib

Run the script using:
```
python3 main.py
``` 

It will output a bunch of graphs in the `output` folder.

## Developing filters
New filters can be added in filters.py. A filter is a function that, when called with one data point,
returns the smoothed datapoints. In the existing filters, data is stored between runs using closures.
In the future, filters may be expanded to being classes.

After placing a new filter in filters, add it to the test cases in `main.py`
PR's with new filters are welcome.


## Future Plans

The current implementation of Points was cool from a functional programming perspective, but
it makes the math inside the filters hard to understand. In the near future I'll refactor the
Point tuple into a class and overload the operators. This should make filter development more
sane.

The end goal of this code is to derive an algorithm suitable for implementation into libinput.
Once this is achieved, the purpose of this code will be fulfilled and the repository will
likely be unmantained unless another purpose can be determined.
