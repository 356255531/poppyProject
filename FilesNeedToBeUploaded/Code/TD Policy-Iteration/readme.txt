In some cases, there was a double implementation of
epsilon greedy. Hence, sometimes there is epsilon set to
0 in the function call. This means, that the epsilon greedy
is suppressed only in one of the classes to avoid double
non-deterministic behaviour.