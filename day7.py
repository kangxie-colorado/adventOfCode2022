from typing import List


class TreeNode:
    def __init__(self, val, sub_nodes=None, file_sizes=None):
        self.val = val
        # sub folders represented as nodes
        self.sub_nodes = sub_nodes if sub_nodes else {}
        self.file_sizes = file_sizes if file_sizes else []

    def calculate_size_at_most_100k(self):
        sum_node_under_100k = 0
        folder_sizes = []
        def helper(node):
            nonlocal sum_node_under_100k
            if node is None:
                return 0

            dir_size = sum(node.file_sizes)
            for sub_node in node.sub_nodes.values():
                dir_size += helper(sub_node)

            if dir_size <= 100000:
                sum_node_under_100k += dir_size
            folder_sizes.append(dir_size)
            return dir_size

        return helper(self), sum_node_under_100k, folder_sizes


def build_tree(filename):
    dummy = TreeNode('', {'/': TreeNode('/'), })
    curr = dummy
    stack = []
    with open(filename) as f:
        for line in f:
            if line.startswith('$'):
                # a command line
                if line.startswith("$ cd"):
                    # change dir
                    dir = line.strip()[5:]
                    if dir == "..":
                        if stack:
                            stack.pop()
                            curr = stack[-1]
                    else:
                        curr = curr.sub_nodes[dir]
                        stack.append(curr)

                if line.startswith("$ ls"):
                    # list dir
                    listing = True
            elif line.startswith('dir'):
                # a line containing a dir
                dir = line.strip().split()[1]
                curr.sub_nodes[dir] = TreeNode(dir)
            else:
                # size filename
                curr.file_sizes.append(int((line.strip().split()[0])))
    return dummy


if __name__ == '__main__':
    input_file = 'day7_sample.txt'
    node = build_tree(input_file)

    total_size, sum_node_under_100k, folder_sizes = node.calculate_size_at_most_100k()
    print(sum_node_under_100k)
    free = 70000000 - total_size
    for folder_size in sorted(folder_sizes):
        if free+folder_size >= 30000000:
            print(folder_size)
            break

    input_file = 'day7_input.txt'
    node = build_tree(input_file)

    total_size, sum_node_under_100k, folder_sizes = node.calculate_size_at_most_100k()
    print(sum_node_under_100k)
    free = 70000000 - total_size
    for folder_size in sorted(folder_sizes):
        if free+folder_size >= 30000000:
            print(folder_size)
            break