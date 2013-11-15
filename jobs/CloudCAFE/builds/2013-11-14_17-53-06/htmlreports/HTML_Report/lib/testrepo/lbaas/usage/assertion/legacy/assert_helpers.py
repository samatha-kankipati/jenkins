import dateutil
from datetime import datetime, timedelta
from ccengine.common.tools.dotteddict import DottedDict
from ccengine.domain.types import LoadBalancerUsageEventTypes as LBUETypes, \
    LoadBalancerSslModes as LBSModes, LoadBalancerVirtualIpTypes as VipTypes

BANDWIDTH_ACCEPTANCE_RATIO = 0.01
BANDWIDTH_ZERO_ACCEPTANCE = 100000
ACC_ACCEPTANCE_RANGE = 1


def are_records_contiguous(records):
    ret = DottedDict()
    ret.result = True
    ret.time1 = None
    ret.time2 = None
    last_st = None
    for r in records:
        st = dateutil.parser.parse(r.startTime)
        et = dateutil.parser.parse(r.endTime)
        if last_st is not None:
            if last_st != et:
                ret.result = False
                ret.time1 = last_st
                ret.time2 = et
                break
        last_st = st
    return ret


def recent_record_has_correct_time(records):
    time = records[len(records) - 1].startTime
    time = dateutil.parser.parse(time)
    now = datetime.utcnow() - timedelta(hours=2)
    return now.hour == time.hour


def get_date_from_days(days):
    delta = timedelta(days=days)
    new_date = datetime.utcnow().date() + delta
    return new_date.isoformat()


def verify_record_properties(record, numVips=1, incomingTransfer=0,
                             outgoingTransfer=0, incomingTransferSsl=0,
                             outgoingTransferSsl=0, vipType=VipTypes.PUBLIC,
                             averageNumConnections=0,
                             averageNumConnectionsSsl=0, sslMode=LBSModes.OFF):
    assert record.numVips == numVips, ('Expected: {0}, Actual: {1}'.format(
        numVips, record.numVips))

    verify_record_bandwidth(record, incomingTransfer=incomingTransfer,
                            outgoingTransfer=outgoingTransfer,
                            incomingTransferSsl=incomingTransferSsl,
                            outgoingTransferSsl=outgoingTransferSsl,
                            sslMode=sslMode)

    assert record.vipType == vipType, ('Expected: {0}, '
        'Actual: {1}'.format(vipType, record.vipType))
    assert record.averageNumConnections == averageNumConnections, ('Expected: '
        '{0}, Actual: {1}'.format(averageNumConnections,
                                  record.averageNumConnections))
    assert record.averageNumConnectionsSsl == averageNumConnectionsSsl, (''
        'Expected: {0}, Actual: {1}'.format(averageNumConnectionsSsl,
                                            record.averageNumConnectionsSsl))
    assert record.sslMode == sslMode, ('Expected: {0}, '
        'Actual: {1}'.format(sslMode, record.sslMode))


def verify_record_bandwidth(record, incomingTransfer=0, outgoingTransfer=0,
                            incomingTransferSsl=0, outgoingTransferSsl=0,
                            sslMode=LBSModes.OFF):
    if incomingTransfer == 0:
        if sslMode == LBSModes.ON:
            assert int(record.incomingTransfer) == 0, (
                'Expected: 0, Actual {0}. Should not have any '
                'incomingTransfer while ssl only on.'.format(
                    record.incomingTransfer))
        else:
            assert incomingTransfer <= int(
                record.incomingTransfer) <= BANDWIDTH_ZERO_ACCEPTANCE, (
                    'Expected: [{0} - {1}], '
                    'Actual: {2}'.format(incomingTransfer,
                                         BANDWIDTH_ZERO_ACCEPTANCE,
                                         record.incomingTransfer))
    elif incomingTransfer > 0:
        assert incomingTransfer <= int(record.incomingTransfer) <= (
            incomingTransfer + (incomingTransfer *
                                BANDWIDTH_ACCEPTANCE_RATIO)), (
            'Expected: {0}, Actual: {1}'.format(incomingTransfer,
                                                record.incomingTransfer))

    if outgoingTransfer == 0:
        if sslMode == LBSModes.ON:
            assert int(record.outgoingTransfer) == 0, (
                'Expected: 0, Actual {0}. Should not have any outgoingTransfer'
                ' while ssl only on.'.format(record.outgoingTransfer))
        else:
            assert outgoingTransfer <= int(
                record.outgoingTransfer) <= BANDWIDTH_ZERO_ACCEPTANCE, (
                    'Expected: [{0} - {1}], '
                    'Actual: {2}'.format(outgoingTransfer,
                                         BANDWIDTH_ZERO_ACCEPTANCE,
                                         record.outgoingTransfer))
    elif outgoingTransfer > 0:
        assert outgoingTransfer <= int(record.outgoingTransfer) <= \
            outgoingTransfer + (outgoingTransfer *
                                BANDWIDTH_ACCEPTANCE_RATIO), (
            'Expected: {0}, Actual: {1}'.format(outgoingTransfer,
                                                record.outgoingTransfer))

    if incomingTransferSsl == 0:
        if sslMode == LBSModes.OFF:
            assert int(record.incomingTransferSsl) == 0, (
                'Expected: 0, Actual {0}. Should not have any '
                'incomingTransferSsl while ssl off.'.format(
                    record.incomingTransferSsl))
        else:
            assert incomingTransferSsl <= int(
                record.incomingTransferSsl) <= BANDWIDTH_ZERO_ACCEPTANCE, (
                    'Expected: [{0} - {1}], '
                    'Actual: {2}'.format(incomingTransferSsl,
                                         BANDWIDTH_ZERO_ACCEPTANCE,
                                         record.incomingTransferSsl))
    elif incomingTransferSsl > 0:
        assert incomingTransferSsl <= int(
            record.incomingTransferSsl) <= incomingTransferSsl + (
                incomingTransferSsl * BANDWIDTH_ACCEPTANCE_RATIO), (
                    'Expected: {0},'
                    ' Actual: {1}'.format(incomingTransferSsl,
                                          record.incomingTransferSsl))

    if outgoingTransferSsl == 0:
        if sslMode == LBSModes.OFF:
            assert int(record.outgoingTransferSsl) == 0, (
                'Expected: 0, Actual {0}. Should not have any '
                'outgoingTransferSsl while ssl off.'.format(
                    record.outgoingTransferSsl))
        else:
            assert outgoingTransferSsl <= int(
                record.outgoingTransferSsl) <= BANDWIDTH_ZERO_ACCEPTANCE, (
                    'Expected: [{0} - {1}], '
                    'Actual: {2}'.format(outgoingTransferSsl,
                                         BANDWIDTH_ZERO_ACCEPTANCE,
                                         record.outgoingTransferSsl))
    elif outgoingTransferSsl > 0:
        assert outgoingTransferSsl <= int(
            record.outgoingTransferSsl) <= outgoingTransferSsl + (
                outgoingTransferSsl * BANDWIDTH_ACCEPTANCE_RATIO), (
                    'Expected: {0},'
                    ' Actual: {1}'.format(outgoingTransferSsl,
                                          record.outgoingTransferSsl))


def verify_records_times(records, event_order, num_vips=None):
    temp_event_order = event_order[:]
    last_end = None
    i = 0
    for i in range(len(records)):
        start = dateutil.parser.parse(records[i].startTime)
        end = dateutil.parser.parse(records[i].endTime)
        if last_end is not None:
            assert start == last_end, ("Record's start time did not "
                "match last record's end time - Record startTime - "
                "{0}, Last record endTime - {0}".format(records[i].startTime,
                                                        records[i].endTime))
        last_end = end
        if records[i].eventType is not None:
            if records[i].eventType == LBUETypes.DELETE_LOADBALANCER and \
               len(temp_event_order) == 0:
                #May want to do somethign with this later. As of now this will
                #give a lot of false negatives because load balancers to get
                #deleted through clean up jobs.
                pass
            else:
                event = temp_event_order.pop(0)
                assert records[i].eventType == event, ('Event did not occur '
                    'in correct order. Expected event - {0}, Actual event - '
                    '{1}'.format(event, records[i].eventType))
        if records[i].eventType == LBUETypes.SUSPENDED_LOADBALANCER:
            if start.minute != 0 or start.second != 0:
                assert i != 0, '1st record not CREATE_LOADBALANCER event'
                last_event = records[i - 1].eventType
                assert last_event == LBUETypes.SUSPEND_LOADBALANCER, (''
                    'Record with event type SUSPENDED_LOADBALANCER and '
                    'startTime is not on the hour should be preceded with a '
                    'record with event of SUSPEND_LOADBALANCER.')
            if end.minute != 0 or end.second != 0:
                assert i != (len(records) + 1), ('If last record is '
                    'SUSPENDED_LOADBALANCER event it should end on the hour '
                    'unless it is followed by a UNSUSPEND_LOADBALANCER event')
                next_event = records[i + 1].eventType
                assert next_event == LBUETypes.UNSUSPEND_LOADBALANCER or \
                       next_event == LBUETypes.DELETE_LOADBALANCER, (''
                    'Record does not have an end time on the hour should '
                    'be followed by a record with an event of '
                    'UNSUSPEND_LOADBALANCER or DELETE_LOADBALANCER')
            if start.minute == 0 and start.second == 0 and \
               end.minute == 0 and end.second == 0:
                if start.hour == 23:
                    assert end.hour == 0, ('End time did not occur '
                           'exactly one hour after start time. startTime - '
                           '{0}, endTime - {0}'.format(start, end))
                else:
                    assert start.hour == (end.hour - 1), ('End time did not '
                           'occur exactly one hour after start time. '
                           'startTime - {0}, endTime - {0}'.format(start, end))
        if records[i].eventType is None:
            if start.minute != 0 or start.second != 0:
                assert i != 0, '1st record not CREATE_LOADBALANCER event'
                assert records[i - 1].eventType is not None, ('Record that '
                    'does not have start time on the hour should be preceded '
                    'with a record with an event. startTime - {0}, last '
                    'records event - {1}'.format(records[i].startTime,
                                                 records[i - 1].eventType))
            if end.minute != 0 or end.second != 0:
                assert i != (len(records) - 1), ('If last record is not an '
                    'event it should end on the hour. endTime - {0}, event - '
                    '{1}'.format(records[i].startTime, records[i].evenetType))
                assert records[i + 1].eventType is not None, ('Record that '
                    'does not have an end time on the hour should be followed '
                    'by a record with an event. endTime - {0}, next event - '
                    '{1}'.format(records[i].startTime,
                                 records[i + 1].eventType))
            if start.minute == 0 and start.second == 0 and \
               end.minute == 0 and end.second == 0:
                if start.hour == 23:
                    assert end.hour == 0, ('End time did not occur '
                           'exactly one hour after start time. startTime - '
                           '{0}, endTime - {0}'.format(start, end))
                else:
                    assert start.hour == (end.hour - 1), ('End time did not '
                           'occur exactly one hour after start time. '
                           'startTime - {0}, endTime - {0}'.format(start, end))
    assert len(temp_event_order) == 0, ('Events that should have been in records '
           'were not: {0}'.format(temp_event_order))
