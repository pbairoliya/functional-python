from typing import Callable, List

def filter_list(predicate: Callable[[int], bool], numbers: List[int]) -> List[int]:
    result: list[int] = []
    for num in numbers:
        if predicate(num):
            result.append(num)
    return result
def is_even(num: int) -> bool:

    return num % 2 == 0

def is_odd(num: int) -> bool:

    return num % 2 != 0

def main():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    even_numbers = filter_list(is_even, numbers)
    print("Even numbers:", even_numbers)
    
    odd_numbers = filter_list(is_odd, numbers)
    print("Odd numbers:", odd_numbers)

if __name__ == "__main__":
    main()



def map( xs: list[str])->list[int]:
    result: list[int] = []
    for x in xs:
        y = int (x)
        result.append(y)
    
    return result


def microbenchmark_avg(
    subject: Subject[T], producer: Producer[T], n: int, runs: int
) -> int:
    """Compute the average time cost (ns) of a microbenchmark over # runs."""

    # 1. Define an "internal" helper function for an individual run
    def run_once(n: int) -> int:
        """Given an n, run one microbenchmark of subject/producer."""
        return microbenchmark(subject, producer, n)

    # 2. n_runs is a list where each element is n repeated (length=runs)
    n_runs: list[int] = [n] * runs

    # 3. Use the built-in map function to call run_once on each n
    time_costs: list[int] = list(map(run_once, n_runs))

    #Compute the average time cost of the runs and return it.
    costSum = 0
    for cost in time_costs:
        costSum += cost
    return costSum//runs

## Average of Many Microbenchmark Runs

Since each microbenchmark has some variance in duration, we're implementing `microbenchmark_avg`, which has an additional parameter of the number of repeated runs of the microbenchmark. We then take the average of this number of runs to give us a more consistent estimated "average cost" of each subject function.

from workbench import microbenchmark_avg

print(f"set_in(n=1000) avg cost {microbenchmark_avg(set_in, set_producer, n=1000, runs=1000)} nanoseconds")
print(f"list_in(n=1000) avg cost {microbenchmark_avg(list_in, list_producer, n=1000, runs=1000)} nanoseconds")

def benchmark(
    subject: Subject[T], producer: Producer[T], max_pow_2_n: int, runs: int
) -> dict[int, int]:
    """Compute the avg cost of a microbenchmark over increasing sizes of n.
    Returns a dictionary where the key is `n` size of produced data set and 
    value is the cost of microbenchmarking the `subject` with the given `n`.

    The sizes of `n` double for each successive benchmark, such that the test
    ns are: [2**0, 2**1, 2**2, ..., 2**max_pow_2_n]
    """
    # 1. Define an internal helper function to compute powers of 2
    def pow2(exponent: int) -> int:
        return int(2**exponent)

    # 2. Produce a list of exponents: [0, 1, 2, ..., max_pow_2_n]
    exponents: list[int] = list(range(max_pow_2_n + 1))

    # 3. Produce a list of n sizes, which are successive powers of 2
    # [1, 2, 4, 8, ..., 2 ** max_pow_2_n]
    # TODO: replace the elipses, hint: use the pow2 function and exponents list
    n_sizes: list[int] = list(map(pow2,exponents))

    # 4. Define an internal helper function to microbenchmark given n
    def avg_cost_runner(n: int) -> int:
        return microbenchmark_avg(subject, producer, n, runs)

    # 5. Compute microbenchmark avg time costs for each of our n_sizes
    # TODO replace the elipses, hint: use n_sizes and the function of step 4
    n_costs: list[int] = list(map(avg_cost_runner,n_sizes))

    # 6. Finally, return a dictionary where the keys are n_sizes and
    # the values are n_costs
    return dict(zip(n_sizes, n_costs))

## Benchmarking Doubling n Sizes of Data

Let's investigate how expensive our subject functions are as the sizes of their datasets grow. To do so, we've defined an ultimate `benchmark` function that produces a dictionary where the keys are our data size and values are the time cost in nanoseconds.


from workbench import benchmark

benchmark(set_in, set_producer, max_pow_2_n=14, runs=1000)
benchmark(list_in, list_producer, max_pow_2_n=14, runs=1000)

# The following function plots our results
import matplotlib.pyplot as plt

def plot(title: str, plots: list[tuple[str, dict[int, int]]]):
    fig, ax = plt.subplots()
    for plot_data in plots:
        label: str = plot_data[0]
        results: dict[int, float] = plot_data[1]
        ax.plot(list(results.keys()), list(results.values()), label=label)
    ax.ticklabel_format(style='plain')
    ax.legend()
    fig.suptitle(title)
    ax.set_xlabel("Size of Collection (N)")
    ax.set_ylabel(f"Avg Cost (Nanoseconds)")
    plt.show()

plot("Time Complexity of `in` Operator",
  [
    ("set's `in`", benchmark(set_in, set_producer, max_pow_2_n=14, runs=1000)),
    ("list's `in`", benchmark(list_in, list_producer, max_pow_2_n=14, runs=1000))
  ]
)