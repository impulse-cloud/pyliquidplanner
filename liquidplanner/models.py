import dateutil.parser
import re
from six import iteritems


class Model(dict):
    """Holds a response from the liquid planner API"""
    
    # ISO 8601 date format
    DATE_REGEX = re.compile(r'^(\d{4})-(\d{2})-(\d{2})T(\d{2})\:(\d{2})\:(\d{2})[+-](\d{2})\:(\d{2})$')

    def __init__(self, manager, data, uri):
        self.manager = manager
        self.object_type = manager.singular
        self.uri = uri
        
        self._convert_dates(data)

        super(Model, self).__init__(data)

    def _convert_dates(self, data):
        """Recursively search through data for string that look like dates and convert
        them to datetime.datetime objects"""
        for key, value in iteritems(data):
            if isinstance(value, basestring) and self.DATE_REGEX.match(value):
                # This is a date! Convert it
                data[key] = dateutil.parser.parse(value)
            elif isinstance(value, dict):
                # This is a dict, recurse
                self._convert_dates(value)
            elif isinstance(value, list):
                # This is a list, recurse if any dicts present
                for inner in value:
                    if isinstance(inner, dict):
                        self._convert_dates(inner)

    def update_assignment(self, obj):
        """Update assignment attributes for a treeitem.

        Note: should only be used for tree item objects.

        :param obj: dict of values to set"""
        return self.manager._make_request('post', 
                self.uri + '/update_assignment', data=obj)

    def reorder_assignments(self, id_list):
        """Reorder assignments for a treeitem.

        Note: should only be used for tree item objects.

        :param id_list: assignment ids in their new order"""
        return self.manager._make_request('post',
                self.uri + '/reorder_assignments', 
                data={'assignment_ids': id_list})

    def delete_assignment(self, id):
        """Delete an assignment for a treeitem.

        :param id: the assignment id"""
        return self.manager._make_request('delete',
                self.uri + '/assignments/' + str(id))

    def move_before(self, other_id):
        """Move this item before another item.

        :param other_id: id of the item to move before"""
        return self.manager._make_request('post',
                self.uri + '/move_before',
                params={'other_id': other_id})

    def move_after(self, other_id):
        """Move this item after another item.

        :param other_id: id of the item to move after"""
        return self.manager._make_request('post',
                self.uri + '/move_after',
                params={'other_id': other_id})

    def package_before(self, other_id):
        """Move the package priority of this item before another item.

        :param other_id: id of the item to move before"""
        return self.manager._make_request('post',
                self.uri + '/package_before',
                params={'other_id': other_id})

    def package_after(self, other_id):
        """Move ithe package priority of this item after another item.

        :param other_id: id of the item to move after"""
        return self.manager._make_request('post',
                self.uri + '/package_after',
                params={'other_id': other_id})

    def thumbnail(self):
        """Download a thumbnail of a document."""
        return self.manager._make_request('get', self.uri + '/thumbnail')

    def download(self):
        """Download a document."""
        return self.manager._make_request('get', self.uri + '/download')

    def track_time(self, obj):
        """Convenient way to track time and update estimates
        
        :param obj: values passed to the API"""
        return self.manager._make_request('post', 
                self.uri + '/track_time', data=obj)

    def timer_commit(self, obj):
        """Stop, use, and reset a timer.
        
        :param obj: values passed to the API"""
        return self.manager._make_request('post', 
                self.uri + '/timer/commit', data=obj)

    def timer_start(self):
        """Start the timer for a task"""
        return self.manager._make_request('post', self.uri + '/timer/start')

    def timer_stop(self):
        """Stop the timer for a task"""
        return self.manager._make_request('post', self.uri + '/timer/stop')

    def timer_clear(self):
        """Start the timer for a task"""
        return self.manager._make_request('post', self.uri + '/timer/clear')

    def comment_stream(self, params):
        """Get the comment stream for a workspace.

        :param obj: parameters added to the query string"""
        return self.manager._make_request('get',
                self.uri + '/comment_stream', params=params)

    def upcoming_tasks(self, params):
        """Get the upcoming tasks for a workspace.

        :param obj: parameters added to the query string"""
        return self.manager._make_request('get',
                self.uri + '/upcoming_tasks', params=params)

    def changes(self, params):
        """Get the list of changes for a workspace.

        :param obj: parameters added to the query string"""
        return self.manager._make_request('get',
                self.uri + '/changes', params=params)

    # This feels a little hackish and circular referencey. It works well though,
    # creating the managers on demand is efficient when retrieving long lists of
    # objects (as opposed to instantiating them as object attributes)
    @property
    def activities(self):
        from .manager import Manager
        return Manager(self.manager.config, 'activities', self.uri + '/activities')

    @property
    def comments(self):
        from .manager import Manager
        return Manager(self.manager.config, 'comments', self.uri + '/comments')

    @property
    def dependencies(self):
        from .manager import Manager
        return Manager(self.manager.config, 'dependencies', self.uri + '/dependencies')

    @property
    def dependents(self):
        from .manager import Manager
        return Manager(self.manager.config, 'dependents', self.uri + '/dependents')

    @property
    def documents(self):
        from .manager import Manager
        return Manager(self.manager.config, 'documents', self.uri + '/documents')
    
    @property
    def estimates(self):
        from .manager import Manager
        return Manager(self.manager.config, 'estimates', self.uri + '/estimates')

    @property
    def links(self):
        from .manager import Manager
        return Manager(self.manager.config, 'links', self.uri + '/links')

    @property
    def note(self):
        from .manager import Manager
        return Manager(self.manager.config, 'note', self.uri + '/note')

    @property
    def snapshots(self):
        from .manager import Manager
        return Manager(self.manager.config, 'snapshots', self.uri + '/snapshots')

    @property
    def tags(self):
        from .manager import Manager
        return Manager(self.manager.config, 'tags', self.uri + '/tags')

    @property
    def timer(self):
        from .manager import Manager
        return Manager(self.manager.config, 'timer', self.uri + '/timer')

