class TreeNode:
    def __init__(self, val, sub_nodes=None, file_sizes=None):
        self.val = val
        # sub folders represented as nodes
        self.sub_nodes = sub_nodes if sub_nodes else {}
        self.file_sizes = file_sizes if file_sizes else []

    def calculate(self):
        under_100k = 0
        folder_sizes = []

        def helper(node):
            nonlocal under_100k
            if node is None:
                return 0

            dir_size = sum(node.file_sizes)
            for sub_node in node.sub_nodes.values():
                dir_size += helper(sub_node)

            if dir_size <= 100000:
                under_100k += dir_size
            folder_sizes.append(dir_size)
            return dir_size

        return helper(self), under_100k, folder_sizes


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
                        # at most go back to root folder
                        if len(stack) > 1:
                            stack.pop()
                            curr = stack[-1]
                    else:
                        curr = curr.sub_nodes[dir]
                        stack.append(curr)

                if line.startswith("$ ls"):
                    # list dir - do nothing
                    ...
            elif line.startswith('dir'):
                # a line containing a dir
                dir = line.strip().split()[1]
                curr.sub_nodes[dir] = TreeNode(dir)
            else:
                # size filename
                curr.file_sizes.append(int((line.strip().split()[0])))
    return dummy


def get_first_enough_folder_size(total_size, folder_sizes):
    free = 70000000 - total_size
    for folder_size in sorted(folder_sizes):
        if free + folder_size >= 30000000:
            return folder_size

    return -1


if __name__ == '__main__':
    input_file = 'day7_sample.txt'
    node = build_tree(input_file)
    total_size, under_100k_sum, sizes = node.calculate()
    print(under_100k_sum)
    print(get_first_enough_folder_size(total_size, sizes))

    input_file = 'day7_input.txt'
    node = build_tree(input_file)
    total_size, under_100k_sum, sizes = node.calculate()
    print(under_100k_sum)
    print(get_first_enough_folder_size(total_size, sizes))
