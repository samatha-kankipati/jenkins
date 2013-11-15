from ccengine.common.tools.dotteddict import DottedDict
import dateutil
from datetime import datetime, timedelta
from ccengine.domain.types import LoadBalancerSslModes as LBSModes, \
    LoadBalancerAtomHopperEvents as LBAHE, \
    LoadBalancerAtomHopperStatusTypes as LBAHST
from ccengine.domain.types import LoadBalancerVirtualIpTypes as VipTypes


BANDWIDTH_ACCEPTANCE_RATIO = 0.33
BANDWIDTH_ZERO_ACCEPTANCE = 100000
ACC_ACCEPTANCE_RANGE = 1


def verify_record_properties(record, numVips=1, bandWidthIn=0,
                             bandWidthOut=0, bandWidthInSsl=0,
                             bandWidthOutSsl=0, vipType=VipTypes.PUBLIC,
                             avgConcurrentConnections=0,
                             avgConcurrentConnectionsSsl=0,
                             sslMode=LBSModes.OFF,
                             status=LBAHST.ACTIVE):

    assert int(record.numVips) == numVips, (
        'Expected: {0}, Actual: '
        '{1}'.format(numVips, record.numVips))

    verify_bandwidth(record, bandWidthIn=bandWidthIn,
                     bandWidthOut=bandWidthOut, bandWidthInSsl=bandWidthInSsl,
                     bandWidthOutSsl=bandWidthOutSsl, sslMode=sslMode)

    assert record.vipType == vipType, (
        'Expected: {0}, '
        'Actual: {1}'.format(vipType, record.vipType))

    assert avgConcurrentConnections <= float(
        record.avgConcurrentConnections) * int(record.numPolls) <= \
        avgConcurrentConnections + ACC_ACCEPTANCE_RANGE, \
        ('Expected: {0}, Actual: {1}'.format(avgConcurrentConnections,
                                             record.avgConcurrentConnections))

    assert avgConcurrentConnectionsSsl <= float(
        record.avgConcurrentConnectionsSsl) * int(record.numPolls) <= \
        avgConcurrentConnectionsSsl + ACC_ACCEPTANCE_RANGE, (
            'Expected: {0}, Actual: {1}'.format(
            avgConcurrentConnectionsSsl,
            record.avgConcurrentConnectionsSsl))

    assert record.sslMode == sslMode, (
        'Expected: {0}, '
        'Actual: {1}'.format(sslMode, record.sslMode))

    assert record.status == status, (
        'Expected: {0}, '
        'Actual: {1}'.format(status, record.status))


def verify_bandwidth(record, bandWidthIn=0, bandWidthOut=0, bandWidthInSsl=0,
                     bandWidthOutSsl=0, sslMode=LBSModes.OFF):
    if bandWidthIn == 0:
        if sslMode == LBSModes.ON:
            assert int(record.bandWidthIn) == 0, ('Expected: 0, Actual '
                                                  '{0}. Should not have '
                                                  'any bandwidthIn '
                                                  'while ssl only on.'.format(
                                                  record.bandWidthIn))
        else:
            assert bandWidthIn <= int(
                record.bandWidthIn) <= BANDWIDTH_ZERO_ACCEPTANCE, (
                    'Expected: [{0} - {1}], '
                    'Actual: {2}'.format(bandWidthIn,
                                         BANDWIDTH_ZERO_ACCEPTANCE,
                                         record.bandWidthIn))
    elif bandWidthIn > 0:
        assert bandWidthIn <= int(record.bandWidthIn) <= bandWidthIn + (
            bandWidthIn * BANDWIDTH_ACCEPTANCE_RATIO), (
                'Expected: {0}, '
                'Actual: {1}'.format(bandWidthIn, record.bandWidthIn))

    if bandWidthOut == 0:
        if sslMode == LBSModes.ON:
            assert int(record.bandWidthOut) == 0, ('Expected: 0, Actual '
                                                   '{0}. Should not have '
                                                   'any bandwidthOut '
                                                   'while ssl only on.'.format(
                                                   record.bandWidthOut))
        else:
            assert bandWidthOut <= int(
                record.bandWidthOut) <= BANDWIDTH_ZERO_ACCEPTANCE, (
                    'Expected: [{0} - {1}], '
                    'Actual: {2}'.format(bandWidthOut,
                                         BANDWIDTH_ZERO_ACCEPTANCE,
                                         record.bandWidthOut))
    elif bandWidthOut > 0:
        assert bandWidthOut <= int(record.bandWidthOut) <= bandWidthOut + (
            bandWidthOut * BANDWIDTH_ACCEPTANCE_RATIO), (
                'Expected: {0}, '
                'Actual: {1}'.format(bandWidthOut, record.bandWidthOut))

    if bandWidthInSsl == 0:
        if sslMode == LBSModes.OFF:
            assert int(record.bandWidthInSsl) == 0, ('Expected: 0, Actual '
                                                     '{0}. Should not have '
                                                     'any bandwidthInSsl '
                                                     'while ssl off.'.format(
                                                     record.bandWidthInSsl))
        else:
            assert bandWidthInSsl <= int(
                record.bandWidthInSsl) <= BANDWIDTH_ZERO_ACCEPTANCE, (
                    'Expected: [{0} - {1}], '
                    'Actual: {2}'.format(bandWidthInSsl,
                                         BANDWIDTH_ZERO_ACCEPTANCE,
                                         record.bandWidthInSsl))
    elif bandWidthInSsl > 0:
        assert bandWidthInSsl <= int(
            record.bandWidthInSsl) <= bandWidthInSsl + (
                bandWidthInSsl * BANDWIDTH_ACCEPTANCE_RATIO), (
                    'Expected: {0},'
                    ' Actual: {1}'.format(bandWidthInSsl,
                                          record.bandWidthInSsl))

    if bandWidthOutSsl == 0:
        if sslMode == LBSModes.OFF:
            assert int(record.bandWidthOutSsl) == 0, ('Expected: 0, Actual '
                                                      '{0}. Should not have '
                                                      'any bandwidthOutSsl '
                                                      'while ssl off.'.format(
                                                      record.bandWidthOutSsl))
        else:
            assert bandWidthOutSsl <= int(
                record.bandWidthOutSsl) <= BANDWIDTH_ZERO_ACCEPTANCE, (
                    'Expected: [{0} - {1}], '
                    'Actual: {2}'.format(bandWidthOutSsl,
                                         BANDWIDTH_ZERO_ACCEPTANCE,
                                         record.bandWidthOutSsl))
    elif bandWidthOutSsl > 0:
        assert bandWidthOutSsl <= int(
            record.bandWidthOutSsl) <= bandWidthOutSsl + (
                bandWidthOutSsl * BANDWIDTH_ACCEPTANCE_RATIO), (
                    'Expected: {0},'
                    ' Actual: {1}'.format(bandWidthOutSsl,
                                          record.bandWidthOutSsl))


def verify_records(records, mode_order=None, status_order=None,
                   num_vips_order=None,
                   bandwidth_out_order=None, bandwidth_in_order=None,
                   bandwidth_out_ssl_order=None, bandwidth_in_ssl_order=None,
                   vip_type_order=None, acc_order=None, acc_ssl_order=None):
    default_list_size = len(records)
    if mode_order is None:
        mode_order = populate_list(LBSModes.OFF, default_list_size)
    else:
        mode_order.extend([mode_order[len(mode_order) - 1]
                           for _ in range(len(mode_order), len(records))])
    if status_order is None:
        status_order = populate_list(LBAHST.ACTIVE, default_list_size)
    else:
        status_order.extend([status_order[len(status_order) - 1]
                             for _ in range(len(status_order), len(records))])
    if num_vips_order is None:
        num_vips_order = populate_list(1, default_list_size)
    else:
        num_vips_order.extend([num_vips_order[len(num_vips_order) - 1]
                               for _ in range(len(num_vips_order),
                                              len(records))])
    if bandwidth_out_order is None:
        bandwidth_out_order = populate_list(0, default_list_size)
    else:
        bandwidth_out_order.extend([0 for _ in range(len(bandwidth_out_order),
                                                     len(records))])
    if bandwidth_in_order is None:
        bandwidth_in_order = populate_list(0, default_list_size)
    else:
        bandwidth_in_order.extend([0 for _ in range(len(bandwidth_in_order),
                                                    len(records))])
    if bandwidth_out_ssl_order is None:
        bandwidth_out_ssl_order = populate_list(0, default_list_size)
    else:
        bandwidth_out_ssl_order.extend([0 for _ in
                                        range(len(bandwidth_out_ssl_order),
                                              len(records))])
    if bandwidth_in_ssl_order is None:
        bandwidth_in_ssl_order = populate_list(0, default_list_size)
    else:
        bandwidth_in_ssl_order.extend([0 for _ in
                                       range(len(bandwidth_in_ssl_order),
                                             len(records))])
    if vip_type_order is None:
        vip_type_order = populate_list(VipTypes.PUBLIC, default_list_size)
    else:
        vip_type_order.extend([vip_type_order[len(vip_type_order) - 1]
                               for _ in range(len(vip_type_order),
                                              len(records))])
    if acc_order is None:
        acc_order = populate_list(0, default_list_size)
    else:
        acc_order.extend([0 for _ in range(len(acc_order), len(records))])
    if acc_ssl_order is None:
        acc_ssl_order = populate_list(0, default_list_size)
    else:
        acc_ssl_order.extend([0 for _ in range(len(acc_ssl_order),
                                               len(records))])

    use_next_record = True
    expected_index = 0
    for index, rec in enumerate(records):
        if not use_next_record:
            use_next_record = True
            continue
        if len(records) >= index + 2:
            next_is_event = is_next_record_an_event(rec, records[index + 1])
            if not next_is_event:
                rec.product.bandWidthIn = \
                    float(rec.product.bandWidthIn) + \
                    float(records[index + 1].product.bandWidthIn)
                rec.product.bandWidthOut = \
                    float(rec.product.bandWidthOut) + \
                    float(records[index + 1].product.bandWidthOut)
                rec.product.bandWidthInSsl = \
                    float(rec.product.bandWidthInSsl) + \
                    float(records[index + 1].product.bandWidthInSsl)
                rec.product.bandWidthOutSsl = \
                    float(rec.product.bandWidthOutSsl) + \
                    float(records[index + 1].product.bandWidthOutSsl)
                use_next_record = False
            elif is_record_end_of_hour(rec):
                rec.product.bandWidthIn = \
                    float(rec.product.bandWidthIn) + \
                    float(records[index + 1].product.bandWidthIn)
                rec.product.bandWidthOut = \
                    float(rec.product.bandWidthOut) + \
                    float(records[index + 1].product.bandWidthOut)
                rec.product.bandWidthInSsl = \
                    float(rec.product.bandWidthInSsl) + \
                    float(records[index + 1].product.bandWidthInSsl)
                rec.product.bandWidthOutSsl = \
                    float(rec.product.bandWidthOutSsl) + \
                    float(records[index + 1].product.bandWidthOutSsl)
                verify_record_properties(
                    records[index + 1].product,
                    numVips=num_vips_order[expected_index],
                    vipType=vip_type_order[expected_index],
                    sslMode=mode_order[expected_index],
                    status=status_order[expected_index])
                use_next_record = False

        verify_record_properties(rec.product, num_vips_order[expected_index],
                                 bandwidth_in_order[expected_index],
                                 bandwidth_out_order[expected_index],
                                 bandwidth_in_ssl_order[expected_index],
                                 bandwidth_out_ssl_order[expected_index],
                                 vip_type_order[expected_index],
                                 acc_order[expected_index],
                                 acc_ssl_order[expected_index],
                                 mode_order[expected_index],
                                 status_order[expected_index])
        expected_index += 1


def populate_list(item, size):
    return [item for _ in range(size)]


def is_next_record_an_event(current_record, next_record):
    return current_record.product.sslMode != next_record.product.sslMode or \
        current_record.product.status != next_record.product.status or \
        current_record.product.numVips != next_record.product.numVips


def is_record_end_of_hour(record):
    end_time = dateutil.parser.parse(record.endTime)
    return end_time.minute == 0 and end_time.second == 0


def are_records_contiguous(records):
    ret = DottedDict()
    ret.result = True
    ret.time1 = None
    ret.time2 = None
    last_st = None
    for r in records:
        st = None
        et = None
        if r.startTime is not None:
            st = dateutil.parser.parse(r.startTime)
            et = dateutil.parser.parse(r.endTime)
        if r.eventTime is not None:
            st = dateutil.parser.parse(r.eventTime)
            et = dateutil.parser.parse(r.eventTime)
        if last_st is not None:
            if last_st != et:
                ret.result = False
                ret.time1 = last_st
                ret.time2 = et
                break
        last_st = st
    return ret


def recent_record_has_correct_time(records):
    time = records[0].eventTime or records[0].startTime
    time = dateutil.parser.parse(time)
    now = datetime.utcnow() - timedelta(hours=1)
    if time.minute <= 15:
        return time.hour == now.hour or time.hour == now.hour - 1
    return time.hour == now.hour
