from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersSmokeFixture, LoadBalancersZeusFixture
from ccengine.common.decorators import attr
from ccengine.common.constants.lbaas import SSLConstants
from ccengine.domain.types import LoadBalancerVirtualIpTypes as LBVipTypes
import requests
import time
try:
    import M2Crypto
except:
    pass


class SSLTerminationSmokeTests(LoadBalancersSmokeFixture):

    @attr('smoke, positive')
    def test_ssl_term_crud(self):
        '''Test CRUD operations of SSL Termination calls.'''
        ssl_enabled = True
        ssl_securePort = 443
        ssl_secureTrafficOnly = False
        ssl_privatekey = SSLConstants.privatekey
        ssl_certificate = SSLConstants.certificate
        r = self.client.update_ssl_termination(self.lb.id,
                                               securePort=ssl_securePort,
                                               privatekey=ssl_privatekey,
                                               certificate=ssl_certificate,
                                               enabled=ssl_enabled,
                                               secureTrafficOnly=
                                               ssl_secureTrafficOnly)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_ssl_termination(self.lb.id)
        self.assertEquals(r.status_code, 200)
        ssl_term = r.entity
        self.assertEquals(ssl_term.enabled, ssl_enabled)
        self.assertEquals(ssl_term.securePort, ssl_securePort)
        self.assertEquals(ssl_term.secureTrafficOnly, ssl_secureTrafficOnly)
        self.assertEquals(ssl_term.privatekey, ssl_privatekey)
        self.assertEquals(ssl_term.certificate, ssl_certificate)
        r = self.client.delete_ssl_termination(self.lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_ssl_termination(self.lb.id)
        self.assertEquals(r.status_code, 404)
        self.assertIsNone(r.entity)


class SSLTerminationTests(LoadBalancersZeusFixture):

    @classmethod
    def setUpClass(cls):
        '''Setting up class. Create load balancer...'''
        super(SSLTerminationTests, cls).setUpClass()
        r = cls.lbaas_provider.create_active_load_balancer(protocol='HTTP',
                                                           port=80)
        assert r.status_code == 200, 'Received %s' % str(r.status_code)
        cls.ssl_lb = r.entity
        cls.lbs_to_delete.append(cls.ssl_lb.id)
        cls.zeus_vs_name = '_'.join([str(cls.tenant_id), str(cls.ssl_lb.id),
                                     'S'])

    @classmethod
    def tearDown(cls):
        cls.lbaas_provider.wait_for_status(cls.ssl_lb.id)
        cls.client.delete_ssl_termination(cls.ssl_lb.id)
        cls.lbaas_provider.wait_for_status(cls.ssl_lb.id)

    @attr('positive')
    def test_ssl_termination_cert_validation(self):
        '''SSL Cert validation - rsaEncryption PEM format'''
        new_format = '''-----BEGIN RSA PRIVATE KEY-----
            MIICXAIBAAKBgQC4BgF7Q524gqtiolTLzUpdabWcFCASDkc8diX9qbKb92vKsmW8
            36GmQWE9EvAXtCu4PfB7YCCiNP+M8iRGGAgHVUlyFzOpSIO2/WSlJVkeNtf7Bpq0
            G9IeQ2OuvPPT1Ar/BOKKbeB2Z2DVJCdINbWb+XO/JzYqdcWxsrmWn3mukwIDAQAB
            AoGAIX7uXBp1pfUa7wwvNR178L7iELPVFpREwSucRKzT1vHVTALm49cs3E9APNaq
            nxXrc1DK6hoYNo5BCc21bpDHPQcs76p/jvpSZdFtfkWxqkJa4A80R7quJr8hxV4d
            ruD+CUhuOsWc8CclhSlBADjAkXupcfRd5OVA6eJ2BOt9w7kCQQDsDhsO716Jn4rU
            qf0iYhGFUmMiwzhrcJ8zxEG7AdXR9nzDE5fOKoO9XmKlh7d7TxeKx9C//JCRTgCF
            zZhaaiIVAkEAx5JzZLwCQVylzMPZBd0P6XzJI8PDN4/XaDMl2P94KsrJaM/uOlal
            0BvOhXG3RrDkyL33VbH3ZE+JccTBcLfABwJAZPpnwszM8SxplC2flozDF/g1ZlKC
            mRtVTyy+PYQ8dpPtrPl9r/jp4CE3K75R1BLybDCr8OTW5wGqIZLggJT0PQJAPCFS
            B03mWA80HWf84Zlji/P/HnmDPiBmxIx0oNcIO8xxttS/cHBe8T8PkIFcuT3fEOS7
            uuQuJ9kXDmI77lxOzQJBANsWHz22RoznGF8NV9DyaBAffQdFNrWdLR14goQlQ1E4
            g2i47ZrLu0D1CdZNi5MA1x7ARweqArek8o60vBgSr+o=
            -----END RSA PRIVATE KEY-----'''
        converted_format = '''-----BEGIN RSA PRIVATE KEY-----
            MIICXAIBAAKBgQC4BgF7Q524gqtiolTLzUpdabWcFCASDkc8diX9qbKb92vKsmW8
            36GmQWE9EvAXtCu4PfB7YCCiNP+M8iRGGAgHVUlyFzOpSIO2/WSlJVkeNtf7Bpq0
            G9IeQ2OuvPPT1Ar/BOKKbeB2Z2DVJCdINbWb+XO/JzYqdcWxsrmWn3mukwIDAQAB
            AoGAIX7uXBp1pfUa7wwvNR178L7iELPVFpREwSucRKzT1vHVTALm49cs3E9APNaq
            nxXrc1DK6hoYNo5BCc21bpDHPQcs76p/jvpSZdFtfkWxqkJa4A80R7quJr8hxV4d
            ruD+CUhuOsWc8CclhSlBADjAkXupcfRd5OVA6eJ2BOt9w7kCQQDsDhsO716Jn4rU
            qf0iYhGFUmMiwzhrcJ8zxEG7AdXR9nzDE5fOKoO9XmKlh7d7TxeKx9C//JCRTgCF
            zZhaaiIVAkEAx5JzZLwCQVylzMPZBd0P6XzJI8PDN4/XaDMl2P94KsrJaM/uOlal
            0BvOhXG3RrDkyL33VbH3ZE+JccTBcLfABwJAZPpnwszM8SxplC2flozDF/g1ZlKC
            mRtVTyy+PYQ8dpPtrPl9r/jp4CE3K75R1BLybDCr8OTW5wGqIZLggJT0PQJAPCFS
            B03mWA80HWf84Zlji/P/HnmDPiBmxIx0oNcIO8xxttS/cHBe8T8PkIFcuT3fEOS7
            uuQuJ9kXDmI77lxOzQJBANsWHz22RoznGF8NV9DyaBAffQdFNrWdLR14goQlQ1E4
            g2i47ZrLu0D1CdZNi5MA1x7ARweqArek8o60vBgSr+o=
            -----END RSA PRIVATE KEY-----'''
        cert = '''-----BEGIN CERTIFICATE-----
            MIICVDCCAb2gAwIBAgIBATANBgkqhkiG9w0BAQUFADBWMQwwCgYDVQQDEwNhZGYx
            DTALBgNVBAsTBGRhc2YxDDAKBgNVBAoTA2FkZjEMMAoGA1UEBxMDZGFmMQwwCgYD
            VQQIEwNhZGYxDTALBgNVBAYTBHNhZGYwHhcNMTIwMzIyMTU0ODA3WhcNMTMwMzIy
            MTU0ODA3WjBWMQwwCgYDVQQDEwNhZGYxDTALBgNVBAsTBGRhc2YxDDAKBgNVBAoT
            A2FkZjEMMAoGA1UEBxMDZGFmMQwwCgYDVQQIEwNhZGYxDTALBgNVBAYTBHNhZGYw
            gZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBALgGAXtDnbiCq2KiVMvNSl1ptZwU
            IBIORzx2Jf2pspv3a8qyZbzfoaZBYT0S8Be0K7g98HtgIKI0/4zyJEYYCAdVSXIX
            M6lIg7b9ZKUlWR421/sGmrQb0h5DY66889PUCv8E4opt4HZnYNUkJ0g1tZv5c78n
            Nip1xbGyuZafea6TAgMBAAGjMjAwMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYE
            FAiJrjYdLcIOxV1ypEHV8bH0EjGBMA0GCSqGSIb3DQEBBQUAA4GBAGJ3PXzr++CA
            o09DHG73u+sFbOQ71t2jFPq4NNpFSbqBu1clauqALkXM2Kfo8bGBfvE3T7Utwp6P
            ttIavjzTYqz7STDAjR5QPClleGNoY1F7v+07YJXwo0VjAuvBGSZgi8RbNrFlp5St
            E7O1DhtacgTix3Y/V/nYZImm1NbQeciJ
            -----END CERTIFICATE-----'''
        r = self.client.update_ssl_termination(self.ssl_lb.id, enabled=True,
                                               securePort=443,
                                               secureTrafficOnly=False,
                                               privatekey=new_format,
                                               certificate=cert)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.ssl_lb.id)
        r = self.client.get_ssl_termination(self.ssl_lb.id)
        new_ssl = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(new_ssl.enabled, True)
        self.assertEquals(new_ssl.securePort, 443)
        self.assertEquals(new_ssl.secureTrafficOnly, False)
        self.assertEquals(new_ssl.privatekey, converted_format)
        self.assertEquals(new_ssl.certificate, cert)
        zeus_cert_name = self.zeus_vs.getSSLCertificate([self.zeus_vs_name])
        zeus_cert_name = zeus_cert_name[1][0]
        zeus_cert = self.zeus_ssl.getRawCertificate([zeus_cert_name])[1][0]
        self.assertEquals(zeus_cert, cert)
        r = self.client.delete_ssl_termination(self.ssl_lb.id)
        self.assertEquals(r.status_code, 202)

    @attr('positive')
    def test_ssl_termination_pkcs8_key_format(self):
        '''SSL Cert validation - pkcs8 format'''
        pkcs8_format = '''-----BEGIN PRIVATE KEY-----
            MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAJX1EADxuonSKCt4
            ItvVwBAqW71J39quRfg3jaCJp0yAaQMMf3qeG6zbH8uOHb4jsL+lS5NUDzfJHEgT
            ihzU5hc2xvE2pmFHys9t5PWX84lQlHaiGTzDFil1aMdNXBvq/SkORWgY3ZurdC+S
            inMZEqgEqYmWFnqMLIlD48qJu/xDAgMBAAECgYBf6osc/4EgbILzIvmxAWzDKkTZ
            s2ny1yu8E9SMDeArp6sDnzfe90iebN5Odg2CNBP20USg7NB7DzD+zTi3LlopHilR
            JBjJ4rjN3klByq+QQCu0PfET1i1Dk/9DU+cJYdXhNOW2yqSWdXiPVvVvkir4z7Ne
            it1bGlr6cFTMqO0O+QJBAMxzpIu1N8DvpCs0rHmd6Gpv57IPeTqJPs86aq5ktcFv
            U6AfqXfb9W0ye7IHDWrEgrBy+heOBeOjo/SFI4x66z8CQQC7xBHd6vB0HyegU6RH
            PLM3LuUfPMCse8gklcg5vxpVEJ8OBHN63BWigmIZ1DhmV80XNxQAvDgN1/I7CCvA
            WcH9AkB/ONLCcNCxyS1CCXPt9bnjSaFGpuRL7Y1dDD/IJzkGlkzWTf15bTEqcwiP
            vl21+3RLcjB3qdO2VGS4yoRVbUOnAkBN5EmRKOw1D9ONdAU7NBgYdVDBQ5+eLf9a
            BfS41+khjrKcywXo2rHy52mw01POSPAgiE24/Fu4inPHP11+/v01AkBLvAgtanbv
            RNujSQ/aMO/zgsmGoG6ZPDfTqfWSPzKqF9EjMudbQ1B/3AZ2/bPt+F5zN1zDyrxn
            B+uu5TZYZGYS
            -----END PRIVATE KEY-----'''
        cert = '''-----BEGIN CERTIFICATE-----
            MIIDITCCAoqgAwIBAgIGATbHOhIHMA0GCSqGSIb3DQEBBQUAMG4xDDAKBgNVBAYT
            A1VTQTEOMAwGA1UECBMFVGV4YXMxFDASBgNVBAcTC1NhbiBBbnRvbmlvMQ0wCwYD
            VQQKEwRUZXN0MREwDwYDVQQLEwhUb3AgQ0EgMjEWMBQGA1UEAxMNVG9wIENBIDIg
            VGVzdDAeFw0xMjA0MTgyMDUyMTNaFw0yMzA3MDYyMDUyMTNaMGsxDDAKBgNVBAYT
            A1VTQTEOMAwGA1UECBMFVGV4YXMxFDASBgNVBAcTC1NhbiBBbnRvbmlvMQ0wCwYD
            VQQKEwRUZXN0MREwDwYDVQQLEwhFbmQgVXNlcjETMBEGA1UEAxMKd3d3LmV1Lm9y
            ZzCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAlfUQAPG6idIoK3gi29XAECpb
            vUnf2q5F+DeNoImnTIBpAwx/ep4brNsfy44dviOwv6VLk1QPN8kcSBOKHNTmFzbG
            8TamYUfKz23k9ZfziVCUdqIZPMMWKXVox01cG+r9KQ5FaBjdm6t0L5KKcxkSqASp
            iZYWeowsiUPjyom7/EMCAwEAAaOBzDCByTAMBgNVHRMBAf8EAjAAMIGZBgNVHSME
            gZEwgY6AFIHKHyKCb/UX5l1k/k4FDyDD4jfboW6kbDBqMRQwEgYDVQQDEwtUb3Ag
            Q0EgVGVzdDEPMA0GA1UECxMGVG9wIENBMQ0wCwYDVQQKEwRUZXN0MRQwEgYDVQQH
            EwtTYW4gQW50b25pbzEOMAwGA1UECBMFVGV4YXMxDDAKBgNVBAYTA1VTQYIGATbH
            OSgXMB0GA1UdDgQWBBRdttAMJYQrChBJCpkqC1Yvy8nCuzANBgkqhkiG9w0BAQUF
            AAOBgQA8LuaDGGmzCK5VEtPRGJdzBpYYFQUtoAEHoNBSmzBAZIwqAtKU/QmxbHOV
            gDIO5BgO7+ZXFQpWOn6wjLIR9mvpixnEzcnZVPB2g/b32EqahhUZztBuK7EM3TzK
            7bYqlQTqCxN/L+76HLrWXAU6WWlRJPuqc0byOzsSSRrdxrSBrg==
            -----END CERTIFICATE-----'''
        r = self.client.update_ssl_termination(self.ssl_lb.id, enabled=True,
                                               securePort=443,
                                               secureTrafficOnly=True,
                                               privatekey=pkcs8_format,
                                               certificate=cert)
        self.assertEquals(r.status_code, 202)
        ssl = r.request.entity
        self.lbaas_provider.wait_for_status(self.ssl_lb.id)
        r = self.client.get_ssl_termination(self.ssl_lb.id)
        new_ssl = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(new_ssl.enabled, ssl.enabled)
        self.assertEquals(new_ssl.securePort, ssl.securePort)
        self.assertEquals(new_ssl.secureTrafficOnly, ssl.secureTrafficOnly)
        self.assertEquals(new_ssl.privatekey, pkcs8_format)
        self.assertEquals(new_ssl.certificate, ssl.certificate)
        zeus_cert_name = self.zeus_vs.getSSLCertificate([self.zeus_vs_name])
        zeus_cert_name = zeus_cert_name[1][0]
#        time.sleep(lb_const.LbaasConstants.ZEUS_REPLICATION_TIME)
        zeus_cert = self.zeus_ssl.getRawCertificate([zeus_cert_name])[1][0]
        self.assertEquals(zeus_cert, cert)
        r = self.client.delete_ssl_termination(self.ssl_lb.id)
        self.assertEquals(r.status_code, 202)

    @attr('positive')
    def test_ssl_termination_pkcs1_key_format(self):
        '''SSL Cert validation - pkcs1 format'''
        pkcs1_format = '''-----BEGIN RSA PRIVATE KEY-----
            MIICWwIBAAKBgQCV9RAA8bqJ0igreCLb1cAQKlu9Sd/arkX4N42giadMgGkDDH96
            nhus2x/Ljh2+I7C/pUuTVA83yRxIE4oc1OYXNsbxNqZhR8rPbeT1l/OJUJR2ohk8
            wxYpdWjHTVwb6v0pDkVoGN2bq3QvkopzGRKoBKmJlhZ6jCyJQ+PKibv8QwIDAQAB
            AoGAX+qLHP+BIGyC8yL5sQFswypE2bNp8tcrvBPUjA3gK6erA5833vdInmzeTnYN
            gjQT9tFEoOzQew8w/s04ty5aKR4pUSQYyeK4zd5JQcqvkEArtD3xE9YtQ5P/Q1Pn
            CWHV4TTltsqklnV4j1b1b5Iq+M+zXordWxpa+nBUzKjtDvkCQQDMc6SLtTfA76Qr
            NKx5nehqb+eyD3k6iT7POmquZLXBb1OgH6l32/VtMnuyBw1qxIKwcvoXjgXjo6P0
            hSOMeus/AkEAu8QR3erwdB8noFOkRzyzNy7lHzzArHvIJJXIOb8aVRCfDgRzetwV
            ooJiGdQ4ZlfNFzcUALw4DdfyOwgrwFnB/QJAfzjSwnDQscktQglz7fW540mhRqbk
            S+2NXQw/yCc5BpZM1k39eW0xKnMIj75dtft0S3Iwd6nTtlRkuMqEVW1DpwJATeRJ
            kSjsNQ/TjXQFOzQYGHVQwUOfni3/WgX0uNfpIY6ynMsF6Nqx8udpsNNTzkjwIIhN
            uPxbuIpzxz9dfv79NQJAS7wILWp270Tbo0kP2jDv84LJhqBumTw306n1kj8yqhfR
            IzLnW0NQf9wGdv2z7fheczdcw8q8ZwfrruU2WGRmEg==
            -----END RSA PRIVATE KEY-----'''
        cert = '''-----BEGIN CERTIFICATE-----
            MIIDITCCAoqgAwIBAgIGATbHOhIHMA0GCSqGSIb3DQEBBQUAMG4xDDAKBgNVBAYT
            A1VTQTEOMAwGA1UECBMFVGV4YXMxFDASBgNVBAcTC1NhbiBBbnRvbmlvMQ0wCwYD
            VQQKEwRUZXN0MREwDwYDVQQLEwhUb3AgQ0EgMjEWMBQGA1UEAxMNVG9wIENBIDIg
            VGVzdDAeFw0xMjA0MTgyMDUyMTNaFw0yMzA3MDYyMDUyMTNaMGsxDDAKBgNVBAYT
            A1VTQTEOMAwGA1UECBMFVGV4YXMxFDASBgNVBAcTC1NhbiBBbnRvbmlvMQ0wCwYD
            VQQKEwRUZXN0MREwDwYDVQQLEwhFbmQgVXNlcjETMBEGA1UEAxMKd3d3LmV1Lm9y
            ZzCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAlfUQAPG6idIoK3gi29XAECpb
            vUnf2q5F+DeNoImnTIBpAwx/ep4brNsfy44dviOwv6VLk1QPN8kcSBOKHNTmFzbG
            8TamYUfKz23k9ZfziVCUdqIZPMMWKXVox01cG+r9KQ5FaBjdm6t0L5KKcxkSqASp
            iZYWeowsiUPjyom7/EMCAwEAAaOBzDCByTAMBgNVHRMBAf8EAjAAMIGZBgNVHSME
            gZEwgY6AFIHKHyKCb/UX5l1k/k4FDyDD4jfboW6kbDBqMRQwEgYDVQQDEwtUb3Ag
            Q0EgVGVzdDEPMA0GA1UECxMGVG9wIENBMQ0wCwYDVQQKEwRUZXN0MRQwEgYDVQQH
            EwtTYW4gQW50b25pbzEOMAwGA1UECBMFVGV4YXMxDDAKBgNVBAYTA1VTQYIGATbH
            OSgXMB0GA1UdDgQWBBRdttAMJYQrChBJCpkqC1Yvy8nCuzANBgkqhkiG9w0BAQUF
            AAOBgQA8LuaDGGmzCK5VEtPRGJdzBpYYFQUtoAEHoNBSmzBAZIwqAtKU/QmxbHOV
            gDIO5BgO7+ZXFQpWOn6wjLIR9mvpixnEzcnZVPB2g/b32EqahhUZztBuK7EM3TzK
            7bYqlQTqCxN/L+76HLrWXAU6WWlRJPuqc0byOzsSSRrdxrSBrg==
            -----END CERTIFICATE-----'''
        r = self.client.update_ssl_termination(self.ssl_lb.id, enabled=True,
                                               securePort=443,
                                               secureTrafficOnly=False,
                                               privatekey=pkcs1_format,
                                               certificate=cert)
        self.assertEquals(r.status_code, 202)
        ssl = r.request.entity
        self.lbaas_provider.wait_for_status(self.ssl_lb.id)
        r = self.client.get_ssl_termination(self.ssl_lb.id)
        new_ssl = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(new_ssl.enabled, ssl.enabled)
        self.assertEquals(new_ssl.securePort, ssl.securePort)
        self.assertEquals(new_ssl.secureTrafficOnly, ssl.secureTrafficOnly)
        self.assertEquals(new_ssl.privatekey, pkcs1_format)
        self.assertEquals(new_ssl.certificate, ssl.certificate)
#        time.sleep(lb_const.LbaasConstants.ZEUS_REPLICATION_TIME)
        zeus_cert_name = self.zeus_vs.getSSLCertificate([self.zeus_vs_name])
        zeus_cert_name = zeus_cert_name[1][0]
        zeus_cert = self.zeus_ssl.getRawCertificate([zeus_cert_name])[1][0]
        self.assertEquals(zeus_cert, cert)
        r = self.client.delete_ssl_termination(self.ssl_lb.id)
        self.assertEquals(r.status_code, 202)

    @attr('positive')
    def test_ssl_termination_headers(self):
        '''SSL Terminated nodes should receive appropriate headers'''
        r = self.lbaas_provider.ssl_mixed_on(self.ssl_lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.ssl_lb.id)
        if self.config.lbaas_api.is_qa_env or self.ssl_lb.virtualIps[0].type \
                == LBVipTypes.SERVICENET:
            self.client.delete_ssl_termination(self.ssl_lb.id)
            self.assertEquals(r.status_code, 202)
            return
        header_page = SSLConstants.ZEUS_PROTO_HEADER_PAGE
        vip = self.ssl_lb.virtualIps.get_ipv4_vips()[0]
        url = ''.join(['https://', vip.address, header_page])
        page = requests.api.get(url, verify=False).content
        self.assertIn('X-Forwarded-Proto: https ', page)
        url = ''.join(['http://', vip.address, header_page])
        page = requests.api.get(url).content
        self.assertNotIn('X-Forwarded-Proto: https ', page)
        self.client.delete_ssl_termination(self.ssl_lb.id)
        self.assertEquals(r.status_code, 202)

    @attr('positive')
    def test_shared_vip_ssl_termination(self):
        '''SSL Terminated shared VIPS'''
        r = self.lbaas_provider.ssl_mixed_on(self.ssl_lb.id)
        self.assertEquals(r.status_code, 202)
        vip_id = self.ssl_lb.virtualIps.get_ipv4_vips()[0].id
        vips = [{'id': vip_id}]
        port = self.ssl_lb.port - 1
        lb2 = self.lbaas_provider.\
            create_active_load_balancer(virtualIps=vips, port=port).entity
        self.lbs_to_delete.append(lb2.id)
        vs_name = '_'.join([str(self.tenant_id), str(self.ssl_lb.id)])
        vs_s_name = '_'.join([vs_name, 'S'])
        vs2_name = '_'.join([str(self.tenant_id) + '_' + str(lb2.id)])
#        time.sleep(lb_const.LbaasConstants.ZEUS_REPLICATION_TIME)
        ip_groups = self.zeus_vs.getListenTrafficIPGroups([vs_name, vs2_name,
                                                           vs_s_name])
        ip_group1 = ip_groups[1][0][0]
        ip_group2 = ip_groups[1][1][0]
        ip_group3 = ip_groups[1][2][0]
        self.assertEquals(ip_group1, ip_group2)
        self.assertEquals(ip_group2, ip_group3)
        r = self.lbaas_provider.ssl_only_on(self.ssl_lb.id)
        self.assertEquals(r.status_code, 202)
        ip_groups = self.zeus_vs.getListenTrafficIPGroups([vs_name, vs2_name,
                                                           vs_s_name])
        ip_group1 = ip_groups[1][0][0]
        ip_group2 = ip_groups[1][1][0]
        ip_group3 = ip_groups[1][2][0]
        self.assertEquals(ip_group1, ip_group2)
        self.assertEquals(ip_group2, ip_group3)

    @attr('negative')
    def test_share_vip_on_ssl_port(self):
        '''Should not be able to share vip with another LB using the ssl port.
        '''
        vips = [{'type': LBVipTypes.PUBLIC}]
        r = self.lbaas_provider.create_active_load_balancer(virtualIps=vips)
        lb1 = r.entity
        self.lbs_to_delete.append(lb1.id)
        vip_id = lb1.virtualIps.get_ipv6_vips()[0].id
        self.lbaas_provider.ssl_mixed_on(lb1.id)
        vips = [{'id': vip_id}]
        nodes = [{'address': '100.1.1.1', 'condition': 'ENABLED', 'port': 80}]
        r = self.client.create_load_balancer(name='cc_ssl_share_vip_ssl_port',
                                             virtualIps=vips, protocol='HTTP',
                                             port=80, nodes=nodes)
        self.assertEquals(r.status_code, 400)

    @attr('negative')
    def test_set_ssl_port_to_lb_port(self):
        '''Test setting ssl port to lb port'''
        r = self.client.update_ssl_termination(self.ssl_lb.id,
                                               enabled=True,
                                               securePort=self.ssl_lb.port,
                                               secureTrafficOnly=False,
                                               privatekey=
                                               SSLConstants.privatekey,
                                               certificate=
                                               SSLConstants.certificate)
        self.assertEquals(r.status_code, 400)

    @attr('negative')
    def test_set_lb_port_to_ssl_port(self):
        '''Test setting lb port to ssl port'''
        r = self.lbaas_provider.ssl_mixed_on(self.ssl_lb.id)
        ssl = r.request.entity
        new_port = ssl.securePort
        r = self.client.update_load_balancer(self.ssl_lb.id, port=new_port)
        self.assertEquals(r.status_code, 400)

    @attr('positive')
    def test_ssl_term_error_page_defect(self):
        '''Shadow server default error file verification'''
        self.lbaas_provider.ssl_mixed_on(self.ssl_lb.id)
        resp, body = self.zeus_vs.getErrorFile([self.zeus_vs_name])
        self.assertEquals(resp, 200)
        default_page = body[0]
        ep_content = '<html><body>ERROR PAGE</body></html>'
        r = self.client.update_error_page(self.ssl_lb.id, content=ep_content)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.ssl_lb.id)
#        time.sleep(lb_const.LbaasConstants.ZEUS_REPLICATION_TIME)
        resp, updated_ep = self.zeus_vs.getErrorFile([self.zeus_vs_name])
        self.assertNotEqual(updated_ep[0], default_page)
        resp = self.client.delete_error_page(self.ssl_lb.id)
        self.assertEquals(resp.status_code, 202)
        self.lbaas_provider.wait_for_status(self.ssl_lb.id)
#        time.sleep(lb_const.LbaasConstants.ZEUS_REPLICATION_TIME)
        resp, updated_ep = self.zeus_vs.getErrorFile([self.zeus_vs_name])
        self.assertEquals(resp, 200)
        self.assertEquals(updated_ep[0], default_page)

    @attr('positive')
    def test_update_lb_with_ssl_term_active_defect(self):
        '''Udpate LB when SSL termination is active'''
        self.lbaas_provider.ssl_mixed_on(self.ssl_lb.id)
        r = self.client.update_load_balancer(self.ssl_lb.id,
                                             name='cc_new_LB_name')
        self.assertEqual(r.status_code, 202)

    @attr('positive')
    def test_update_lb_to_ssl_port(self):
        '''Update LB to the same port as SSL termination'''
        self.lbaas_provider.ssl_mixed_on(self.ssl_lb.id)
        r = self.client.update_load_balancer(self.ssl_lb.id, port=443)
        self.assertEquals(r.status_code, 400)

    @attr('positive')
    def test_add_ssl_termination_to_lb_on_ssl_port(self):
        '''Add SSL termination to a LB on the SSL port'''
        r = self.lbaas_provider.create_active_load_balancer(port=80)
        lb = r.entity
        self.lbs_to_delete.append(lb.id)
        r = self.client.update_load_balancer(lb.id, port=443)
        self.assertEquals(r.status_code, 202)
        r = self.client.get_load_balancer(lb.id)
        self.assertEquals(r.status_code, 200)
        lb = r.entity
        self.assertTrue(lb.port == 443)
        r = self.client.update_ssl_termination(lb.id, securePort=443,
                                               certificate=
                                               SSLConstants.certificate,
                                               privatekey=
                                               SSLConstants.privatekey)
        self.assertEquals(r.status_code, 400)

    @attr('positive')
    def test_expired_ssl_certificate_after_sync(self):
        '''An ssl cert that has expired returns bad request on sync.'''
        seconds = 30
        priv_key, cert = self.create_private_key_and_certificate(
            seconds_to_expire=seconds)
        time1 = time.time()
        resp = self.lbaas_provider.create_active_load_balancer(
            name="Expired Ssl Cert Sync")
        lb = resp.entity
        self.lbs_to_delete.append(lb.id)
        resp = self.lbaas_provider.client.update_ssl_termination(
            lb.id, securePort=443, privatekey=priv_key,
            certificate=cert, enabled=True, secureTrafficOnly=False)
        self.assertEquals(resp.status_code, 202)
        self.lbaas_provider.wait_for_status(lb.id)
        time2 = time.time()
        while int(time2) <= int(time1) + seconds:
            time.sleep(1)
            time2 = time.time()
        resp = self.lbaas_provider.mgmt_client.sync_load_balancer(lb.id)
        self.assertEquals(resp.status_code, 400)
        self.assertIn("User cert expired", resp.content)

    #this method should be pulled out, abstracted more, cleaned up, and moved
    #to a helper module/class.
    def create_private_key_and_certificate(self, days_to_expire=None,
                                           seconds_to_expire=None):
        if days_to_expire is None and seconds_to_expire is None:
            return None
        #creating csr and priv key
        #callback set to a lambda, because without a callback specified
        #printf is used as the callback and prints to stdout
        privkey = M2Crypto.RSA.gen_key(1024, 65537,
                                       callback=lambda x, y, z: None)
        md = "sha1"
        version = 2
        serial = 10
        pubkey = M2Crypto.EVP.PKey()
        pubkey.assign_rsa(privkey, capture=0)
        req = M2Crypto.X509.Request()
        subj = req.get_subject()
        subj.CN = 'QE'
        subj.ST = 'Texas'
        subj.L = 'Something'
        subj.O = 'Rackspace'
        subj.OU = 'QE'
        subj.C = 'US'
        subj.emailAddress = 'bleh@blehbleh.com'
        subj.Email = 'bleh@blehbleh.com'
        req.set_subject(subj)
        req.set_pubkey(pubkey)
        req.set_version(version)
        req.sign(pubkey, md)

        #create cert
        crt = M2Crypto.X509.X509()
        crt.set_pubkey(pubkey)
        crt.set_issuer(req.get_subject())
        crt.set_subject(req.get_subject())

        time1 = time.time()
        not_before = M2Crypto.ASN1.ASN1_UTCTIME()
        not_before.set_time(int(time1))
        not_after = M2Crypto.ASN1.ASN1_UTCTIME()
        seconds = 0
        if days_to_expire is not None:
            seconds = days_to_expire * 24 * 60 * 60
        if seconds_to_expire is not None:
            seconds += seconds_to_expire
        not_after.set_time(int(time1) + seconds)
        crt.set_not_before(not_before)
        crt.set_not_after(not_after)
        crt.set_serial_number(serial)
        crt.set_version(version)
        crt.sign(pubkey, md)
        return privkey.as_pem(cipher=None), crt.as_pem()


