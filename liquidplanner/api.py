from .manager import Manager

class LiquidPlanner(object):
    """An ORM-like interface to the LiquidPlanner API"""

    # (name, url, options)
    MANAGERS = (
            # The special two that don't require a workspace id
            ('account', '/account', {}),
            ('workspaces', '/workspaces', {}),

            # The rest in the same order as listed at
            # https://app.liquidplanner.com/api/help/types
            ('activities', '/workspaces/{workspace_id}/activities', {}),
            ('members', '/workspaces/{workspace_id}/members', {}),
            ('checklist_items', '/workspaces/{workspace_id}/checklist_items', {}), 
            ('clients', '/workspaces/{workspace_id}/clients', {}),
            ('comments', '/workspaces/{workspace_id}/comments', {}), 
            ('custom_fields', '/workspaces/{workspace_id}/custom_fields', {}), 
            ('documents', '/workspaces/{workspace_id}/documents', {}), 
            ('events', '/workspaces/{workspace_id}/events', {}), 
            ('folders', '/workspaces/{workspace_id}/folders', {}), 
            ('links', '/workspaces/{workspace_id}/links', {}), 
            ('milestones', '/workspaces/{workspace_id}/milestones', {}), 
            ('packages', '/workspaces/{workspace_id}/packages', {}), 
            ('partial_day_events', '/workspaces/{workspace_id}/partial_day_events', {}), 
            ('projects', '/workspaces/{workspace_id}/projects', {}),
            ('tags', '/workspaces/{workspace_id}/tags', {}),
            ('tasks', '/workspaces/{workspace_id}/tasks', {}),
            ('teams', '/workspaces/{workspace_id}/teams', {}),
            ('timesheet_entries', '/workspaces/{workspace_id}/timesheet_entries', {}),
            ('timesheets', '/workspaces/{workspace_id}/timesheets', {}),
            ('webhooks', '/workspaces/{workspace_id}/webhooks', {}),
            ('treeitems', '/workspaces/{workspace_id}/treeitems', {}),
    )

    # Valid options for the include parameter. Not enforced, but here as
    # a reference (and can be passed if you want to include everything)
    ASSOCIATED_RECORDS = [
            'activities', 'comments', 'dependencies', 'dependents',
            'documents', 'estimates', 'links', 'note', 'snapshots',
            'tags', 'timer'
    ]

    def __init__(self, credentials, use_first_workspace=True):
        self.workspace_id = None
        self.credentials = credentials

        for manager in self.MANAGERS:
            setattr(self, manager[0], Manager(self, *manager))

        if use_first_workspace:
            self.workspace_id = self.workspaces.all()[0]['id']

