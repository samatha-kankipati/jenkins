'''This file has been duct taped together from a script Carlos Garza wrote for
LBaaS.  Tell Brandon to clean and organize this.'''

import xmlrpclib
import json


CONFIG_FILE_STR = """
{
  "domains": {
    "rackexp.org": {
      "url": "https://108.166.106.130:23144", 
      "baseDomain": ".rackexp.org", 
      "cred": {
        "passwd": "MuP8k9J2", 
        "user": "dnsuser"
      }
    }, 
    "crc.m2linux.com": {
      "url": "https://184.106.98.162:23142", 
      "baseDomain": ".crc.m2linux.com", 
      "cred": {
        "passwd": "Sh#IQH*M", 
        "user": "dnsuser"
      }
    }, 
    "thesenotions.com": {
      "url": "https://108.166.106.130:23143", 
      "baseDomain": ".thesenotions.com", 
      "cred": {
        "passwd": "mdyt4Z7", 
        "user": "dnsuser"
      }
    }, 
    "local": {
      "url": "https://10.6.61.86:23142", 
      "baseDomain": ".localhost.org", 
      "cred": {
        "passwd": "dnspasswd", 
        "user": "dnsuser"
      }
    }
  }, 
  "curr_domain": "rackexp.org"
}
"""

def load_json():
    json_data = CONFIG_FILE_STR
    out = json.loads(json_data)
    return out

def getCurrentDomain(*args):
    conf = load_json()
    if len(args)==0:
        domain = conf["curr_domain"]
    else:
        domain = args[0]
    url = conf["domains"][domain]["url"]
    baseDomain = conf["domains"][domain]["baseDomain"]
    cred = conf["domains"][domain]["cred"]
    return (url,domain,baseDomain,cred)

class SslDnsClient(object):
    @staticmethod
    def add_A_record(host, ip):
        (url,domain,baseDomain,cred) = getCurrentDomain()
        s = xmlrpclib.ServerProxy(url,allow_none=True)
        res = s.addARecord(cred,host,ip,None)
    
    @staticmethod
    def update_A_record(host, ip):
        (url,domain,baseDomain,cred) = getCurrentDomain()
        s = xmlrpclib.ServerProxy(url,allow_none=True)
        res = s.setARecord(cred,host,ip,None)
    
    @staticmethod
    def delete_A_records(host, ips):
        (url,domain,baseDomain,cred) = getCurrentDomain()
        s = xmlrpclib.ServerProxy(url)
        deletedIps = s.delARecord(cred,host,*ips)

    @staticmethod
    def list_A_records():
        (url,curr_domain,baseDomain,cred) = getCurrentDomain()
        s = xmlrpclib.ServerProxy(url)
        A = s.getARecords(cred)
        
            
class SslGen(object):
    
    @staticmethod
    def generate(host):
        url = "http://jdk.rackexp.org:12345"

        sslservice = xmlrpclib.ServerProxy(url)
        
        subj = {
              "C": "US",
              "OU": "RackExp Organization",
              "L": "San Antonio",
              "O": "RackExp",
              "ST": "Texas"
        }
        subj["CN"] = "".join([host,".rackexp.org"])
        
        caKey = SslGen.ca_key
        caCrt = SslGen.ca_cert
        chain = SslGen.ca_chain
        
        keySize = 2048
        
        (key,csr,crt) = sslservice.newCrt(keySize,subj,caKey,caCrt)
        
        #sys.stdout.write("Key = %s\n"%key)
        #sys.stdout.write("CSR = %s\n"%csr)
        #sys.stdout.write("CRT = %s\n"%crt)
        return (key,csr,crt)
        
    ca_cert = """-----BEGIN CERTIFICATE-----
MIIERzCCAy+gAwIBAgIBAjANBgkqhkiG9w0BAQUFADB5MQswCQYDVQQGEwJVUzEO
MAwGA1UECBMFVGV4YXMxDjAMBgNVBAcTBVRleGFzMRowGAYDVQQKExFSYWNrU3Bh
Y2UgSG9zdGluZzEUMBIGA1UECxMLUmFja0V4cCBDQTQxGDAWBgNVBAMTD2NhNC5y
YWNrZXhwLm9yZzAeFw0xMjAxMTIxNzU3MDZaFw0xNDAxMTAxNzU3MDZaMHkxCzAJ
BgNVBAYTAlVTMQ4wDAYDVQQIEwVUZXhhczEOMAwGA1UEBxMFVGV4YXMxGjAYBgNV
BAoTEVJhY2tTcGFjZSBIb3N0aW5nMRQwEgYDVQQLEwtSYWNrRXhwIENBNTEYMBYG
A1UEAxMPY2E1LnJhY2tleHAub3JnMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEAsVK6npit7Q3NLlVjkpiDj+QuIoYrhHTL5KKzj6CrtQsFYukEL1YEKNlM
/dv8id/PkmdQ0wCNsk8d69CZKgO4hpN6O/b2aUl/vQcrW5lv3fI8x4wLu2Ri92vJ
f04RiZ3Jyc0rgrfGyLyNJcnMIMjnFV7mQyy+7cMGKCDgaLzUGNyR5E/Mi4cERana
xyp1nZI3DjA11Kwums9cx5VzS0Po1RyBsu7Xnpv3Fp2QqCBgdX8uaR5RuSak40/5
Jv2ORv28mi9AFu2AIRj6lrDdaLQGAXnbDk8b0ImEvVOe/QASsgTSmzOtn3q9Yejl
peQ9PFImVr2TymTF6UarGRHCWId1dQIDAQABo4HZMIHWMA8GA1UdEwEB/wQFMAMB
Af8wgaMGA1UdIwSBmzCBmIAUoeopOMWIEeYGtksI+T+ZjXWKc4ahfaR7MHkxCzAJ
BgNVBAYTAlVTMQ4wDAYDVQQIEwVUZXhhczEOMAwGA1UEBxMFVGV4YXMxGjAYBgNV
BAoTEVJhY2tTcGFjZSBIb3N0aW5nMRQwEgYDVQQLEwtSYWNrRXhwIENBMzEYMBYG
A1UEAxMPY2EzLnJhY2tleHAub3JnggECMB0GA1UdDgQWBBSJF0Is0Wn7cVQ2iz/x
W/xdobdNezANBgkqhkiG9w0BAQUFAAOCAQEAHUIe5D3+/j4yca1bxXg0egL0d6ed
Cam/l+E/SHxFJmlLOfkMnDQQy/P31PBNrHPdNw3CwK5hqFGl8oWGLifRmMVlWhBo
wD1wmzm++FQeEthhl7gBkgECxZ+U4+WRiqo9ZiHWDf49nr8gUONF/qnHHkXTOZKo
vB34N2y+nONDvyzky2wzbvU46dW7Wc6Lp2nLTt4amC66V973V31Vlpbzg3C0K7sc
PA2GGTsiW6NF1mLd4fECgXslaQggoAKax7QY2yKrXLN5tmrHHThV3fIvLbSNFJbl
dZsGmy48UFF4pBHdhnE8bCAt8KgK3BJb0XqNrUxxI6Jc/Hcl9AfppFIEGw==
-----END CERTIFICATE-----"""
    ca_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAsVK6npit7Q3NLlVjkpiDj+QuIoYrhHTL5KKzj6CrtQsFYukE
L1YEKNlM/dv8id/PkmdQ0wCNsk8d69CZKgO4hpN6O/b2aUl/vQcrW5lv3fI8x4wL
u2Ri92vJf04RiZ3Jyc0rgrfGyLyNJcnMIMjnFV7mQyy+7cMGKCDgaLzUGNyR5E/M
i4cERanaxyp1nZI3DjA11Kwums9cx5VzS0Po1RyBsu7Xnpv3Fp2QqCBgdX8uaR5R
uSak40/5Jv2ORv28mi9AFu2AIRj6lrDdaLQGAXnbDk8b0ImEvVOe/QASsgTSmzOt
n3q9YejlpeQ9PFImVr2TymTF6UarGRHCWId1dQIDAQABAoIBACm7jrBEvqpL1T5S
WlzmCBCVY0Y8zYEe+92TbS8gYUj6jwn4TUPWuqPigHw+ifDo+7E5H4yJVM/iTuhw
75szxPnnO51hQh0Fb0rNpSaptepGWIeeLiSsO55/f6y2cuoweI1F/DeHiQE1XwLF
u4T7w2cELq0gms7aV1iaZDZCOqie3Dub7KAL76jwpG3ECQlWzF04TjQ5lZBdM7Fa
z3fbaJ497k5DoPbZMqGi2eR7P8NJAPjIpmaL3vls2vlmWwd/7D10AJUNoILb74jm
648YFo76yKS15jtHFvifSaxEg3gjmth7IuRF4SbL5AjFqhj1qo9yQKLep7pNv9Bx
0eYoqwECgYEA4r3h/4WGuXrnh36zJW860O7+pO3l8rm83wP1oGc8xCK74aBQP5zL
JHaJypeImisZg3OcKL5IBop76LZ/i5oCDozHvTRByFHYnkRU3oh6FDcIvPkDCB7o
qq8y6Q+gbTJlKzpSxoRnj1rkHOweDzNG/7QD/D/g2z5ZejW3xC6H3R8CgYEAyDRe
Qv/ATAn1F0r7LweShjAcqaf5DxmXNDpaw7Wj0OKZxyxYw6aPVm3LnZP1tmGe9UlE
CFRTX5Y98x+9Z+PFtYgW0EdZCVQXKLkGJUhD8SRxyaS5Tlz1hzSHtbxGbDFuecRd
Qv/XmrJapVQrT4TMa5ivw836tjQhVqCrNyCHRusCgYEAk9o793IrkuFI/rqouN1a
HgnqNMQIcQma1lXvomQPZNo9Z3gxO/nTIXjGizva0KUQIv6NMqg5sUI2YF44t2B6
vOAiEwdzadutBC8MpHucF3h3kzpRNsdo8nwCF6Wf9/SnsdN7TIXkPb+IBjAVvdWz
E2RgQOmqh2yVzjIfHac14wMCgYEAkgiA6WYcIlrxB/iNmBRx8KePgMEhjr4f6NzX
8AHCaE+h1AKpDK2lyGl2KI8Qn+Q9SrYShfDcj9DLh1gTlIA0auHFok8oxwErk2zC
6tb3mCH5Thh1go+UGPdcNlgLFkhISVHOpVxxLEoEjKwEm5BGfAV3z9+jjNwhpUq1
GRUFF9kCgYBu/b84bEmflvv0z412hiQuIjDrJWPLUENfJujs6RitU42KV78Momif
/qrCK1exgdMiXET3nXg7Ff2zi5O8QArM3ITaWOczukAXaAeTPKm9o59ubb4PsU9K
A8Lv1syLCAC54udcbBGG2gvv7KVwJZQhmwItdX0ev5oAY3DTbJwstg==
-----END RSA PRIVATE KEY-----"""
    ca_chain = """-----BEGIN CERTIFICATE-----
MIIERzCCAy+gAwIBAgIBAjANBgkqhkiG9w0BAQUFADB5MQswCQYDVQQGEwJVUzEO
MAwGA1UECBMFVGV4YXMxDjAMBgNVBAcTBVRleGFzMRowGAYDVQQKExFSYWNrU3Bh
Y2UgSG9zdGluZzEUMBIGA1UECxMLUmFja0V4cCBDQTQxGDAWBgNVBAMTD2NhNC5y
YWNrZXhwLm9yZzAeFw0xMjAxMTIxNzU3MDZaFw0xNDAxMTAxNzU3MDZaMHkxCzAJ
BgNVBAYTAlVTMQ4wDAYDVQQIEwVUZXhhczEOMAwGA1UEBxMFVGV4YXMxGjAYBgNV
BAoTEVJhY2tTcGFjZSBIb3N0aW5nMRQwEgYDVQQLEwtSYWNrRXhwIENBNTEYMBYG
A1UEAxMPY2E1LnJhY2tleHAub3JnMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEAsVK6npit7Q3NLlVjkpiDj+QuIoYrhHTL5KKzj6CrtQsFYukEL1YEKNlM
/dv8id/PkmdQ0wCNsk8d69CZKgO4hpN6O/b2aUl/vQcrW5lv3fI8x4wLu2Ri92vJ
f04RiZ3Jyc0rgrfGyLyNJcnMIMjnFV7mQyy+7cMGKCDgaLzUGNyR5E/Mi4cERana
xyp1nZI3DjA11Kwums9cx5VzS0Po1RyBsu7Xnpv3Fp2QqCBgdX8uaR5RuSak40/5
Jv2ORv28mi9AFu2AIRj6lrDdaLQGAXnbDk8b0ImEvVOe/QASsgTSmzOtn3q9Yejl
peQ9PFImVr2TymTF6UarGRHCWId1dQIDAQABo4HZMIHWMA8GA1UdEwEB/wQFMAMB
Af8wgaMGA1UdIwSBmzCBmIAUoeopOMWIEeYGtksI+T+ZjXWKc4ahfaR7MHkxCzAJ
BgNVBAYTAlVTMQ4wDAYDVQQIEwVUZXhhczEOMAwGA1UEBxMFVGV4YXMxGjAYBgNV
BAoTEVJhY2tTcGFjZSBIb3N0aW5nMRQwEgYDVQQLEwtSYWNrRXhwIENBMzEYMBYG
A1UEAxMPY2EzLnJhY2tleHAub3JnggECMB0GA1UdDgQWBBSJF0Is0Wn7cVQ2iz/x
W/xdobdNezANBgkqhkiG9w0BAQUFAAOCAQEAHUIe5D3+/j4yca1bxXg0egL0d6ed
Cam/l+E/SHxFJmlLOfkMnDQQy/P31PBNrHPdNw3CwK5hqFGl8oWGLifRmMVlWhBo
wD1wmzm++FQeEthhl7gBkgECxZ+U4+WRiqo9ZiHWDf49nr8gUONF/qnHHkXTOZKo
vB34N2y+nONDvyzky2wzbvU46dW7Wc6Lp2nLTt4amC66V973V31Vlpbzg3C0K7sc
PA2GGTsiW6NF1mLd4fECgXslaQggoAKax7QY2yKrXLN5tmrHHThV3fIvLbSNFJbl
dZsGmy48UFF4pBHdhnE8bCAt8KgK3BJb0XqNrUxxI6Jc/Hcl9AfppFIEGw==
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIERzCCAy+gAwIBAgIBAjANBgkqhkiG9w0BAQUFADB5MQswCQYDVQQGEwJVUzEO
MAwGA1UECBMFVGV4YXMxDjAMBgNVBAcTBVRleGFzMRowGAYDVQQKExFSYWNrU3Bh
Y2UgSG9zdGluZzEUMBIGA1UECxMLUmFja0V4cCBDQTMxGDAWBgNVBAMTD2NhMy5y
YWNrZXhwLm9yZzAeFw0xMjAxMTIxNzU3MDZaFw0xNDAxMTAxNzU3MDZaMHkxCzAJ
BgNVBAYTAlVTMQ4wDAYDVQQIEwVUZXhhczEOMAwGA1UEBxMFVGV4YXMxGjAYBgNV
BAoTEVJhY2tTcGFjZSBIb3N0aW5nMRQwEgYDVQQLEwtSYWNrRXhwIENBNDEYMBYG
A1UEAxMPY2E0LnJhY2tleHAub3JnMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEApOqRiZRrgNSHs9VW3sfow1fQzepczUK1X+4SxpxIjHFN8QS+zQeYOcHP
zdpHGCQLG35pWtY0iKMjMcA6AzZ8KHE0tCmGmOjEB2gjlAwOa0eHb2NHN44duu/n
ESEn2NJr05r2/q9bihjy7qQlVCrcRcXAQpj2F7t875Rq90a0d+AlHfGtN8su/S6y
G/fbUjP4fvIAzDJuhPoD1CG1zIJqo7EAy1kaqwh4jzvUt1WYcreRXNe6FJ4EMtyY
oeC/mbA9m/Zsz1FE7WR2auY2yC2Q3gHBzTmJtvuxNTCn96n0EFpzzXBz0W7wl9gu
jd+ikFjzT3Y5KhQMNmLXEMP80tvdPQIDAQABo4HZMIHWMA8GA1UdEwEB/wQFMAMB
Af8wgaMGA1UdIwSBmzCBmIAUQS5J4Ijc/J47kM0yVk5k1DH1Oo6hfaR7MHkxCzAJ
BgNVBAYTAlVTMQ4wDAYDVQQIEwVUZXhhczEOMAwGA1UEBxMFVGV4YXMxGjAYBgNV
BAoTEVJhY2tTcGFjZSBIb3N0aW5nMRQwEgYDVQQLEwtSYWNrRXhwIENBMjEYMBYG
A1UEAxMPY2EyLnJhY2tleHAub3JnggECMB0GA1UdDgQWBBSh6ik4xYgR5ga2Swj5
P5mNdYpzhjANBgkqhkiG9w0BAQUFAAOCAQEALMwRm7OXBru1H/1IqxNL+/Uky6BB
01Acwi7ESNDnsKd/m2G+SUd1Xy3v+fI6Im1qWBM8XthDHaYBQmjFTr+qOkbhQhOR
Z+T5s+zPF0yYo5hYU3xtotuL84SusrFMZYw0KzIwgRvRsMexZmenCTNHOOW7J2/C
hLJ5rBZ9oX2X7arB65JdTu/EI/Zt32I83Xh/+GtK8mZegP12GOyDSnxuWyZi7noK
21zoWKcxFo+qMwORgJ3ZO7BqANMUYQHUoytK9nxJZUHBSpUq08Kq9LTuIpdtyoJD
fGgT3quNreSCMmaTqxCgaTSOk1BuQDEbsVX+gYvULGfePNIUHYyFKdTA0w==
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIERzCCAy+gAwIBAgIBAjANBgkqhkiG9w0BAQUFADB5MQswCQYDVQQGEwJVUzEO
MAwGA1UECBMFVGV4YXMxDjAMBgNVBAcTBVRleGFzMRowGAYDVQQKExFSYWNrU3Bh
Y2UgSG9zdGluZzEUMBIGA1UECxMLUmFja0V4cCBDQTIxGDAWBgNVBAMTD2NhMi5y
YWNrZXhwLm9yZzAeFw0xMjAxMTIxNzU3MDRaFw0xNDAxMTAxNzU3MDRaMHkxCzAJ
BgNVBAYTAlVTMQ4wDAYDVQQIEwVUZXhhczEOMAwGA1UEBxMFVGV4YXMxGjAYBgNV
BAoTEVJhY2tTcGFjZSBIb3N0aW5nMRQwEgYDVQQLEwtSYWNrRXhwIENBMzEYMBYG
A1UEAxMPY2EzLnJhY2tleHAub3JnMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEAmtodLv2WXOJgtUtcDJR6GYztsHsUoZQ+jjg2N0bC0UmZbjbtkx+w+N1m
FBiBG5pMYCBzi3d0VGicGD3ZSIKEqoSnf3PHW5wJEJQjFqNcI0wcxJGrPAcp3Th5
4bmLwUnxQt9OK+icmRMwvqtxPf6zk14JUC830oQ8WNyOXlT4qxJqSwDK51sViTYO
P912oyKmDqguKgs1xgWQz78ABWbRgu2Yg9+R9GybvUcyiSo1qox+FlXVOoA8tFlE
lU8h3b1XCW80rzrdHICvSulMnVGhA2gWyWpznQjinzui1QJZbtdDLEcFZJEf1Tnl
/7Fh5Xo6n5KH4Rc1pheKaMkMoU2PBQIDAQABo4HZMIHWMA8GA1UdEwEB/wQFMAMB
Af8wgaMGA1UdIwSBmzCBmIAUfVXL/xzk1fBzmAKxZtd5YYcp3NmhfaR7MHkxGDAW
BgNVBAMTD2NhMS5yYWNrZXhwLm9yZzEUMBIGA1UECxMLUmFja0V4cCBDQTExGjAY
BgNVBAoTEVJhY2tTcGFjZSBIb3N0aW5nMQ4wDAYDVQQHEwVUZXhhczEOMAwGA1UE
CBMFVGV4YXMxCzAJBgNVBAYTAlVTggECMB0GA1UdDgQWBBRBLkngiNz8njuQzTJW
TmTUMfU6jjANBgkqhkiG9w0BAQUFAAOCAQEAH9qo0y5EZSUpX2baRHEkUjeuLQnK
4cIyAoGBzyBTm9vev0ezLMXwXp/3J9KTSizLfRZZPMw2rFhy738nf6rI8aCCi+KE
afyI1EJTRZmgxDbANwVcK+k85yuWf4P27+4WL82E7c26wghldh52YLIz+GnfQMIb
vTuSPbUubcg67CfEL7c4tgqhMzmcpKZwKbgzla0JkYfeLq8boclFYN+RkA9lo7OG
tyLdgpJ+aLwxQzgvA1qMLUilmaO26i8cN7kw56uNalVwSFt6s39JVdlRYhrwoAAy
9T/mt/ioL4NW2rbC3XJVKSD+tRyfEb+5YjmGkPJKof19Ys5+Vro7NOn08g==
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIERzCCAy+gAwIBAgIBAjANBgkqhkiG9w0BAQUFADB5MRgwFgYDVQQDEw9jYTEu
cmFja2V4cC5vcmcxFDASBgNVBAsTC1JhY2tFeHAgQ0ExMRowGAYDVQQKExFSYWNr
U3BhY2UgSG9zdGluZzEOMAwGA1UEBxMFVGV4YXMxDjAMBgNVBAgTBVRleGFzMQsw
CQYDVQQGEwJVUzAeFw0xMjAxMTIxNzU3MDRaFw0xNDAxMTAxNzU3MDRaMHkxCzAJ
BgNVBAYTAlVTMQ4wDAYDVQQIEwVUZXhhczEOMAwGA1UEBxMFVGV4YXMxGjAYBgNV
BAoTEVJhY2tTcGFjZSBIb3N0aW5nMRQwEgYDVQQLEwtSYWNrRXhwIENBMjEYMBYG
A1UEAxMPY2EyLnJhY2tleHAub3JnMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEAuEvwdPdXflt17FbLUOSDPEMBRKcZwnNpfqNK2b7X5ADYFFvaLMHW6PGr
SHDRBpqpwqmvyJ28xgKZ+CoxHJhdHAWmTvk6h9kuO8o8oyIBpD6YDNe95ApSvUCs
DTS3DW8GpNeHCKBPkUci4EazSeGkuKEpG+xWZoLm0USiTAbnbuskG/5ASw+KQNKU
DcBHkBYlym6KSlxkz+XOJO5hrMqGbe0bhhRClqqQIh5WDmDriA5aLm07lFqmnwXz
koVsTmCwbbMMy11FzDSA59klBB+IA3UvD9LFbmH0GVWkueo5fOAqTcNkdSFC34pG
GbnZYA4rGrgVBwxbjCzRmB2fCgTjEwIDAQABo4HZMIHWMA8GA1UdEwEB/wQFMAMB
Af8wgaMGA1UdIwSBmzCBmIAUOMPfFuJzzCcpUTLox0wDdc5iIt6hfaR7MHkxGDAW
BgNVBAMTD2NhMS5yYWNrZXhwLm9yZzEUMBIGA1UECxMLUmFja0V4cCBDQTExGjAY
BgNVBAoTEVJhY2tTcGFjZSBIb3N0aW5nMQ4wDAYDVQQHEwVUZXhhczEOMAwGA1UE
CBMFVGV4YXMxCzAJBgNVBAYTAlVTggEBMB0GA1UdDgQWBBR9Vcv/HOTV8HOYArFm
13lhhync2TANBgkqhkiG9w0BAQUFAAOCAQEAGZ1Yt/0Calmm7fPNOkzixof50xej
GJ4LjELTaawVLEfl3dcmoAbqcGlaygAGxTVoSw47j3kOOyABUBSfGoWUkav21kQg
rXUEnx8ToplVAvn/qZHTrrzJCLBk/K/BzBhBnVf3ma5GkJ0kcwQd3Cn7FjKzl9Be
oisPp9fQ5WBeRO5QizJDjgj8LS63ST01ni7/U2EhBIdfoBM5vMnGhc5Ns6mamPjJ
jH3zzLdtGaN6UzjUUUVTAoah0qHsL4K7haFA0uiJldiCt8mZfN7F6nzb23GVuAdK
ZLtkSGD042R/ppnfdZ5NautNxA9tNVH0pkjXkba/qzGz935bri1SvxIzzg==
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIDnzCCAoegAwIBAgIBATANBgkqhkiG9w0BAQUFADB5MRgwFgYDVQQDEw9jYTEu
cmFja2V4cC5vcmcxFDASBgNVBAsTC1JhY2tFeHAgQ0ExMRowGAYDVQQKExFSYWNr
U3BhY2UgSG9zdGluZzEOMAwGA1UEBxMFVGV4YXMxDjAMBgNVBAgTBVRleGFzMQsw
CQYDVQQGEwJVUzAeFw0xMjAxMTIxNzU3MDRaFw0xNDAxMTExNzU3MDRaMHkxGDAW
BgNVBAMTD2NhMS5yYWNrZXhwLm9yZzEUMBIGA1UECxMLUmFja0V4cCBDQTExGjAY
BgNVBAoTEVJhY2tTcGFjZSBIb3N0aW5nMQ4wDAYDVQQHEwVUZXhhczEOMAwGA1UE
CBMFVGV4YXMxCzAJBgNVBAYTAlVTMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEAn+myn3GNUG8jOEnwMREdDzjLskljm3mPtPUVJCyf6pQmXbpAsCp8mpQH
L7AS2BVHImpq7762Q29u46j+W+6wmdn3rZaZsQ6HZrkvlzTxip6oJtMszobkrdsB
ZFTH2kvNWpktgAuxc9Dr6oinBYGr62vFz+LI93CPloI7gv7N8YABkdWnNuqrYdtA
wE4OMdXy1kWWi7jENZdRmb8A6qmQj1NZmv5Jgwggxy40fH4m88GK098Prl6oerlX
als7HdWCpk3iglOhxN0+sg88mufWNr71YsQ5b1oVhtv/5qzsq/DdPrOpffHjYRPs
A+YgavRfrKSWz4fuZOBqaXGnNdf+NQIDAQABozIwMDAPBgNVHRMBAf8EBTADAQH/
MB0GA1UdDgQWBBQ4w98W4nPMJylRMujHTAN1zmIi3jANBgkqhkiG9w0BAQUFAAOC
AQEAMjB0DHQn5C2WpWXZEEEAQvGmzC/NvoJ9K7Kkizpd9I8GOz5/cpLtEXSQdlq7
2aOrLb9b5jtuuWiu9rpkxo/vX5jMCPHW/jr+51v2InSfe8SJSgcciGFdFBz++rve
DhMvprCgbwWnyqHd+2B8KoLt9k/x5MUWPTRmMtlonOVe7+wgiwdgyQLeZuQp0jg8
/dGFHwFi/6Ns2Cd5UKT8sbt22lN0uatddQ9bwJ0dFg0tvh6aVNRa121mYtmtSsU9
BF9RsonnOUtCYQRR+ovVvAyT0XKBfixtwndpW26vd5BKJQ1X5i3W1rssQwzPYBIW
LE3/pvvbh3Ar83QycrLE/w1/KA==
-----END CERTIFICATE-----
"""