#!/usr/bin/env python 
"""
This script shows some example usage of the pyliquidplanner library.

"""

from __future__ import print_function
import os

# Suppress urllib InsecurePlatform warnings for this example
import logging
logging.captureWarnings(True)


def show_usage():
    print("""
Instructions:
    1. Set environment variables LP_EMAIL and LP_PASSWORD.
    2. Ensure pyliquidplanner is installed in your environment
    3. Run the command `python reading.py`
""")

def read_demo():
    try:
        from liquidplanner import LiquidPlanner
        from liquidplanner.auth import BasicCredentials
    except ImportError:
        show_usage()
        print("Halting because liquidplanner library wasn't installed")
        return

    email = os.environ.get("LP_EMAIL", None)
    password = os.environ.get("LP_PASSWORD", None)

    if not email or not password:
        show_usage()
        print("Halting because one of LP_EMAIL or LP_PASSWORD are missing")
        return

    print("Logging in...")
    credentials = BasicCredentials(email, password)
    lp = LiquidPlanner(credentials)


    # Load up the first few open projects
    projects = lp.projects.all(
            include=["comments"], filters=['is_done is false'])

    print("")
    print("Your first five open projects:")
    for project in projects[:5]:
        print("* {} (comments: {})".format(project["name"], len(project["comments"])))
    print("")


    # Show fetching of associated. We'll show the estimates for task
    tasks = lp.tasks.all(
            limit=1, filters=['is_done is false'])

    if not tasks:
        print("You have no open tasks")
    else:
        task = tasks[0]

        print("Your first open task is {}. Estimates:".format(task["name"]))

        estimates = task.estimates.all()
        for estimate in estimates:
            print("* {}h - {}h from {}".format(estimate["low"], estimate["high"], 
                estimate["created_at"]))

        if not estimates:
            print("* There are no estimates for this task.")


if __name__ == "__main__":
    read_demo()
