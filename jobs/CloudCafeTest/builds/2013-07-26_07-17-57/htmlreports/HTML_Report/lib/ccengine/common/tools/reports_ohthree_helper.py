import requests
from HTMLParser import HTMLParser


class CustomHtmlParser(HTMLParser):
    '''
    @summary: Custom Html Parser to parse for error link
    and the stack trace from reports.ohthree.com
    '''
    def __init__(self):
        HTMLParser.__init__(self)
        self.error_flag = False
        self.stack_flag = False
        self.error_link = ""
        self.exception_trace = ""

    def handle_starttag(self, tag, attrs):
        '''HTMLParser is a SAX parser so it is upto this class
        to keep the context of the elements.
        1) Look for the <div> element and if the class atrribute of div
        is equal to "alert alert-error" then set the flag to True
        2) The href from next <a> (link) element found after the div found
        above is then stored in the self.error_link variable
        '''
        if tag == "div" and attrs[0][1] == "alert alert-error":
            self.error_flag = True
        elif tag == 'a' and self.error_flag and attrs[0][0] == 'href':
            self.error_flag = False
            self.error_link = attrs[0][1]
        #Parsing for <pre> tag for the stack trace in error page
        elif tag == 'pre':
            self.stack_flag = True

    def  handle_data(self, data):
        if self.stack_flag:
            self.exception_trace = data
            self.stack_flag = False


class ReportsOhThreeHelper():

    def __init__(self, env):
        self.base_url = 'http://reports.ohthree.com'
        self.environment_name = env

    def _parse_html_for_link_to_server_error_page(self, html_resp):
        parser = CustomHtmlParser()
        parser.feed(html_resp)
        parser.close()
        return parser.error_link

    def _parse_html_for_server_error_stack_trace(self, body):
        body = body.replace('<br>', '\n')
        parser = CustomHtmlParser()
        parser.feed(body)
        parser.close
        return parser.exception_trace

    def get_server_build_error(self , server_id):
        url = self.base_url + '/%s/instance/%s' % (self.environment_name, server_id)
        http_response = requests.get(url)
        error_link = self._parse_html_for_link_to_server_error_page(http_response.content)
        error_link_response = requests.get('%s%s' % (self.base_url, error_link))
        return self._parse_html_for_server_error_stack_trace(error_link_response.content)
