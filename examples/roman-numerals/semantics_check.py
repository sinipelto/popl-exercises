#!/usr/bin/env python3
#

from semantics_common import visit_tree, SymbolData, SemData

# Define semantic check functions


# Stupid check, make sure all numbers are < 10
def check_literals(node, semdata):
  nodetype = node.nodetype
  if nodetype == 'literal':
    if node.value >= 10:
      return "Literal "+str(node.value)+" too large!"

# Check that the stack size remains acceptable within operations
def check_stack_size_before(node, semdata):
  nodetype = node.nodetype
  if nodetype == 'unary_op': # Push
    if node.value == '⇑':
      # One more push done to stack
      semdata.stack_size = semdata.stack_size + 1
    else:
      return "Unknown unary_op "+node.value
  elif nodetype == '⇓': # Pop
    # One more drop done to stack
    semdata.stack_size = semdata.stack_size - 1
  elif nodetype == 'ψ': # Print
    # Check that stack is not empty, remove one
    if semdata.stack_size == 0:
      return "Nothing in stack!"
    semdata.stack_size = semdata.stack_size - 1
  elif nodetype == '↔': # Swap
     # Check that at least two items are in stack
    if semdata.stack_size < 2:
      return "Too few items in stack for swap!"
  elif nodetype == 'complex_stmt':
    if node.child_op.nodetype == '↔': # Swap
      # Check that enough items are in stack
      if semdata.stack_size < node.child_idx1.value or semdata.stack_size < node.child_idx2.value:
        return "Too few items in stack for complex swap!"
  elif nodetype == '⊕' or nodetype == '⊖': # Add or subtract
    # Check that at least two items are in stack, remove one
    if semdata.stack_size < 2:
      return "Too few items in stack for add/sub!"
    semdata.stack_size = semdata.stack_size - 1
  elif nodetype == 'program':
    # Store old stack size when embedded program starts
    semdata.old_stack_sizes.append(semdata.stack_size)

def check_stack_size_after(node, semdata):
  nodetype = node.nodetype
  if nodetype == 'program':
    # Restore old stack size when embedded program ends
    semdata.stack_size = semdata.old_stack_sizes.pop()


def semantic_checks(tree, semdata):
  '''run all semantic checks'''
  visit_tree(tree, check_literals, None, semdata)
  semdata.stack_size = 0 # Initially stack is empty
  semdata.old_stack_sizes = [] # Initially no old stacks
  visit_tree(tree, check_stack_size_before, check_stack_size_after, semdata)

import tokenizer
import tree_generation
import tree_print
parser = tree_generation.parser

if __name__ == "__main__":
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file', help='filename to process')

    ns = arg_parser.parse_args()

    if ns.file is None:
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        ast_tree = parser.parse(data, lexer=tokenizer.lexer, debug=False)
        tree_print.treeprint(ast_tree)

        semdata = SemData()
        semdata.in_function = None
        semantic_checks(ast_tree, semdata)
        print("Semantics ok:")
