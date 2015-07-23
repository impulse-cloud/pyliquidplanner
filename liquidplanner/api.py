from .manager import Manager

class LiquidPlanner(object):
    """An ORM-like interface to the LiquidPlanner API"""

    MANAGERS = (
            ('account', '/account'),
            ('workspaces', '/workspaces'),
            ('projects', '/workspaces/{workspace_id}/projects'),
            ('tasks', '/workspaces/{workspace_id}/tasks'),
            ('clients', '/workspaces/{workspace_id}/clients'),
    )

    def __init__(self, credentials, use_first_workspace=True):
        self.workspace_id = None
        self.credentials = credentials

        for manager in self.MANAGERS:
            setattr(self, manager[0], Manager(self, manager[0], manager[1]))

        if use_first_workspace:
            self.workspace_id = self.workspaces.all()[0]['id']

