from pandasai.helpers.save_chart import compare_ast

import ast
import logging
import os
from itertools import zip_longest
from os.path import dirname
from typing import Union

import astor


def add_save_chart(code: str, folder_name: str, print_save_dir: bool = True) -> str:
    """
    Add line to code that save charts to a file, if plt.show() is called.

    Args:
        code (str): Code to add line to.
        folder_name (str): Name of folder to save charts to.
        print_save_dir (bool): Print the save directory to the console.
            Defaults to True.

    Returns:
        str: Code with line added.

    """

    # define chart save directory
    project_root = dirname(__file__)
    chart_save_dir = os.path.join(project_root, "exports", "charts", folder_name)

    tree = ast.parse(code)

    # count number of plt.show() calls
    show_count = sum(
        compare_ast(node, ast.parse("plt.show()").body[0], ignore_args=True)
        for node in ast.walk(tree)
    )

    # if there are no plt.show() calls, return the original code
    if show_count == 0:
        return code

    if not os.path.exists(chart_save_dir):
        os.makedirs(chart_save_dir)

    # iterate through the AST and add plt.savefig() calls before plt.show() calls
    counter = ord("a")
    new_body = []
    for node in tree.body:
        if compare_ast(node, ast.parse("plt.show()").body[0], ignore_args=True):
            filename = "chart"
            if show_count > 1:
                filename += f"_{chr(counter)}"
                counter += 1

            chart_save_path = os.path.join(chart_save_dir, f"{filename}.png")
            new_body.append(ast.parse(f"plt.savefig(r'{chart_save_path}')"))
        new_body.append(node)

    chart_save_msg = f"Charts saving to: {chart_save_dir}"
    if print_save_dir:
        print(chart_save_msg)
    logging.info(chart_save_msg)

    new_tree = ast.Module(body=new_body)
    return astor.to_source(new_tree).strip()