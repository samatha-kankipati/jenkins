import json
import time
import random
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.sql import between
from sqlalchemy import update
from ccengine.common.connectors.mysql_manager import MySQLManager
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.common.constants.compute_constants \
        import Constants as ComputeConstants
from ccengine.common.tools.datatools import string_to_datetime

Base = declarative_base()
session = MySQLManager.Session()


class ExistsEventQueue(Base, BaseMarshallingDomain):
    """
    @summary: Represents the queue of exist events
    """
    __tablename__ = "existseventqueue"

    id = Column(Integer, Sequence('exists_event_id_seq'), primary_key=True)
    server_id = Column(String(100))
    tenant_id = Column(String(100))
    user_id = Column(String(100))
    flavor_id = Column(String(100))
    server_name = Column(String(100))
    image_id = Column(String(100))
    created_date = Column(String(50))
    launched_at = Column(String(50))
    deleted_at = Column(String(50))
    audit_period_beginning = Column(String(50))
    audit_period_ending = Column(String(50))
    bandwidth_usage = Column(String(500))
    server_status = Column(String(50))
    state_description = Column(String(50))
    test_name = Column(String(250))
    test_executed = Column(String(50))
    test_status = Column(String(100))
    test_type = Column(String(100))
    image_metadata = Column(String(500))
    region = Column(String(100))
    env_name = Column(String(100))

    def __init__(self, server, audit_period_ending,
                 bandwidth_usage, test_name, state_description=None,
                 image_metadata="{}", launched_at=None, deleted_at=None,
                 test_status='New', test_type='event_tests',
                 region='ORD', env_name='preprodord'):

        self.session = MySQLManager.Session()
        config = _MCP()

        # for recording build problems, wrap server attributes in try catch
        try:
            self.server_id = server.id
        except AttributeError:
            self.server_id = None

        try:
            self.user_id = server.user_id
        except AttributeError:
            self.user_id = None

        try:
            self.flavor_id = server.flavor.id
        except AttributeError:
            self.flavor_id = None

        try:
            self.server_name = server.name
        except AttributeError:
            self.server_name = None

        try:
            self.image_id = server.image.id
        except AttributeError:
            self.image_id = None

        try:
            self.created_date = server.created
        except AttributeError:
            self.created_date = None

        try:
            self.server_status = server.status
        except AttributeError:
            self.server_status = None

        self.state_description = state_description
        self.tenant_id = config.compute_api.tenant_id
        self.launched_at = launched_at
        self.deleted_at = deleted_at
        self.audit_period_beginning = \
            datetime.utcnow().strftime(ComputeConstants
                                       .DATETIME_0AM_FORMAT)
        self.audit_period_ending = audit_period_ending
        self.bandwidth_usage = bandwidth_usage
        self.test_name = test_name
        self.test_executed = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        self.test_status = test_status
        self.test_type = test_type
        self.image_metadata = json.dumps(image_metadata)
        self.region = region
        self.env_name = env_name

    def __repr__(self):
        """
        @summary: Return string representation of ExistsEventQueue
        @rtype: string
        """
        return "<ExistsEventQueue('%s','%s','%s','%s','%s','%s', \
                '%s','%s','%s','%s','%s','%s','%s','%s','%s', \
                '%s','%s','%s','%s','%s','%s')>" % \
                (self.server_id, self.tenant_id, self.user_id, self.flavor_id,
                 self.server_name, self.image_id, self.created_date,
                 self.server_status, self.state_description, self.launched_at,
                 self.deleted_at, self.audit_period_beginning,
                 self.audit_period_ending, self.bandwidth_usage,
                 self.test_name, self.test_executed,
                 self.test_status, self.image_metadata, self.test_type,
                 self.region, self.env_name)

    def add_to_queue(self):
        """
        @summary: Add a Exists Event Queue Item to Database
        """
        random.seed()
        num = 0
        sent_to_database = False
        while not sent_to_database:
            try:
                session.add(self)
                session.commit()
                sent_to_database = True
            except Exception, e:
                self.session.rollback()
                num += 1
                if num >= 10:
                    raise Exception(
                        "Failed to add and commit item to database. msg: {0}"
                        .format(e))
            time.sleep(random.randint(1, 5))

    @classmethod
    def get_validation_data(self, audit_period_beginning,
                            audit_period_ending,
                            test_type='bandwidth_tests',
                            region='ORD', env_name='preprod'):
        """
        @summary: Fetch all the exist events to be verified
        @return: List of exists events to be verified
        @rtype: ExistsEventQueue List
        """
        audit_period_beginning = audit_period_beginning.strftime(
                                    "%Y-%m-%d %H:%M:%S")
        audit_period_ending = audit_period_ending.strftime("%Y-%m-%d %H:%M:%S")
        self._update_validation_data_test_status_new(audit_period_beginning,
                                                     audit_period_ending)
        return (session.query(ExistsEventQueue)
                .filter_by(test_status='New')
                .filter_by(test_type=test_type)
                .filter_by(region=region)
                .filter_by(env_name=env_name)
                .filter(between(ExistsEventQueue.audit_period_beginning,
                                audit_period_beginning,
                                audit_period_ending))
                .order_by(ExistsEventQueue.id))

    @classmethod
    def _update_validation_data_test_status_new(self, audit_period_beginning,
                                                audit_period_ending):
        """
        @summary: Sets the test status for data to be validated to New
            based on audit_period_beginning and audit_period_ending
        @param audit_period_beginning: The starting time of audit period
        @type audit_period_beginning: string formatted date
        @param audit_period_ending: The ending time of audit period
        @type audit_period_ending: string formatted date
        """
        try:
            (session.query(ExistsEventQueue)
             .filter(ExistsEventQueue.audit_period_beginning
                     .between(audit_period_beginning,
                              audit_period_ending))
             .update({"test_status": "New"}, synchronize_session=False))
        except Exception, e:
            raise Exception("The exists event test status failed to be "
                            "updated into the DB: {0}".format(e))


metadata = Base.metadata
metadata.create_all(MySQLManager.engine)
