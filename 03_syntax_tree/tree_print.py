#!/usr/bin/env python3
# ----------------------------------------------------------------------

# Values to control the module's working

# How to recognize attributes in nodes by their names

child_prefix_default = "child_"
children_prefix_default = "children_"
value_attr = "value"
type_attr = "nodetype"


# Finding and creating a list of all children nodes of a node, based on
# attribute names of a node

def get_childvars(node, child_prefix=child_prefix_default,
                  children_prefix=children_prefix_default):
    '''Return all children nodes of a tree node

    This function assumes that all attributes of a node beginning with
    child_prefix refer to a child node, and attributes beginning with
    children_prefix refer to a LIST of child nodes. The return value is a list
    of pairs (tuples), where the first element of each pair is a "label"
    for the node (the name of the attribute without the child/children prefix),
    and the second element is the child node itself. For child lists, the label
    also contains the number of the child, or EMPTY if the list is empty
    (in which case None is used as the second element, as there is no child).'''

    childvars = []
    # Only search for attributes if we have an object
    if hasattr(node, "__dict__"):
        # Iterate though all attributes of the node object
        for name, val in vars(node).items():
            # An attribute containing one child node
            if name.startswith(child_prefix):
                label = name[len(child_prefix):]
                childvars.append((label, val))
            # An attribute containing a child list
            elif name.startswith(children_prefix):
                label = name[len(children_prefix):]
                # Make sure contents is not None and is a list (or actually, can
                # be iterated through
                if val is None:
                    childvars.append((label + "[NONE stored instead of a list!!!]", None))
                else:
                    assert not val is None, "'None' passed as children list!"
                    assert hasattr(val, "__iter__"), "Children list is not a list!!!"
                    # An empty list/iterable (no nodes)
                    if not val:
                        childvars.append((label + "[EMPTY]", None))
                    # A non-empty list/iterable
                    else:
                        childvars.extend([(label + "[" + str(i) + "]", child) for (i, child) in enumerate(val)])
    return childvars


# Printing the syntax tree (AST)

# Strings that ASCII and Unicode trees are made out of

vertical_uni = "\N{BOX DRAWINGS LIGHT VERTICAL}"
horizontal_uni = "\N{BOX DRAWINGS LIGHT HORIZONTAL}"
vertical_right_uni = "\N{BOX DRAWINGS LIGHT VERTICAL AND RIGHT}"
up_right_uni = "\N{BOX DRAWINGS LIGHT UP AND RIGHT}"
child_indent_uni = vertical_right_uni + horizontal_uni + horizontal_uni
last_child_indent_uni = up_right_uni + horizontal_uni + horizontal_uni
normal_indent_uni = vertical_uni + "  "
last_normal_indent_uni = "   "

vertical_asc = "|"
horizontal_asc = "-"
vertical_right_asc = "+"
up_right_asc = "+"
child_indent_asc = vertical_right_asc + horizontal_asc + horizontal_asc
last_child_indent_asc = up_right_asc + horizontal_asc + horizontal_asc
normal_indent_asc = vertical_asc + "  "
last_normal_indent_asc = "   "

# What to put to the beginning and end of dot files

dot_preamble = '''digraph parsetree {
    ratio=fill
    node [shape="box"]
    edge [style=bold]
    ranksep=equally
    nodesep=0.5
    rankdir = TB
    clusterrank = local'''

dot_postamble = '}'


def dotnodeid(nodenum):
    '''Convert node number to a dot id'''
    return "N" + str(nodenum)


def treeprint_indent(node, outtype="unicode", label="", first_indent="", indent=""):
    '''Print out an ASCII/Unicode version of a subtree in a tree.

    node = the root of the subtree
    outtype = unicode/ascii
    label = the "role" of the subtree on the parent node (from attribute name)
    first_indent = what to print at the beginning of the first line (indentation)
    indent = what to print at the beginning of the rest of the lines (indentation)'''

    # Add label (if any) to the first line after the indentation
    if label:
        first_indent += label + ": "
    if not node:
        # If node is None, just print NONE
        print(first_indent + "NONE")
    else:
        # If node has node type attribute, print that, otherwise try to print the whole
        # node take help in finding the error
        if hasattr(node, type_attr):
            print(first_indent + getattr(node, type_attr), end="")
        else:
            print(first_indent + "??? '" + str(node) + "' ???", end="")
        # If node has a value attribute, print the value of the node in parenthesis
        if hasattr(node, value_attr):
            print(" (" + str(node.value) + ")")
        else:
            print()
        # Get all children of the node and iterate through them
        childvars = get_childvars(node)
        i = len(childvars)
        for name, value in childvars:
            i -= 1
            if i > 0:
                # Not the last child, use normal indentation
                if outtype == "unicode":
                    first_indent = child_indent_uni
                    rest_indent = normal_indent_uni
                else:
                    first_indent = child_indent_asc
                    rest_indent = normal_indent_asc
            else:
                # The last child, use indentation for that case
                if outtype == "unicode":
                    first_indent = last_child_indent_uni
                    rest_indent = last_normal_indent_uni
                else:
                    first_indent = last_child_indent_asc
                    rest_indent = last_normal_indent_asc
            # Recursively print the child subtrees, adding indentation
            treeprint_indent(value, outtype, name, indent + first_indent,
                             indent + rest_indent)


def treeprint_dot(node, nodenum, nodecount):
    '''Print a subtree in dot format.

    nodenum = number of the node (for dot id generation)
    nodecount = a list containing the maximum used id'''

    nodeline = dotnodeid(nodenum)
    if not node:
        # None is output as an ellipse with label NONE
        nodeline += ' [shape="ellipse", label="NONE"]'
        print(nodeline)
    else:
        # Normal nodes use the default shape
        nodeline += ' [label="'
        # If node has node type attribute, print that, otherwise try to print the whole
        # node take help in finding the error
        if hasattr(node, type_attr):
            nodeline += getattr(node, type_attr)
        else:
            nodeline += "??? '" + str(node) + "' ???"
        # If node has a value attribute, output the value in parenthesis
        if hasattr(node, value_attr):
            nodeline += " (" + str(node.value) + ")"
        nodeline += '"]'
        print(nodeline)
        # Get all children of the node and iterate through them
        childvars = get_childvars(node)
        for name, value in childvars:
            # Number the child by one more than current maximum (and update maximum)
            nodecount[0] += 1
            childnum = nodecount[0]
            # Recursively print the child subtrees
            treeprint_dot(value, childnum, nodecount)
            # Output the named connection between parent and child
            print(dotnodeid(nodenum) + "->" + dotnodeid(childnum) + ' [label="' + name + '"]')


def treeprint(rootnode, outtype="unicode"):
    '''Prints out a tree, given its root.

       The second argument is the output type:
       "unicode" (default) prints a text-version of the tree using Unicode block characters.
       "ascii" prints an ASCII-only version, with |, -, +.
       "dot" prints a tree in dot format (can be converted to a graphical tree
       using dot command in graphwiz).'''
    if outtype == "dot":
        print(dot_preamble)
        treeprint_dot(rootnode, 0, [0])
        print(dot_postamble)
    else:
        treeprint_indent(rootnode, outtype)
