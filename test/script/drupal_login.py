#! /usr/bin/env python

import json
import re
import requests
import sys


class DrupalInteraction(object):
    def __init__(self, ip, domain="example.com",
                 login_id="admin", password=""):
        self.ip = ip
        self.domain = domain
        self.login_id = login_id
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({"Host": self.domain[7:-1]})

    def get_login_page(self):
        url = "http://{}".format(self.ip)
        r = self.session.get(url)
        return r.text

    def drupal_post_login(self):
        url = 'http://{}/?q=node&destination=node'.format(self.ip)
        print "url is {}".format(url)
        data = {"name": self.login_id,
                "pass": self.password,
                "form_id": "user_login_block",
                "form_build_id": "",
                "op": "Log in" }
        print json.dumps(data, indent=4)
        r = self.session.post(url, data=data, allow_redirects=False)
        if r.is_redirect:
            redirected_url = r.headers.get('location')
            r = self.session.get(re.sub(self.domain, "http://" + self.ip + "/", redirected_url))
        print "status code is {}".format(r.status_code)
        return r.text

    def login_successful(self):
        content = self.drupal_post_login()
        return "Dashboard" in content


if __name__ == "__main__":
    print json.dumps(sys.argv)
    ip = sys.argv[1]
    domain = sys.argv[2]
    login_id = sys.argv[3]
    password = sys.argv[4]
    drupal = DrupalInteraction(ip, domain=domain, login_id=login_id, password=password)

    if drupal.login_successful():
        print "Drupal login successful."
        sys.exit(0)
    else:
        print "login failed :("
        sys.exit(1)
