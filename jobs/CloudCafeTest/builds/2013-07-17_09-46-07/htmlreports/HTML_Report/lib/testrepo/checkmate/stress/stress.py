import eventlet
eventlet.monkey_patch()

import httplib

from testrepo.common.testfixtures.checkmate import CheckmateFixture
from eventlet.green import urllib2

class StressTest(CheckmateFixture):

    def setUp(self):
        self.success_count = 0
        self.count = 0
        self.url = '10.23.248.146:8080' # TODO: Fix DNS lookup

    def parse(self, deployment):
        ''' Returns the result of a call to /deployments/parse '''
        eventlet.sleep()
        return self.checkmate_provider.client.parse_deployment(deployment=deployment)

    def test_parse(self):
        ''' Testing Checkmate Plan Function '''

        api_response = self.parse(wordpress)
        self.assertTrue(api_response.ok, "Plan get failed with error: \
            '%s' and status code '%s': \n '%s'" \
            % (api_response.reason, api_response.status_code,
                api_response.json))
        self.success_count += 1

    def test_parse_limit(self):
        ''' Testing server limit for parsing '''
        conn = httplib.HTTPConnection(self.url)        
        pool = eventlet.GreenPool()
        
        while True:
            try:
                conn.request("GET", "/index.html")
                res = conn.getresponse()
                if res.status is 200:
                    pool.spawn_n(self.test_parse)
                    eventlet.sleep()
                    self.count += 1
                else:
                    raise Exception("Can't reach server at %s after %s successful parses" \
                                    "and %s tries" % (self.url, self.success_count, self.count))
                    break
            except (Exception, KeyboardInterrupt), exc:
                raise Exception("Exception %s with %s successful parses and %s tries" %
                                (exc, self.success_count, self.count))
                break       
                
    def test_deployment(self):
        ''' Testing Checkmate Deployments '''

        # TODO: Test deployments without embedding them
        api_response = self.checkmate_provider.client.deploy(deployment=wordpress)
        self.assertTrue(api_response.ok, "Plan get failed with error: \
            '%s' and status code '%s': \n '%s'" \
            % (api_response.reason, api_response.status_code,
                api_response.json))

wordpress="""blueprint:
  id: 0255a076c7cf4fd38c69b6727f0b37ea
  name: Managed Cloud WordPress w/ MySQL on VMs
  description: |
    Create a multi-server WordPress deployment on any cloud account using the
    Chef cookbooks created by the Managed Cloud team.
    This deployment includes a default environment and blueprint. It has been
    designed with Managed Cloud defaults incorporated in it.
  services:
    lb:
      open-ports:
      - 80/tcp
      component:
        interface: proxy
        type: load-balancer
        constraints:
        - algorithm: ROUND_ROBIN
      relations:
        web: http
        master: http
      exposed: true
    master:
      component:
        type: application
        name: wordpress-master-role
        constraints:
          wordpress/version: 3.4.1
          wordpress/database/create_db: "true"
          wordpress/database/create_db_user: "true"
      relations:
        wordpress/database:
          interface: mysql
          service: backend
        wordpress/database/host:
          interface: host
          service: backend
          attribute: private_ip
        wordpress/database/server_root_password:
          interface: host
          service: backend
          attribute: password
        varnish/master_backend:
          interface: host
          attribute: private_ip
        lsyncd/slaves:
          interface: host
          service: web
          attribute: private_ip
      constraints:
      - count: 1
    web:
      component:
        type: application
        name: wordpress-web-role
        constraints:
          wordpress/version: 3.4.1
      relations:
        wordpress/database:
          interface: mysql
          service: backend
        varnish/master_backend:
          interface: host
          service: master
          attribute: private_ip
        lsyncd/slaves:
          interface: host
          attribute: private_ip
        wordpress/database/host:
          interface: host
          service: backend
          attribute: private_ip
    backend:
      component:
        name: mysql-master-role
        interface: mysql
        type: database
      relations:
        mysql/host:
          interface: host
          attribute: private_ip
        mysql/server_root_password:
          interface: host
          attribute: password
  options:
    domain:
      regex: ^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$
      constrains:
      - setting: apache/domain_name
        service: web
        resource_type: application
      - setting: apache/domain_name
        service: master
        resource_type: application
      description: 'The domain you wish to host your blog on. (ex: example.com)'
      label: Domain
      sample: example.com
      type: combo
      required: true
      choice: []
    path:
      constrains:
      - setting: wordpress/path
        service: web
        resource_type: application
      - setting: wordpress/path
        service: master
        resource_type: application
      description: 'The path you wish to host your blog on under your domain. (ex: /blog)'
      default: /
      label: Path
      sample: /blog
      type: string
    register-dns:
      default: false
      type: boolean
      label: Create DNS records
    region:
      required: true
      type: select
      default: ORD
      label: Region
      choice:
      - DFW
      - ORD
      - LON
    prefix:
      constrains:
      - setting: wordpress/database/prefix
        service: master
        resource_type: application
      - setting: wordpress/database/prefix
        service: web
        resource_type: application
      help: |
        Note that this also the user name, database name, and also identifies this
        wordpress install from other ones you might add later to the same deployment.
      default: wp_
      required: true
      label: Prefix
      type: string
      description: The application ID (and wordpress table prefix).
    password:
      type: password
      description: Password to use for service. Click the generate button to generate a random password.
      label: Password
      constrains:
      - setting: resources/wp user/password
    username:
      type: string
      description: The user name to use for Wordpress and the deployment servers and database.
      required: true
      label: Username
      default: wp_user
      constrains:
      - setting: resources/wp user/name
    os:
      constrains:
      - setting: os
        service: web
        resource_type: compute
      - setting: os
        service: master
        resource_type: compute
      - setting: os
        service: backend
        resource_type: compute
      description: The operating system for the all servers.
      default: Ubuntu 12.04
      label: Operating System
      type: select
      choice:
      - Ubuntu 12.04
    server_size:
      constrains:
      - setting: memory
        service: web
        resource_type: compute
      - setting: memory
        service: master
        resource_type: compute
      description: The size of the Wordpress server instances in MB of RAM.
      default: 512
      label: Server Size
      type: select
      choice:
      - name: 512 Mb
        value: 512
      - name: 1 Gb
        value: 1024
      - name: 2 Gb
        value: 2048
      - name: 4 Gb
        value: 4096
      - name: 8 Gb
        value: 8092
      - name: 16 Gb
        value: 16384
      - name: 30 Gb
        value: 30720
    web_server_count:
      constrains:
      - setting: count
        service: web
        resource_type: application
      description: The number of WordPress servers in addition to the master server
      default: 1
      label: Additional Web Servers
      type: int
      constraints:
      - greater-than: 0
    database_size:
      constrains:
      - setting: memory
        service: backend
        resource_type: compute
      description: The size of the database instance in MB of RAM.
      default: 1024
      label: Database Instance Size
      type: select
      choice:
      - name: 512 Mb (20 Gb disk)
        value: 512
      - name: 1 Gb (40 Gb disk)
        value: 1024
      - name: 2 Gb (80 Gb disk)
        value: 2048
      - name: 4 Gb (160 Gb disk)
        value: 4096
      - name: 8 Gb (320 Gb disk)
        value: 8192
      - name: 16 Gb (620 Gb disk)
        value: 15872
      - name: 30 Gb (1.2 Tb disk)
        value: 30720
    web_server_protocol:
      default: http
      label: HTTP Protocol
      type: select
      choice:
      - name: HTTP Only
        value: http
        precludes:
        - ssl_certificate
        - ssl_private_key
      - name: HTTP and HTTPS
        value: http_and_https
        requires:
        - ssl_certificate
        - ssl_private_key
      help: Use HTTP or HTTP and HTTPS (SSL) for web traffic. HTTPS requires an SSL certificate and private key.
      description: Use HTTP or HTTP and HTTPS (SSL) for web traffic. HTTPS requires an SSL certificate and private key.
      constrains:
      - setting: protocol
        service: lb
        resource_type: load-balancer
    ssl_certificate:
      sample: |
        -----BEGIN CERTIFICATE-----
        Encoded Certificate
        -----END CERTIFICATE-----
      constrains:
      - setting: apache/ssl_cert
        service: web
        resource_type: application
      - setting: apache/ssl_cert
        service: master
        resource_type: application
      type: text
      description: SSL certificate in PEM format. Make sure to include the BEGIN and END certificate lines.
      label: SSL Certificate
    ssl_private_key:
      sample: |
        -----BEGIN PRIVATE KEY-----
        Encoded key
        -----END PRIVATE KEY-----
      constrains:
      - setting: apache/ssl_private_key
        service: web
        resource_type: application
      - setting: apache/ssl_private_key
        service: master
        resource_type: application
      type: text
      label: SSL Certificate Private Key
    ssl_intermediate_certificate:
      constrains:
      - resource_type: application
        service: web
        setting: apache/cacert
      - resource_type: application
        service: master
        setting: apache/cacert
      label: SSL CA Cert
      description: The collection of trusted root and/or intermediate certification authority certificates.
      sample: |
        -----BEGIN PRIVATE KEY-----
        Encoded key
        -----END PRIVATE KEY-----
      type: text
  resources:
    wp keys:
      type: key-pair
      constrains:
      - setting: lsyncd/user/ssh_private_key
        service: web
        resource_type: application
        attribute: private_key
      - setting: lsyncd/user/ssh_private_key
        service: master
        resource_type: application
        attribute: private_key
      - setting: lsyncd/user/ssh_pub_key
        service: web
        resource_type: application
        attribute: public_key_ssh
      - setting: lsyncd/user/ssh_pub_key
        service: master
        resource_type: application
        attribute: public_key_ssh
    wp user:
      type: user
      constrains:
      - setting: lsyncd/user/name
        service: web
        resource_type: application
        attribute: name
      - setting: lsyncd/user/name
        service: master
        resource_type: application
        attribute: name
      - setting: mysql/database_name
        service: web
        resource_type: application
        attribute: name
      - setting: mysql/database_name
        service: master
        resource_type: application
        attribute: name
      - setting: wordpress/database/database_name
        service: web
        resource_type: application
        attribute: name
      - setting: wordpress/database/database_name
        service: master
        resource_type: application
        attribute: name
      - setting: mysql/password
        service: web
        resource_type: application
        attribute: password
      - setting: mysql/password
        service: master
        resource_type: application
        attribute: password
      - setting: mysql/username
        service: web
        resource_type: application
        attribute: name
      - setting: mysql/username
        service: master
        resource_type: application
        attribute: name
      - setting: wordpress/database/password
        service: web
        resource_type: application
        attribute: password
      - setting: wordpress/database/password
        service: master
        resource_type: application
        attribute: password
      - setting: wordpress/database/username
        service: web
        resource_type: application
        attribute: name
      - setting: wordpress/database/username
        service: master
        resource_type: application
        attribute: name
      - setting: wordpress/user/name
        service: web
        resource_type: application
        attribute: name
      - setting: wordpress/user/name
        service: master
        resource_type: application
        attribute: name
      - setting: wordpress/user/password
        service: web
        resource_type: application
        attribute: password
      - setting: wordpress/user/password
        service: master
        resource_type: application
        attribute: password
      - setting: wordpress/user/hash
        service: web
        resource_type: application
        attribute: hash
      - setting: wordpress/user/hash
        service: master
        resource_type: application
        attribute: hash
environment:
  description: This environment uses next-gen cloud servers.
  name: Next-Gen Open Cloud
  providers:
    chef-local:
      provides:
      - application: http
      - database: mysql
      - compute: mysql
      vendor: opscode
    load-balancer: {}
    nova: {}
    common:
      vendor: rackspace
inputs:
  blueprint:
    domain: wordpress.cldsrvr.com
    password: pULQxCxkIK
    region: DFW
    ssl_certificate: |
      -----BEGIN CERTIFICATE-----
      MIIDxjCCAq6gAwIBAgIJAMPPVAWqOFGIMA0GCSqGSIb3DQEBBQUAMIGWMQswCQYD
      VQQGEwJVUzELMAkGA1UECBMCVHgxFDASBgNVBAcTC1NhbiBBbnRvbmlvMRowGAYD
      VQQKExFBd2Vzb21lbmVzcywgSW5jLjEdMBsGA1UEAxMUbXlhd2Vzb21ld2Vic2l0
      ZS5jb20xKTAnBgkqhkiG9w0BCQEWGnN0dWZmQG15YXdlc29tZXdlYnNpdGUuY29t
      MB4XDTEyMDYxNTE0MDE0NloXDTIyMDYxMzE0MDE0NlowgZYxCzAJBgNVBAYTAlVT
      MQswCQYDVQQIEwJUeDEUMBIGA1UEBxMLU2FuIEFudG9uaW8xGjAYBgNVBAoTEUF3
      ZXNvbWVuZXNzLCBJbmMuMR0wGwYDVQQDExRteWF3ZXNvbWV3ZWJzaXRlLmNvbTEp
      MCcGCSqGSIb3DQEJARYac3R1ZmZAbXlhd2Vzb21ld2Vic2l0ZS5jb20wggEiMA0G
      CSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDKqXVCJkLHNJzlqKQ1GTh0nyFqbZik
      G5uMzzauBa1BtwCspziUqL1X/PNoGXOnSyEqp+zwtArci82o4PYJ9c8rYAzHZRtM
      mg+ZKR/8w/aO/AFuLfoGiqVLaWcexARR0fw3W9qB84KjBQ/bNAWbYLDle+tLdhep
      gmggbjTfSl8YzqHi7fBqLww+OSp9PYFJs02v6TIzNVZXw5TFTaedIuOaixz5dsaj
      uWag9YX2Lb7Ysl5V07bp0Mvv4YGyVXtngigK2WuKwpMFbOZJRbYYT9LAK+XvJKUy
      85XcmxXTjTREmS6TS1nvJgFAu3uP1dpfkH9JzWtpXtsZ0cChFQL1+U1NAgMBAAGj
      FTATMBEGCWCGSAGG+EIBAQQEAwIGQDANBgkqhkiG9w0BAQUFAAOCAQEAqXZuiTPy
      +YRWkkE9DOWJmmnSsjLBrnh1YY0ZmNDMFM9xP6uRd/StAbwgIYxMS2Wo8ZtMkrNv
      naCBB6ghgQHaNJmx1j92SpS1U/WELcSKV01j9DnklFXbSH6n5fS/VsckTcmVOXoW
      wLgHXXd0aueqBTPpiKEjNfI7dUl+uUpbklb+RyN565hxjzrSDSuhSjZ/0GL61RVz
      4pY+rjEPNp3itHbR6weyWwNvi0xA8FYipwJYEiErN2zuhH1ikACrlBw9Fo/7hSmh
      Z3rujqhToCEbXsejLKjSKSzdVGEhgRHla+9+cEvnAYfWnIkAl1pVK3BH+5Bg4634
      FQOjVTygmZVlVw==
      -----END CERTIFICATE-----
    ssl_private_key: |
      -----BEGIN RSA PRIVATE KEY-----
      MIIEowIBAAKCAQEAyql1QiZCxzSc5aikNRk4dJ8ham2YpBubjM82rgWtQbcArKc4
      lKi9V/zzaBlzp0shKqfs8LQK3IvNqOD2CfXPK2AMx2UbTJoPmSkf/MP2jvwBbi36
      BoqlS2lnHsQEUdH8N1vagfOCowUP2zQFm2Cw5XvrS3YXqYJoIG4030pfGM6h4u3w
      ai8MPjkqfT2BSbNNr+kyMzVWV8OUxU2nnSLjmosc+XbGo7lmoPWF9i2+2LJeVdO2
      6dDL7+GBslV7Z4IoCtlrisKTBWzmSUW2GE/SwCvl7ySlMvOV3JsV0400RJkuk0tZ
      7yYBQLt7j9XaX5B/Sc1raV7bGdHAoRUC9flNTQIDAQABAoIBAE3RhgoRgQDXDgwN
      loghGBGH7R/d14fkZfVKt/dYjK+4IpUpXMuQg6weoCRv6X3qlmC3vH6s06LeN+lK
      AI/QiG1iY2XJSBNA8Q5hwTugz7MVx0LUerY6VMBBR+yDXhlA5XUoWx4dMCOC1RTZ
      w/FmzmZAEBiYzvsy7OLPDpRTDXMLbV3ULlC+TsKOHAGeSnJbLFrS7MMI4rs8d366
      lyz9pYy9VG2/NRFk+yLvO5vd2YKiPgWWCFWmxkULvRYC7pRU8Uye6iUh0Zn/LWQd
      0Rt38ZrMfVUoIm8ep8TjfwvZDO4MURy7mqAtqLRNyUJk1Rau23crbq5F6jCF0ukq
      MzLlguECgYEA+mzdUD4dic92V5+sP9LYM79DMVlRFLQ9nDJOK4hKukG9+KXSyk8T
      WEtLlJA/2LoDOBAPqq+3eg6l54YTq1RPgVOQxFAwIQHq1K2aBJEt1tyMA1eK3Kp/
      bsS8/jbr3V3C82q3E/Llsm0JCO/5cTCc59DC6xHZvWZ4YJRT7Fc+LHUCgYEAzyxl
      z81fgoaOglcEpVMcv+48EUANEoG06+WXLu9Juc7G9xuKe/QGvl3cAhx0zB+PwnKw
      SF9CXj3d5hCgnioNC8HZ6fO9IiYBqbrjmenrvdPBAbG4SSVZTChYSg44Kh6puSOB
      fZpDaW3poTl4YFFOSpijkukL/kWs5m7zpM4b4nkCgYBkL6d+0crpdllnBtdXlVev
      pCYSmSQJ/23ijnGdkuIqj+CbmGOzUl1v5nevUOJqJ0jgZfSOmcvyheezr30w/wLr
      v23cTCRlICo9udIzX42SNxvAvoYsb/2ZaBYgMgK8xiUXUys5TOS+NEb4D2Gg+gzb
      5TYF61dMIbGpGc5VcDXMfQKBgDId/WsttYMv5d2mC1urJXNQwHsz0XW+pvPCELar
      8Fvgp8UzhmbB+7eloQlptN+EaxSRBhAb60Q9FycGsrRQW+OSO5MbAY/3PcO/kDu1
      mO/NAA3W3kvjmxyPTfxsQC4ASPKeoj6uSMyCaFg2POagBJ6LGlb5xYr3dAIyqQIf
      UiORAoGBAN79cXdQBL6XJIFuy43QzcT37IDihxJ3sGOBPf4nOCealOHxA/iRgYim
      N7YE6SrkAPPZdG3L9U7LOCfchUiIbSvQFXReukewn6714N4QMYY0Dz+1NBwXD/w1
      8j3jDF3oufViQELOIrmjxtZbBazVffOTpgYiepnP8Ns7U5WGijhF
      -----END RSA PRIVATE KEY-----
    username: wp_user
    web_server_count: 1
    web_server_protocol: http_and_https
    server_size: 1024"""
