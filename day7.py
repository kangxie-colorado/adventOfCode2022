class TreeNode:
    def __init__(self, val, sub_nodes=None, file_sizes=None):
        self.val = val
        # sub folders represented as nodes
        self.sub_nodes = sub_nodes if sub_nodes else {}
        self.file_sizes = file_sizes if file_sizes else []

    def calculate_folder_sizes(self):
        folder_sizes = []

        def helper(node):
            if node is None:
                return 0
            dir_size = sum(node.file_sizes)
            for sub_node in node.sub_nodes.values():
                dir_size += helper(sub_node)

            folder_sizes.append(dir_size)
            return dir_size

        return helper(self), folder_sizes


def build_tree(filename):
    root = TreeNode('', {'/': TreeNode('/'), })
    curr = root
    stack = []
    with open(filename) as f:
        for line in f:
            if line.startswith('$'):
                # a command line
                if line.startswith("$ cd"):
                    # change dir
                    folder = line.strip()[5:]
                    if folder == "..":
                        # at most go back to root folder
                        if len(stack) > 1:
                            stack.pop()
                            curr = stack[-1]
                    else:
                        curr = curr.sub_nodes[folder]
                        stack.append(curr)

                if line.startswith("$ ls"):
                    # list dir - do nothing
                    ...
            elif line.startswith('dir'):
                # a line containing a dir
                folder = line.strip().split()[1]
                curr.sub_nodes[folder] = TreeNode(folder)
            else:
                # size filename
                curr.file_sizes.append(int((line.strip().split()[0])))
    return root


def get_sum_of_under_100k(folder_sizes):
    under_100K_sum = 0
    for s in sizes:
        if s < 100000:
            under_100K_sum += s

    return under_100K_sum


def get_first_enough_folder_size(used, folder_sizes):
    free = 70000000 - used
    for folder_size in sorted(folder_sizes):
        if free + folder_size >= 30000000:
            return folder_size

    return -1


if __name__ == '__main__':
    input_file = 'day7_sample.txt'
    root = build_tree(input_file)
    total_size, sizes = root.calculate_folder_sizes()
    print(get_sum_of_under_100k(sizes))
    print(get_first_enough_folder_size(total_size, sizes))

    input_file = 'day7_input.txt'
    root = build_tree(input_file)
    total_size, sizes = root.calculate_folder_sizes()
    print(get_sum_of_under_100k(sizes))
    print(get_first_enough_folder_size(total_size, sizes))
