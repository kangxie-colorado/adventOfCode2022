"""
This feel like a back track problem but it is too difficult to do that
so I observe the input, the sample has 6 valves with values
the final input has 14
why don't I just permutation all the possibilities
the total is not much

hmm.
# >>> fac(14)
87178291200
okay... not that much? 87 billion?
but it could terminate early if the time is used up

# >>> fac(15)
1307674368000
okay it is actually 1Trillion... there is no way to solve it brute force

but notice in 30 minutes, for 15 valves it will be only opened if these valves
are chained together one by one
so it is not gonna to open all of them... 
so maybe I search for a path that can be finished in 30 minutes and calculate its value
then so on and so forth..
when to stop??

I could use some pre-sort, dist to A * (time left)
I could calculate the dist between A and every non-zero valves, sort
I could calculate the dist between every non-zero and other non-zero valves.. (sort dynamically) 
then start with the top one.. 

to make this work.. we must has a way to tell it to stop...
the 30 minutes budget seems like the stop condition.. 

like I don't care the flow-rate.. I focus on getting as much as valves opened??

"""
from collections import defaultdict
from functools import cache

"""
the twist of this problem is the time limit
which actually limits the dfs/backtrack/permutation stuff to small enough to solve 

so okay let us do it

"""


def default_dist():
    return 100000


class Solution:
    def __init__(self, filename):
        self.graph = {}
        self.rates = defaultdict(int)
        self.distances = defaultdict(default_dist)
        self.parse_input(filename)

    def parse_input(self, filename):
        with open(filename) as f:
            for line in f:
                fields = line.strip().split(maxsplit=9)
                valve = fields[1]
                rate = int(fields[4].split('=')[-1][:-1])
                neighbors = [nei.strip() for nei in fields[9].split(',')]
                if rate:
                    self.rates[valve] = rate
                self.graph[valve] = neighbors

        # also build the distance grid between AA and non-zero valves
        for valve, adj_sets in self.graph.items():
            self.distances[valve, valve] = 0
            for nei in adj_sets:
                self.distances[(valve, nei)] = 1

        for i in self.graph:
            for j in self.graph:
                for k in self.graph:
                    if i != k:
                        self.distances[(j, k)] = min(self.distances[(j, k)],
                                                     self.distances[j, i] + self.distances[(i, k)])

    def _solve(self):
        # cache by myself
        mem = {}

        def helper(valve, time, opened):
            if time <= 1:
                return 0

            if (valve, time, opened) in mem:
                return mem[valve, time, opened]

            res = 0
            for nei in self.graph[valve]:
                res = max(res, helper(nei, time - 1, opened))

            if valve not in opened and self.rates[valve]:
                opened = tuple([*opened, valve])
                res = max(res, helper(valve, time - 1, opened) + self.rates[valve] * (time - 1))

            mem[valve, time, opened] = res
            return res

        return helper('AA', 30, ())

    def solve(self):
        @cache
        def one_step_walker(valve, time, opened):
            if time <= 1:
                return 0

            res = 0
            # why do I need to do this for loop: not open myself first?
            # swap the order this is wrong
            # ah I kinda see
            # you lost the option of not-opening this valve
            # which is kind of back-track.. if you need to
            for nei in self.graph[valve]:
                res = max(res, one_step_walker(nei, time - 1, opened))

            if valve not in opened and self.rates[valve]:
                opened = tuple([*opened, valve])
                res = max(res, one_step_walker(valve, time - 1, opened) + self.rates[valve] * (time - 1))

            return res

        @cache
        def one_step_walker_bt(valve, time, opened):
            # try open this valve first, then backtrack
            # yeah... looks like it will be correct this time
            if time <= 1:
                return 0

            res = 0

            if valve not in opened and self.rates[valve]:
                old = opened
                opened = tuple([*opened, valve])
                res = max(res, one_step_walker_bt(valve, time - 1, opened) + self.rates[valve] * (time - 1))
                opened = old

            for nei in self.graph[valve]:
                res = max(res, one_step_walker_bt(nei, time - 1, opened))

            return res

        @cache
        def big_strikes(valve, time, opened):
            if time <= 1:
                return 0

            res = 0

            # open this valve first
            # cannot do this first.. must do it later (backtrack implicitly lost)
            # or you explicitly backtrack
            if valve not in opened and self.rates[valve]:
                old = opened
                opened = tuple([*opened, valve])
                res = max(res, big_strikes(valve, time - 1, opened) + self.rates[valve] * (time - 1))
                opened = old

            # travel to other valve first
            next_targets = [n for n in self.graph if self.rates[n] and n != valve and n not in opened]
            for n in next_targets:
                res = max(res, big_strikes(n, time - self.distances[valve, n], opened))

            return res

        return big_strikes('AA', 30, ())

    def solve_iterative(self):
        order_run = 1

        def all_orders(node, todo, done, time):
            """
            figures out all eligible orders to run
            fact(15) is > 1 trillion but becomes of the time limit, so the total number of orders is not that great

            tricks in this function
                - copy the parameter every time.. instead of maintaining a changing state
                - done when yield is the sequence
                - the open operation is captured by +1
                    - because this is dealing in order no back forth
                    - so open is implicit and just a +1
            """
            for next_node in todo:
                cost = self.distances[node, next_node] + 1
                if cost < time:
                    yield from all_orders(next_node, todo - {next_node}, done + [next_node], time - cost)
            yield done

        def run_order(costs, start_node, nodes, t):
            release = 0
            curr = start_node
            for node in nodes:
                cost = costs[curr, node] + 1
                t -= cost
                assert t > 0
                release += t * self.rates[node]
                curr = node
            nonlocal order_run
            order_run += 1
            return release

        none_zero_nodes = {n for n in self.rates if self.rates[n]}
        orders = all_orders('AA', none_zero_nodes, [], 30)

        res = max(run_order(self.distances, 'AA', order, 30) for order in orders)
        print(order_run)
        return res


if __name__ == '__main__':
    input_file = 'day16_sample.txt'
    S = Solution(input_file)
    print(S.solve_iterative())

    input_file = 'day16_input.txt'
    S = Solution(input_file)
    print(S.solve_iterative())
