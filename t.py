import re


class St:
    def __init__(self, val):
        self.val = val
        self.parent = None
        self.whitespace = 0
        self.depth = 0
        self.is_last = False
        self.stripped_val = ""

    # for debugging purposes
    def print_val(self):
        if self.parent is None:
            print("val:", self.val, "parent:", None)
        else:
            print(
                "val:",
                self.val,
                "parent:",
                self.parent.val,
                "depth:",
                self.depth,
                "is_last:",
                self.is_last
            )


def read_file():
    with open("file.txt", "r") as f:
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

    # depth 1 will have the minimum whitespace; everything else will be relative to that
    min_whitespace = min(x for x in whitespace_arr if x != 0)
    for i in range(len(st_arr)):
        if whitespace_arr[i] != 0:
            st_arr[i].depth = whitespace_arr[i] // min_whitespace

# Mark all nodes in the dict as last-nodes
def assign_last(di):
    for k,v in di.items():
        v.is_last = True


def calc_if_last(st_arr):
    # {depth, node} dict
    last_of_depth = {}
    for i in range(len(st_arr)):
        # This list contains the last node of each depth
        last_of_depth[st_arr[i].depth] = st_arr[i]

        # last item
        if i + 1 == len(st_arr):
            assign_last(last_of_depth)
            last_of_depth.clear()
        elif st_arr[i+1].depth < st_arr[i].depth:
            st_arr[i].is_last = True
            # if this node is last, but the next one is also a parent - we need to perform the if parent check as well
            # otherwise some of the items in the current dict will get overriden by items from the next parent's list
            if st_arr[i+1].depth == 0:
                del last_of_depth[0]
                # next node is parent
                assign_last(last_of_depth)
                last_of_depth.clear()
        elif st_arr[i+1].depth == 0:
            del last_of_depth[0]
            # next node is parent
            assign_last(last_of_depth)
            last_of_depth.clear()


def assign_parent(c, parent):
    # usually done when current's space is less parent's space
    #   if tmp was parent, tmp now equals tmp.parent
    tmp = parent
    while (c.whitespace < tmp.whitespace):
        # it's back-tracking at this point so, prev nodes will have parents assigned to them
        if tmp.parent is not None:
            tmp = tmp.parent
    # if the list has correct markdown syntax/indent, == should be g
    if c.whitespace == tmp.whitespace:
        c.parent = tmp.parent


def tst(zzz):
    for z in zzz:
        z.print_val()

def print_func():
    pass

def print_grid(d_arr):
    for li in d_arr:
        print(li)


# print("│   " * (items[i].depth-1) + "└── " + text[i])
def magic(arr):
    # ^1: i'th item can have a max depth of i
    # item 0, d=0
    # item 1, d=0,1 
    # item 2, d=0,1,2

    s_a = "├── "

    s_b = "└── "
    s_c = "│   "
    s_d = "    "

    # Initialize grid, depth_0 (j=0) will always have a pre-space/indent of ""
    grid = [[None if j!=0 else "" for j in range(len(arr))] for i in range(len(arr))]
      
    for i in range(1,len(arr)):
        for j in range(len(arr)):
            if j != 0 and arr[i].depth != 0:
                if arr[i].depth == j and j == 1:
                    pre_space = ""
                    if not arr[i].is_last:
                        pre_space = s_a
                    elif grid[i-1][j] == s_a:
                        pre_space = s_c
                    elif arr[i].is_last and not arr[i].parent.is_last:
                        pre_space = s_a
                    elif arr[i].is_last and arr[i].parent.is_last:
                        pre_space = s_b
                    grid[i][j] = grid[i-1][j-1] + pre_space
                elif j == 1:
                    print(i,j,"found 2 1 ...")
                    if grid[i-1][j] == s_c:
                        grid[i][j] = s_c
                    elif grid[i-1][j] == s_b:
                        grid[i][j] = s_d
                    if j < i:
                        pre_space = ""
                        if grid[i-1][j] == s_b:
                            pre_space = s_d
                        elif grid[i-1][j] == s_a:
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
                    elif grid[i-1][j] == s_a:
                        pre_space = s_c
                    elif grid[i-1][j] == s_b:
                        pre_space = s_d
                    grid[i][j] = pre_space
                elif j > arr[i].depth:
                    # break inner loop as per rule ^1
                    break
                elif j < i:
                    print(i,j)
                    pre_space = ""
                    if grid[i-1][j] == s_b:
                        pre_space = s_d
                    elif grid[i-1][j] == s_a:
                        pre_space = s_c
                    else:
                        pre_space = s_d

                    grid[i][j] = pre_space

                else:
                    # j == i
                    # i-1][j-1] ...
                    break






    print_grid(grid)
    # for i,item in enumerate(arr):
    #     print(grid[i][item.depth] + item.stripped_val + " ", item.is_last) 





# Need this method to stop printing bar under the last node of (last of its respective depth)
# O(n^2) because we are iterating back to calculate the parent of the node,
#   and in the worst case, this parent is at index 1
def calc_parent(st_li):
    # parent = [i-1]
    for i in range(len(st_li)):
        if i == 0:
            continue
        if st_li[i].whitespace < st_li[i-1].whitespace:
            assign_parent(st_li[i], st_li[i-1])
        elif st_li[i].whitespace == st_li[i-1].whitespace:
            st_li[i].parent = st_li[i-1].parent
        else:
            st_li[i].parent = st_li[i-1]


    return st_li


def main():
    st_arr = read_file()
    assign_depth_and_whitespace(st_arr)
    calc_if_last(st_arr)
    calc_parent(st_arr)
    # build_tree(st_arr)
    assign_true_value(st_arr)
    magic(st_arr)


if __name__ == "__main__":
    main()
