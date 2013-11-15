from ccengine.common.decorators import attr
import testrepo.lbaas.functional.test_session_persistence as LBSessPers


def setup_nodeless_fixture(cls):
    cls.orig_lb = cls.lb
    cls.lb = cls.lbaas_provider.create_active_load_balancer(
        nodeless=True).entity
    cls.lbs_to_delete.append(cls.lb.id)


class NodelessSessionPersistenceSmokeTests(
        LBSessPers.SessionPersistenceSmokeTests):
    @classmethod
    def setUpClass(cls):
        super(NodelessSessionPersistenceSmokeTests, cls).setUpClass()
        setup_nodeless_fixture(cls)

    @attr('nodeless')
    def test_nodeless_functional_persistence(self):
        """ Testing session persistence CRUD operations on nodeless LB"""
        return self.test_functional_session_persistence()

    @attr('nodeless')
    def test_update_nodeless_lb_after_cookie_session_persistence(self):
        """ Testing cookie based session persistence nodeless load balancer """
        return self.test_update_lb_after_cookie_session_persistence()


class NodelessSessionPersistenceTests(LBSessPers.SessionPersistenceTests):
    @classmethod
    def setUpClass(cls):
        super(NodelessSessionPersistenceTests, cls).setUpClass()
        setup_nodeless_fixture(cls)

    @attr('nodeless')
    def test_nodeless_non_http_load_balancer_ip_session_persistence(self):
        """
        Verify IP based session persistence on a nodeless non-HTTP load
        balancer

        """
        return self.test_non_http_load_balancer_ip_session_persistence()

    @attr('nodeless')
    def test_nodeless_delete_session_persistence_status(self):
        """
        Verify after session persistence is deleted, nodeless LB is
        PENDING_UPDATE

        """
        return self.test_delete_session_persistence_status()


