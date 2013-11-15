from ccengine.common.loaders.base_parameterized_loader \
    import BaseParameterizedLoader
from testrepo.designate.smoke.records \
    import RecordsTest
from unittest2.suite import TestSuite


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    custom_loader = BaseParameterizedLoader()
    custom_loader.addTest(RecordsTest(
        "test_records_type_A"))
    custom_loader.addTest(RecordsTest(
        "test_records_type_AAAA"))
    suite.addTest(custom_loader.getSuite())
    custom_loader.addTest(RecordsTest(
        "test_records_type_PTR"))
    custom_loader.addTest(RecordsTest(
        "test_records_type_SPF"))
    custom_loader.addTest(RecordsTest(
        "test_records_type_CNAME"))
    custom_loader.addTest(RecordsTest(
        "test_records_type_TXT"))
    custom_loader.addTest(RecordsTest(
        "test_records_type_SRV"))
    custom_loader.addTest(RecordsTest(
        "test_records_type_MX"))
    custom_loader.addTest(RecordsTest(
        "test_records_type_NS"))
    custom_loader.addTest(RecordsTest(
        "test_records_type_SSHFP"))
    return suite
