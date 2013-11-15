from testrepo.common.testfixtures.isl import ISLFixture
from ccengine.common.decorators import attr


class IncidentListTest(ISLFixture):

    @classmethod
    def setUpClass(cls):
        super(IncidentListTest, cls).setUpClass()
        '''Creation of 2 Tickets needed for the tests'''
        category = {"id": "CAT-001","sub-category": {"id": "SCAT-001"}}

        cls.first_ticket = cls.incident_provider.incident_client.create_incidents("Incident1", "Test Description1", "test1@test.test", category).entity
        cls.second_ticket = cls.incident_provider.incident_client.create_incidents("Incident2", "Test Description2", "test2@test.test", category).entity

    @attr(type='isl')
    def test_list_incidents(self):
        """ List of all incidents"""
        incidents = self.incident_provider.incident_client.list_incidents().entity
        incident_subjects = []
        for incident in incidents:
            incident_subjects.append(incident.subject)
        self.assertTrue("Incident1" in incident_subjects)
        self.assertTrue("Incident2" in incident_subjects)
