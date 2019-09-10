import os
import math
from collections import namedtuple
import matplotlib.pyplot as plt
from point import Point
import filters
import point_array
import noise


TestCase = namedtuple("TestCase", ["name", "filter"])
TestResult = namedtuple("TestResult", ["name", "filtered_array"])


def plot_filters(noisy_shape, results, shape, run_name):
    """ Pots a filtering run """
    plot_width = math.ceil(math.sqrt(len(results)))
    fig, axes = plt.subplots(plot_width, plot_width)
    fig.set_size_inches(20, 20)
    
    shape_x, shape_y = point_array.point_array_to_axis_arrays(shape)
    noisy_shape_x, noisy_shape_y = point_array.point_array_to_axis_arrays(noisy_shape)
    
    for test_id, test_result in enumerate(results):
        axis = axes[math.floor(test_id/plot_width)][test_id%plot_width]
        comparison = point_array.squared_difference(test_result.filtered_array, shape)

        filtered_shape_x, filtered_shape_y = point_array.point_array_to_axis_arrays(test_result.filtered_array)

        axis.plot(shape_x, shape_y, 'g')
        axis.set_autoscale_on(False)
        axis.plot(noisy_shape_x, noisy_shape_y, 'rx')
        axis.plot(filtered_shape_x, filtered_shape_y, 'b')
        axis.plot(filtered_shape_x[-1], filtered_shape_y[-1], 'bo', fillstyle='none')
        axis.text(1, 2, '(Average Delta = {:.02f})'.format(comparison))

        axis.set_title(test_result.name)

    directory = "output/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.savefig("{}/{}.png".format(directory, run_name))


def generate_box():
    """ Generates a predetermined zigzag line that can be used to test """
    points = []
    points.extend(point_array.generate_line_segment(Point(0, 0), Point(0, 5), 20))
    points.extend(point_array.generate_line_segment(Point(0, 5), Point(5, 5), 20))
    points.extend(point_array.generate_line_segment(Point(5, 5), Point(5, 0), 20))
    return points
    
    
def generate_step():
    """ Generates a predetermined zigzag line that can be used to test """
    points = []
    points.extend(point_array.generate_line_segment(Point(0, 0), Point(5, 0), 20))
    points.extend(point_array.generate_line_segment(Point(5, 5), Point(10, 5), 20))
    return points

def generate_sine():
    """ Generates a predetermined zigzag line that can be used to test """
    points = []
    for x in range(100):
        points.append(Point(x/20, math.sin(x/20)*2.5 + 2.5))
    return points


def run_filters(shape, noisy_shape, run_name):
    test_cases = [
        TestCase("No Filter", filters.null_filter()),
        TestCase("Reference (Mean Filter 4 Samples)", filters.mean_filter(4)),
        TestCase("Exp Filter 0.6", filters.exp_filter(0.6))
    ]

    
    # ~ for prediction in [0.2, 0.6, 0.8]:
        # ~ for smoothing in [0.1, 0.2, 0.6, 0.8]:
            # ~ test_cases.append(TestCase(
                # ~ "Predictive Filter (predict={}, smooth={})".format(prediction, smoothing),
                # ~ filters.simple_predictive_filter(prediction, smoothing)
            # ~ ))
            
            
    for smoothing in [0.0, 0.2, 0.5, 0.8, 0.95]:
        test_cases.append(TestCase(
            "Predictive Filter 2 (smoothing={})".format(smoothing),
            filters.simple_predictive_filter_2(smoothing)
        ))

    
    print("Beginning Filter Run:", run_name)
    test_results = []
    for case in test_cases:
        test_results.append(TestResult(
            case.name,
            filters.filter_array(case.filter, noisy_shape)
        ))

    print("Plotting Filter Run:", run_name)
    plot_filters(
        noisy_shape,
        test_results,
        shape,
        run_name,
    )


def main():
    """ Runs the filtering methods and generates some graphs """
    box = generate_box()
    step = generate_step()
    sine = generate_sine()

    for seed in range(5):
        distortion_box = noise.generate_noise_array(noise.white_noise(seed, 0.2), len(box))
        noisy_box = point_array.sum_point_arrays(distortion_box, box)
        run_filters(box, noisy_box, "Box seed={} Noise=0.2".format(seed))
        
        distortion_sine = noise.generate_noise_array(noise.white_noise(seed, 0.2), len(sine))
        noisy_sine = point_array.sum_point_arrays(distortion_sine, sine)
        run_filters(sine, noisy_sine, "Sine seed={} Noise=0.2".format(seed))

    run_filters(box, box, "BoxClean")
    run_filters(step, step, "StepClean")
    run_filters(sine, sine, "SineClean")


if __name__ == "__main__":
    main()
