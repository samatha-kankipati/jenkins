from ccengine.common.decorators import attr
from testrepo.common.testfixtures.rad import RADFixture
from time import time


class TestFlavorsCreation(RADFixture):

    """Tests for Flavor Creation Use case."""

    @attr(type='smoke')
    def test_create_flavor(self):
        """
        Verify Creation of a new flavor and it's display in the flavor list
        """
        # New flavor data
        device_id = '106542'
        ingredient_skus = [{"sku_id": 107328, "skunit_id": 11328},
                           {"sku_id": 106963, "skunit_id": 11963}]
        desc = "CentOS 6 Server, no Anti-Virus{0}".format(time()).split(".")[0]
        # Store the current state of flavors in the system
        flavors_before_test = self.rad_provider.rad_client.get_flavors().entity
        # Create a new flavor and capture the response
        create_flavor_resp = self.rad_provider.rad_client.create_flavor(
            device_id=device_id, ingredient_skus=ingredient_skus,
            desc=desc)
        created_flavor = create_flavor_resp.entity
        # Verify the request is successful
        self.assertEquals(create_flavor_resp.status_code, 200,
                          "Flavor Creation Not successful with {0}"
                          .format(create_flavor_resp.request.entity))
        # Verify the response matches the supplied flavor properties
        self.assertEquals(created_flavor.device_id, device_id,
                          "Device Id did not match")
        self.assertEquals(created_flavor.ingredient_skus, ingredient_skus,
                          "Ingredient SKUs did not match")
        # Get the new list of flavors
        flavors_after_test = self.rad_provider.rad_client.get_flavors().entity
        # Verify the difference between the new flavor list and
        # the old flavor list has the newly created flavor
        new_flavors = set(flavors_after_test).difference(set(flavors_before_test))
        self.assertTrue(len(new_flavors) >= 1,
                        "A flavor creation should add flavors to the flavor list")
        # Get the new flavor returned in the flavor list
        new_flavor_in_list = None
        while len(new_flavors) > 0:
            new_flavor_in_list = new_flavors.pop()
            # Get the Flavor whose id matches the id in the POST call's response
            if (new_flavor_in_list.id_val == created_flavor.id_val):
                break
        # Verify the flavor properties match
        self.assertTrue(new_flavor_in_list == created_flavor,
                        "Flavor returned in the GET call does not match \
                        the created flavor")
