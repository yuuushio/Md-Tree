import re
import sys
import argparse
import os


class St:
    def __init__(self, val):
        self.val = val
        self.whitespace = 0
        self.depth = 0
        self.is_last = False
        self.stripped_val = ""


def read_file(file):
    with open(file, "r") as f:
        data = f.readlines()
        return [St(d) for d in data]


def assign_true_value(st_arr):
    text = []

    for i in st_arr:
        # strips everything till the first character after the bullet point
        tmp = re.sub(r"^\s*[-*+]\s+", "", i.val)
        text.append(tmp.strip())
    for i in range(len(text)):
        st_arr[i].stripped_val = text[i]


def assign_depth_and_whitespace(st_arr):
    whitespace_arr = []
    for s in st_arr:
        v = s.val
        s.whitespace = len(re.match(r"^\s*", v).group(0))
        whitespace_arr.append(s.whitespace)
    
    l = [x for x in whitespace_arr if x != 0]
    # depth 1 will have the minimum whitespace; everything else will be relative to that
    if l:
        # Incase the input file only contains items with depth 0 (or 1 item)
        min_whitespace = min(l)
    for i in range(len(st_arr)):
        if whitespace_arr[i] != 0:
            st_arr[i].depth = whitespace_arr[i] // min_whitespace


# Mark all nodes in the dict as last-nodes
def assign_last(di, cur_depth):
    for k, v in di.items():
        # You only want to assign lasts for nodes that are greater than the depth the
        #  pointer is currently pointing at
        if k > cur_depth:
            v.is_last = True


def calc_last(arr):
    # Dict that contains the last st-object for its respective depth/section
    d = {}
    for i, item in enumerate(arr):
        # Essentially acts as a pointer to the current depth
        cur_depth = item.depth
        # The value for each depth gets replaced by the latest node of that depth
        d[item.depth] = item

        if i + 1 == len(arr):
            assign_last(d, -1)
        else:
            # Whenever there's a backwards change in depth
            if cur_depth < arr[i - 1].depth:
                arr[i - 1].is_last = True
                # Assign last to all the nodes up till this pointer (not inclusive)
                assign_last(d, cur_depth)


def print_grid(d_arr):
    # debug purposes
    for li in d_arr:
        print(li)


# List containing the final pre-space/indent/unicode-chars for each item
def construct_indent(grid):
    # the grid will always be n by n
    return_list = []
    for i in range(len(grid)):
        tmp = ""
        for j in range(len(grid)):
            if grid[i][j] == None:
                break
            else:
                tmp += grid[i][j]
        return_list.append(tmp)
    return return_list


def print_tree(indent_list, st_arr):
    print(".")
    for i, item in enumerate(st_arr):
        print(indent_list[i] + item.stripped_val)


def make_prespace_grid(arr):
    # ^1: i'th item can have a max depth of i
    # item 0, d=0
    # item 1, d=0,1
    # item 2, d=0,1,2

    s_a = "├── "
    s_b = "└── "
    s_c = "│   "
    s_d = "    "

    # Initialize grid, depth_0 (j=0) will always have a pre-space/indent of ""
    grid = [[None if j != 0 else s_c for j in range(len(arr))] for i in range(len(arr))]

    # since we don't want to display the unicode characters past last depth 0 node
    past_last = False

    # otherwise it's gonna write out string past the last depth 0 node
    for i in range(0, len(arr)):
        for j in range(len(arr)):
            if j != 0 and arr[i].depth != 0:
                if arr[i].depth == j and j == 1:
                    pre_space = ""
                    if not arr[i].is_last:
                        pre_space = s_a
                    elif arr[i].is_last:
                        pre_space = s_b
                    elif grid[i - 1][j] == s_a:
                        pre_space = s_c
                    grid[i][j] = pre_space

                elif j == 1:
                    if grid[i - 1][j] == s_c:
                        grid[i][j] = s_c
                    elif grid[i - 1][j] == s_b:
                        grid[i][j] = s_d
                    if j < i:
                        pre_space = ""
                        if grid[i - 1][j] == s_b:
                            pre_space = s_d
                        elif grid[i - 1][j] == s_a:
                            pre_space = s_c
                        elif grid[i - 1][j] == s_c:
                            pre_space = s_c
                        else:
                            pre_space = s_d
                        grid[i][j] = pre_space
                elif arr[i].depth == j:
                    pre_space = ""
                    if arr[i].is_last:
                        pre_space = s_b
                    elif not arr[i].is_last:
                        pre_space = s_a
                    elif grid[i - 1][j] == s_a:
                        pre_space = s_c
                    elif grid[i - 1][j] == s_b:
                        pre_space = s_d
                    grid[i][j] = pre_space
                elif j > arr[i].depth:
                    # break inner loop as per rule ^1
                    break
                elif j < i:
                    pre_space = ""
                    if grid[i - 1][j] == s_b:
                        pre_space = s_d

                    elif grid[i - 1][j] == s_a:
                        pre_space = s_c

                    elif grid[i - 1][j] == s_c:
                        pre_space = s_c
                    else:
                        pre_space = s_d

                    grid[i][j] = pre_space

                else:
                    # j == i
                    # i-1][j-1] ...
                    break
            else:
                # depth == 0
                if arr[i].depth == 0 and not arr[i].is_last:
                    grid[i][0] = s_a
                else:
                    if arr[i].depth == 0 and arr[i].is_last:
                        past_last = True
                        # depth 0 node is last
                        grid[i][0] = s_b
                    else:
                        # Empty indent if we're past the last depth 0 node
                        grid[i][0] = s_d if past_last else s_c

    # print_grid(grid)
    print_tree(construct_indent(grid), arr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", help="File containing the markdown-style list.", required=True
    )
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()

    if not os.path.isfile(args.file):
        print(f"Path or file not valid.")

    st_arr = read_file(args.file)

    assign_depth_and_whitespace(st_arr)
    calc_last(st_arr)
    assign_true_value(st_arr)
    make_prespace_grid(st_arr)  


if __name__ == "__main__":
    main()

# Tests #
# - [x] list with only 1 item
# - [x] list where all items are depth 0
# - [x] three depth 0 items, and one depth 1 item which is under the first item
