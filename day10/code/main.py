import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


def parse_adapter_input(adapters):
    # Separate by lines, convert to integer, prepend the initial adapter (0) and append the final adapter (max + 3)
    adapters = [0] + sorted(int(x) for x in adapters.split("\n") if x)
    adapters.append(max(adapters) + 3)

    return adapters


def get_adapter_differences(adapters):
    # Given all adapters need to be used, this is just a matter of sorting them and computing the differences
    adapters = parse_adapter_input(adapters)
    adapters_delta = [adapters[i + 1] - adapters[i] for i in range(len(adapters) - 1)]

    return adapters_delta


def get_adapter_path_count(adapters):
    # Parse and convert adapters to tuple (because lru_cache decorated functions need hashable arguments)
    adapters = tuple(parse_adapter_input(adapters))
    return get_adapter_path_count_priv(adapters)


@lru_cache()
def get_adapter_path_count_priv(adapters, current=0):
    # Get the next adapter indices
    next_indices = [x for x in range(current + 1, current + 4) if x < len(adapters)]

    # If there are no more indices, we're at base case so return 1
    if not next_indices:
        return 1

    # Otherwise, sum all branches from matching adapters (according to <= 3 criteria)
    return sum(get_adapter_path_count_priv(adapters, i) for i in next_indices if adapters[i] - adapters[current] <= 3)
