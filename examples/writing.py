#!/usr/bin/env python 
"""
This script shows some example write/update usage of the pyliquidplanner library.
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
    3. Run the command `python writing.py`
""")

def write_demo():
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


    # Create a new project
    project = lp.projects.create({"name": "API Test Project"})
    print("Created a new projet called {} with id {}".format(
            project["name"], project["id"]))

    # Add a task to the project
    task = lp.tasks.create({
        "parent_id": project["id"], 
        "name": "API Test Task"})
    print("Added a task to that project called {} with id {}".format(
            task["name"], task["id"]))

    # Rename the task
    task = lp.tasks.update({"name": "API Renamed Task"}, task["id"])
    print("Renamed task {} to {}".format(
            task["id"], task["name"]))

    # Reorder the project to be before the first one
    last_project = lp.projects.all()[0]
    project.move_before(last_project["id"])
    print("Moved {} before {}".format(
            project["name"], last_project["name"]))

    raw_input("Tasks created and can be seen in LiquidPlanner. Press a key to continue...")

    # Remove added project / task
    lp.tasks.delete(task["id"])
    lp.projects.delete(project["id"])
    print("Deleted project and task that were added")


if __name__ == "__main__":
    write_demo()
