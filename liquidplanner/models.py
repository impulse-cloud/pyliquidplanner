import dateutil.parser
import re


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
        for key, value in data.iteritems():
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

    # This feels a little hackish and circular referencey. It works well though,
    # creating the managers on demand is efficient when retrieving long lists of
    # objects (as opposed to instantiating them as object attributes)
    @property
    def activities(self):
        from .manager import Manager
        return Manager(self.manager.config, 'activities', self.uri + '/activities', {})

    @property
    def comments(self):
        from .manager import Manager
        return Manager(self.manager.config, 'comments', self.uri + '/comments', {})

    @property
    def dependencies(self):
        from .manager import Manager
        return Manager(self.manager.config, 'dependencies', self.uri + '/dependencies', {})

    @property
    def dependents(self):
        from .manager import Manager
        return Manager(self.manager.config, 'dependents', self.uri + '/dependents', {})

    @property
    def documents(self):
        from .manager import Manager
        return Manager(self.manager.config, 'documents', self.uri + '/documents', {})
    
    @property
    def estimates(self):
        from .manager import Manager
        return Manager(self.manager.config, 'estimates', self.uri + '/estimates', {})

    @property
    def links(self):
        from .manager import Manager
        return Manager(self.manager.config, 'links', self.uri + '/links', {})

    @property
    def note(self):
        from .manager import Manager
        return Manager(self.manager.config, 'note', self.uri + '/note', {})

    @property
    def snapshots(self):
        from .manager import Manager
        return Manager(self.manager.config, 'snapshots', self.uri + '/snapshots', {})

    @property
    def tags(self):
        from .manager import Manager
        return Manager(self.manager.config, 'tags', self.uri + '/tags', {})

    @property
    def timer(self):
        from .manager import Manager
        return Manager(self.manager.config, 'timer', self.uri + '/timer', {})

