from testrepo.common.testfixtures.fixtures import BaseTestFixture


class BlockstorageBaseTestFixture(BaseTestFixture):
    @classmethod
    def setUpClass(cls):
        super(BlockstorageBaseTestFixture, cls).setUpClass()
        cls._class_teardown_tasks = []

    @classmethod
    def tearDownClass(cls):
        #TODO: Figure out a way to make this run independently of tearDownClass
        cls._do_class_teardown_tasks()
        super(BlockstorageBaseTestFixture, cls).tearDownClass()

    @classmethod
    def _do_class_teardown_tasks(cls):
        for func, args, kwargs in reversed(cls._class_teardown_tasks):
            cls.fixture_log.error(
                "Running teardown task: {0}({1}, {2})".format(
                    func.__name__,
                    ", ".join([str(arg) for arg in args]),
                    ", ".join(["{0}={1}".format(
                        str(k), str(kwargs[k])) for k in kwargs])))
            try:
                func(*args, **kwargs)
            except Exception as exception:
                #Pretty prints method signature in the following format:
                #"classTearDown failure: Unable to execute FnName(a, b, c=42)"
                cls.fixture_log.exception(exception)
                cls.fixture_log.error(
                    "classTearDown failure: Exception occured while trying to"
                    " execute class teardown task: {0}({1}, {2})".format(
                        func.__name__,
                        ", ".join([str(arg) for arg in args]),
                        ", ".join(["{0}={1}".format(
                            str(k), str(kwargs[k])) for k in kwargs])))

    @classmethod
    def addTearDownClassTask(cls, function, *args, **kwargs):
        """Named to match unittest's addCleanup"""
        cls._class_teardown_tasks.append((function, args or [], kwargs or {}))
