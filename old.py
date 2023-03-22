import re


class St:
    def __init__(self, val):
        self.val = val
        self.parent = None
        self.whitespace = 0
        self.depth = 0
        self.is_last = False

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


def build_tree(items):
    text = []

    for i in items:
        # strips everything till the first character after the bullet point
        tmp = re.sub(r"^\s*[-*+]\s+", "", i.val)
        text.append(tmp.strip())

    # There is a correlation between indent and depth
    # We probably don't even need to calculate the parents since everything can be done using depth
    for i in range(len(items)):
        # if the current node is the child/last node
        # if i + 1 == len(items):
        #     print("│   " * (items[i].depth-1) + "└── " + text[i])
        # # if the next node is not the child of the current, nor is it in line with it
        # elif items[i + 1].depth < items[i].depth:
        #     print("│   " * (items[i].depth-1) + "└── " + text[i])

        if items[i].depth == 0:
            print(text[i])
        elif items[i].is_last:
            print("│   " * (items[i].depth-1) + "└── " + text[i])
        # elif items[i + 1].depth < items[i].depth:
        #     print("│   " * (items[i].depth-1) + "└── " + text[i])
        else:
            print("│   " * (items[i].depth-1) + "├── " + text[i])


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
    build_tree(st_arr)


if __name__ == "__main__":
    main()
