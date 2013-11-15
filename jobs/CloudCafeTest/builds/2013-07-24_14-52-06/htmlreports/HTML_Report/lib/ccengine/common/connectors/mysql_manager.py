from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ccengine.common.connectors.base_connector import BaseConnector
from ccengine.providers.configuration import MasterConfigProvider as _MCP


class MySQLManager(BaseConnector):
    """
    @summary: Mysql database connection manager
    """

    config = _MCP()
    engine = create_engine('mysql://%s?charset=utf8&use_unicode=0' %
                           config.compute_api.mysql_conn_string, pool_size=30,
                           pool_recycle=300, max_overflow=30, echo=True,
                           echo_pool='debug')
    Session = scoped_session(sessionmaker(bind=engine, autoflush=True))
