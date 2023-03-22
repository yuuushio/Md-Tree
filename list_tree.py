import re

# def generate_tree_from_file(file_path):
#     # Read the markdown list from file
#     with open(file_path, 'r') as f:
#         md_list = f.read()
#     
#     # Generate the tree from markdown list
#     print(md_list)
#     generate_tree(md_list)
#
# # def generate_tree(md_list):
# #     # Convert markdown list to plain text
# #     text = re.sub(r'^\s*[-*+]\s+', '', md_list, flags=re.MULTILINE)
# #     
# #     # Split text into lines
# #     lines = text.split('\n')
# #     
# #     # Determine the depth of each line
# #     depths = [len(line) - len(line.lstrip()) for line in lines]
# #     print(depths)
# #     print(lines)
# #     
# #     # Create the tree structure
# #     tree = []
# #     stack = [tree]
# #     for i, line in enumerate(lines):
# #         node = {'name': line.strip(), 'children': []}
# #         depth = depths[i]
# #         while depth < len(stack) - 1:
# #             stack.pop()
# #         if stack:
# #             stack[-1][-1]['children'].append(node)
# #         stack.append(node['children'])
# #     
# #     # Print the tree
# #     print_tree(tree)
# #     
# # def print_tree(tree, indent=''):
# #     for i, node in enumerate(tree):
# #         is_last = i == len(tree) - 1
# #         print(indent + ('└── ' if is_last else '├── ') + node['name'])
# #         if node['children']:
# #             print_tree(node['children'], indent + ('    ' if is_last else '│   '))
# #
# #
#
#
# def generate_tree(md_list):
#     # Convert markdown list to plain text
#     text = re.sub(r'^\s*[-*+]\s+', '', md_list, flags=re.MULTILINE)
#
#     # Split text into lines
#     lines = text.split('\n')
#
#     # Determine the depth of each line
#     depths = [len(line) - len(line.lstrip()) for line in lines]
#
#     # Create the tree structure
#     tree = []
#     stack = [tree]
#     for i, line in enumerate(lines):
#         node = {'name': line.strip(), 'children': []}
#         depth = depths[i]
#         while depth < len(stack) - 1:
#             stack.pop()
#         if stack:
#             stack[-1].append(node)
#         stack.append(node['children'])
#     
#     # Print every node
#     print_node(tree)
#
# def print_node(node, indent=''):
#     print(indent + node['name'])
#     for child in node['children']:
#         print_node(child, indent + '  ')
# file_path = "file.txt"
# generate_tree_from_file(file_path)


def print_tree(nodes, depth=0):
    for node in nodes:
        if node.startswith("#"):
            continue
        if node.startswith("-"):
            node = node[2:]
        print("    " * depth + "- " + node.strip())
        
def read_md_file(filename):
    with open(filename, "r") as f:
        nodes = f.readlines()
    return nodes

filename = "file.txt"
nodes = read_md_file(filename)
print_tree(nodes)
