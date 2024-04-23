#!/usr/bin/env python3
#

# Generic useful stuff for semantic analysis and interpretation/code generation

import sys
from tree_print import get_childvars


# A class for collecting data needed during semantic analysis etc.
# By default contains the symbol table

class SemData:
  def __init__(self):
    self.symtbl = dict()

# An element in the symbol table, by default containing symbols type
# and reference to its definition in the syntax tree

class SymbolData:
  def __init__(self, symtype, defnode):
    self.symtype = symtype
    self.defnode = defnode

# The function is given the root of the tree 
def visit_tree(node, before_func=None, after_func=None, semdata=None):
  '''A generic visitor (which uses tree_print.get_childvars)
  
     Parameters:
     node: root of the (sub)tree to be traversed
     before_func: When a node is found, this function is first called,
                then all the childrens of the node are visited recursively, then
                the second function (after_func) is called. NOTE: If function returns
                anything except None, it's regarded as an error message, which is printed
                out and execution is terminated. If node contains an attribute 'lineno',
                that's included in the error message.
     after_func: When a node is found, the func_before function is first called,
                then all the childrens of the node are visited recursively, then
                this function is called. NOTE: If function returns
                anything except None, it's regarded as an error message, which is printed
                out and execution is terminated. If node contains an attribute 'lineno',
                that's included in the error message.
     semdata: optional data that is passed to all functions'''

  if before_func:
    err = before_func(node, semdata)
    if not err is None:
      if hasattr(node, "lineno"):
        err = "Line " + str(node.lineno) + ": " + err
      print(err)
      sys.exit()

  children = get_childvars(node)

  for name,child in children:
    if child:
      visit_tree(child, before_func, after_func, semdata)

  if after_func:
    err = after_func(node, semdata)
    if not err is None:
      if hasattr(node, "lineno"):
        err = "Line " + str(node.lineno) + ": " + err
      print(err)
      sys.exit()
