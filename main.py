import os
import math
from collections import namedtuple

import matplotlib.pyplot as plt
from point import *
import filters
import point_array
import noise


TestFilter = namedtuple("TestCase", ["filter_name", "filter"])
TestShape = namedtuple("TestShape", ["shape_name", "clean_shape", "noisy_shape"])
TestResult = namedtuple("TestResult", ["shape", "filter", "filtered_array", "average_error"])


def generate_box():
    """ Generates a predetermined zigzag line that can be used to test
    the response to sharp corners"""
    points = []
    points.extend(point_array.generate_line_segment(Point(0, 0), Point(0, 5), 20))
    points.extend(point_array.generate_line_segment(Point(0, 5), Point(5, 5), 20))
    points.extend(point_array.generate_line_segment(Point(5, 5), Point(5, 0), 20))
    return points


def generate_step():
    """ Generates a single step to make it easy to check overshoot """
    points = []
    points.extend(point_array.generate_line_segment(Point(0, 0), Point(5, 0), 20))
    points.extend(point_array.generate_line_segment(Point(5, 5), Point(10, 5), 20))
    return points


def generate_sine():
    """ Generates a predetermined zigzag line that can be used to test
    corner-cutting on a more natural shape """
    points = []
    for x in range(100):
        points.append(Point(x/20, math.sin(x/20)*2.5 + 2.5))
    return points


def get_test_filters():
    """ Returns some filters. These filters are run for each shape
    returned by "get_test_shapes()". This function is called for
    each run to prevent contamination """
    test_filters = [
        TestFilter("No Filter", filters.null_filter()),
        TestFilter("Reference (Mean Filter 4 Samples)", filters.mean_filter(4)),
        TestFilter("Exp Filter 0.6", filters.exp_filter(0.6)),
        TestFilter("Predictive Filter (predict=0.6, smooth=0.6)",filters.simple_predictive_filter(0.6, 0.6))
    ]

    # It can be useful to iterate for a particular filter, eg:
    # for filter_constant in [0.3, 0.6, 0.9]:
    #    test_filters.append(TestFilter(
    #        "Exp Filter {}".format(filter_constant, filters.exp_filter(filter_constant)),
    #    ))

    return test_filters


def get_test_shapes():
    """ Run each filter on these different steps. This makes it possible
    to check filter response on different sets of input data """
    box = generate_box()
    step = generate_step()
    sine = generate_sine()

    test_shapes = [
        TestShape("Box Clean", box, box),
        TestShape("Step Clean", step, step),
        TestShape("Sine Clean", sine, sine),
    ]
    for seed in range(3):
        distortion_box = noise.generate_noise_array(noise.white_noise(seed, 0.2), len(box))
        noisy_box = point_array.sum_point_arrays(distortion_box, box)
        test_shapes.append(TestShape(
            "Box seed={} Noise=0.2".format(seed),
            box,
            noisy_box
        ))
    for seed in range(3):
        distortion_sine = noise.generate_noise_array(noise.white_noise(seed, 0.2), len(sine))
        noisy_sine = point_array.sum_point_arrays(distortion_sine, sine)
        test_shapes.append(TestShape(
            "Sine seed={} Noise=0.2".format(seed),
            sine,
            noisy_sine
        ))
    return test_shapes


def run_filters(test_shapes):
    """ Generates and runs each filter on each of the provided shapes """
    print("Starting Filtering")
    results = []
    count = 0
    for shape in test_shapes:
        for filt in get_test_filters(): # Recreate the filters for each shape
            count += 1
            print("Filtering {}".format(count), end='\r')
            filtered_shape = filters.filter_array(filt.filter, shape.noisy_shape)
            results.append(TestResult(
                shape,
                filt,
                filtered_shape,
                math.sqrt(point_array.squared_difference(filtered_shape, shape.clean_shape))
            ))
    print("Filtering Complete")
    return results


def plot_shapes(test_results):
    """ Plots the test results grouping all the shapes onto the same
    output image """
    print("Plotting Shapes")
    runs_by_shape = {}
    for result in test_results:
        shape_name = result.shape.shape_name
        shape_array = runs_by_shape.get(shape_name, [])
        shape_array.append(result)
        runs_by_shape[shape_name] = shape_array

    plot_runs("output/shapes", runs_by_shape)
    print("Plotting Shapes Complete")



def plot_filters(test_results):
    """ Plots the test results grouping all the filters onto the same
    output image """
    print("Plotting Filters")
    runs_by_filter = {}
    for result in test_results:
        filter_name = result.filter.filter_name
        filter_array = runs_by_filter.get(filter_name, [])
        filter_array.append(result)
        runs_by_filter[filter_name] = filter_array

    plot_runs("output/filters", runs_by_filter)
    print("Plotting Filters Complete")


def plot_runs(directory, runs):
    total_num = len(runs)
    count = 0
    for run_name in runs:
        count += 1
        print("Plotting {}/{}".format(count, total_num), end='\r')
        results = runs[run_name]

        plot_width = math.ceil(math.sqrt(len(results)))
        fig, axes = plt.subplots(plot_width, plot_width)
        fig.set_size_inches(plot_width * 5, plot_width * 5)

        for test_id, test_result in enumerate(results):
            axis = axes[math.floor(test_id/plot_width)][test_id%plot_width]
            plot_run(axis, test_result)


        if not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig("{}/{}.png".format(directory, run_name))


def plot_run(axis, test_result):
    """ Plots the supplied test onto the provided set of graph axis """
    filtered_shape_x, filtered_shape_y = point_array.point_array_to_axis_arrays(test_result.filtered_array)
    shape_x, shape_y = point_array.point_array_to_axis_arrays(test_result.shape.clean_shape)
    noisy_shape_x, noisy_shape_y = point_array.point_array_to_axis_arrays(test_result.shape.noisy_shape)

    axis.plot(shape_x, shape_y, 'g')
    axis.set_autoscale_on(False)
    axis.plot(noisy_shape_x, noisy_shape_y, 'rx')
    axis.plot(filtered_shape_x, filtered_shape_y, 'b')
    axis.plot(filtered_shape_x[-1], filtered_shape_y[-1], 'bo', fillstyle='none')
    axis.text(1, 2, '(Average Delta = {:.02f})'.format(test_result.average_error))

    axis.set_title("{}\n{}".format(
        test_result.shape.shape_name,
        test_result.filter.filter_name
    ))


def main():
    test_shapes = get_test_shapes()
    test_results = run_filters(test_shapes)

    plot_shapes(test_results)
    plot_filters(test_results)


if __name__ == "__main__":
    main()
