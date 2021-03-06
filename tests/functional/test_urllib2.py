# #!/usr/bin/env python
# -*- coding: utf-8 -*-

# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
import urllib2
from sure import *
from httpretty import HTTPretty

@within(two=microseconds)
def test_httpretty_should_mock_a_simple_get_with_urllib2_read():
    u"HTTPretty should mock a simple GET with urllib2.read()"

    HTTPretty.register_uri(HTTPretty.GET, "http://globo.com/",
                           body="The biggest portal in Brazil")

    fd = urllib2.urlopen('http://globo.com')
    got = fd.read()
    fd.close()

    assert that(got).equals('The biggest portal in Brazil')

@within(two=microseconds)
def test_httpretty_should_mock_headers_urllib2(now):
    u"HTTPretty should mock basic headers with urllib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           status=201)

    request = urllib2.urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    assert that(request.code).equals(201)
    assert that(headers).equals({
        'content-type': 'text/plain',
        'connection': 'close',
        'content-length': '35',
        'status': '201 Created',
        'server': 'Python/HTTPretty',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    })


@within(two=microseconds)
def test_httpretty_should_allow_adding_and_overwritting_urllib2(now):
    u"HTTPretty should allow adding and overwritting headers with urllib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           adding_headers={
                               'Server': 'Apache',
                               'Content-Length': '27',
                               'Content-Type': 'application/json',
                           })

    request = urllib2.urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    assert that(request.code).equals(200)
    assert that(headers).equals({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': '27',
        'status': '200 OK',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    })

@within(two=microseconds)
def test_httpretty_should_allow_forcing_headers_urllib2():
    u"HTTPretty should allow forcing headers with urllib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           forcing_headers={
                               'Content-Type': 'application/xml',
                           })

    request = urllib2.urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    assert that(headers).equals({
        'content-type': 'application/xml',
    })


@within(two=microseconds)
def test_httpretty_should_allow_adding_and_overwritting_by_kwargs_u2(now):
    u"HTTPretty should allow adding and overwritting headers by keyword args " \
        "with urllib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           server='Apache',
                           content_length='23456789',
                           content_type='application/json')

    request = urllib2.urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    assert that(request.code).equals(200)
    assert that(headers).equals({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': '23456789',
        'status': '200 OK',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    })


@within(two=microseconds)
def test_httpretty_should_support_a_list_of_successive_responses_urllib2(now):
    u"HTTPretty should support adding a list of successive responses with urllib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/gabrielfalcao/httpretty",
                           responses=[
                               HTTPretty.Response(body="first response", status=201),
                               HTTPretty.Response(body='second and last response', status=202),
                            ])

    request1 = urllib2.urlopen('http://github.com/gabrielfalcao/httpretty')
    body1 = request1.read()
    request1.close()

    assert that(request1.code).equals(201)
    assert that(body1).equals('first response')

    request2 = urllib2.urlopen('http://github.com/gabrielfalcao/httpretty')
    body2 = request2.read()
    request2.close()
    assert that(request2.code).equals(202)
    assert that(body2).equals('second and last response')

    request3 = urllib2.urlopen('http://github.com/gabrielfalcao/httpretty')
    body3 = request3.read()
    request3.close()
    assert that(request3.code).equals(202)
    assert that(body3).equals('second and last response')
