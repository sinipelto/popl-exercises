#!/usr/bin/env python3
#

from semantics_common import SymbolData, SemData

def run_program(tree, semdata):
  semdata.old_stacks = []
  semdata.stack = []
  eval_node(tree, semdata)

def eval_node(node, semdata):
  symtbl = semdata.symtbl
  nodetype = node.nodetype
  if nodetype == 'program':
    # Copy and store current stack
    semdata.old_stacks.append(semdata.stack.copy())
    for i in node.children_stmts:
      eval_node(i, semdata)
    # Restore stack
    semdata.stack = semdata.old_stacks.pop()
    return None
  elif nodetype == 'unary_op':
    if node.value == '⇑': # Push
      semdata.stack.append(node.child_roman.value)
    else:
      print("Impossible unary_op", node.value)
    return None
  elif nodetype == '⇓': # Pop
    semdata.stack.pop()
    return None
  elif nodetype == '↔': # Swap
    semdata.stack[-1], semdata.stack[-2] = semdata.stack[-2], semdata.stack[-1]
    return None
  elif nodetype == 'complex_stmt':
    if node.child_op.nodetype == '↔': # Swap
      idx1 = node.child_idx1.value
      idx2 = node.child_idx2.value
      semdata.stack[-idx1], semdata.stack[-idx2] = semdata.stack[-idx2], semdata.stack[-idx1]
    else:
      print('Error, unknown complex operation ', node.child_op)
    return None
  elif nodetype == '⊕':
    semdata.stack.append(semdata.stack.pop() + semdata.stack.pop())
    return None
  elif nodetype == '⊖':
    semdata.stack.append(semdata.stack.pop() - semdata.stack.pop())
    return None
  elif nodetype == 'ψ':
    print(semdata.stack.pop())
    return None


import sys
import tokenizer
import tree_generation
import tree_print
parser = tree_generation.parser

import semantics_check

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

        semdata = SemData()
        semdata.in_function = None
        semantics_check.semantic_checks(ast_tree, semdata)
        tree_print.treeprint(ast_tree)
        print("Semantics ok.")
        run_program(ast_tree, semdata)
        print("Program finished.")
