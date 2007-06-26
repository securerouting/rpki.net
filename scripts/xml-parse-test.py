# $Id$

import base64
import glob
import os
import re
import socket
import xml.sax

def relaxng(xml, rng):
  i, o = os.popen4(("xmllint", "--noout", "--relaxng", rng, "-"))
  i.write(xml)
  i.close()
  v = o.read()
  o.close()
  return v

class rpki_updown_as_set(object):

  def __init__(self, s):
    self.as_set = []
    if s != "":
      vec = s.split(",")
      for elt in vec:
        r = re.match("^([0-9]+)-([0-9]+)$", elt)
        if r:
          b, e = r.groups()
          self.as_set.append((long(b), long(e)))
        else:
          self.as_set.append((long(elt), ))
      self.as_set.sort()

  def __str__(self):
    vec = []
    for elt in self.as_set:
      if len(elt) == 1:
        vec.append(str(elt[0]))
      else:
        vec.append(str(elt[0]) + "-" + str(elt[1]))
    return ",".join(vec)

class rpki_updown_ipv4_set(object):

  def __init__(self, s):
    self.ipv4_set = []
    if s != "":
      vec = s.split(",")
      for elt in vec:
        r = re.match("^([0-9.]+)-([0-9.]+)$", elt)
        if r:
          b, e = r.groups()
          self.ipv4_set.append((socket.inet_pton(socket.AF_INET, b), socket.inet_pton(socket.AF_INET, e)))
          continue
        r = re.match("^([0-9.]+)/([0-9]+)$", elt)
        if r:
          i, p = r.groups()
          self.ipv4_set.append((socket.inet_pton(socket.AF_INET, i), int(p)))
          continue
        self.ipv4_set.append((socket.inet_pton(socket.AF_INET, elt), ))
      self.ipv4_set.sort()

  def __str__(self):
    vec = []
    for elt in self.ipv4_set:
      if len(elt) == 1:
        vec.append(socket.inet_ntop(socket.AF_INET, elt[0]))
      elif isinstance(elt[1], int):
        vec.append(socket.inet_ntop(socket.AF_INET, elt[0]) + "/" + str(elt[1]))
      else:
        vec.append(socket.inet_ntop(socket.AF_INET, elt[0]) + "-" + socket.inet_ntop(socket.AF_INET, elt[1]))
    return ",".join(vec)

class rpki_updown_ipv6_set(object):

  def __init__(self, s):
    self.ipv6_set = []
    if s != "":
      vec = s.split(",")
      for elt in vec:
        r = re.match("^([0-9:a-fA-F]+)-([0-9:a-fA-F]+)$", elt)
        if r:
          b, e = r.groups()
          self.ipv6_set.append((socket.inet_pton(socket.AF_INET6, b), socket.inet_pton(socket.AF_INET6, e)))
          continue
        r = re.match("^([0-9:a-fA-F]+)/([0-9]+)$", elt)
        if r:
          i, p = r.groups()
          self.ipv6_set.append((socket.inet_pton(socket.AF_INET6, i), int(p)))
          continue
        self.ipv6_set.append((socket.inet_pton(socket.AF_INET6, elt), ))
      self.ipv6_set.sort()

  def __str__(self):
    vec = []
    for elt in self.ipv6_set:
      if len(elt) == 1:
        vec.append(socket.inet_ntop(socket.AF_INET6, elt[0]))
      elif isinstance(elt[1], int):
        vec.append(socket.inet_ntop(socket.AF_INET6, elt[0]) + "/" + str(elt[1]))
      else:
        vec.append(socket.inet_ntop(socket.AF_INET6, elt[0]) + "-" + socket.inet_ntop(socket.AF_INET6, elt[1]))
    return ",".join(vec)

class rpki_updown_msg(object):

  def toXML(self):
    return ('\
<?xml version="1.0" encoding="UTF-8"?>\n\
<message xmlns="http://www.apnic.net/specs/rescerts/up-down/"\n\
         version="1"\n\
         sender="%s"\n\
         recipient="%s"\n\
         msg_ref="%d"\n\
         type="%s">\n' \
            % (self.sender, self.recipient, self.msg_ref, self.type)
            ) + self.innerToXML() + "</message>\n"

  def innerToXML(self):
    return ""

  def startElement(self, name, attrs): pass

  def endElement(self, name, text): pass

class rpki_updown_cert(object):

  def __init__(self, attrs):
    self.cert_url = attrs.getValue("cert_url")
    self.cert_ski = attrs.getValue("cert_ski")
    self.cert_aki = attrs.getValue("cert_aki")
    self.cert_serial = attrs.getValue("cert_serial")
    self.resource_set_as = rpki_updown_as_set(attrs.getValue("resource_set_as"))
    self.resource_set_ipv4 = rpki_updown_ipv4_set(attrs.getValue("resource_set_ipv4"))
    self.resource_set_ipv6 = rpki_updown_ipv6_set(attrs.getValue("resource_set_ipv6"))
    try:
      self.req_resource_set_as = rpki_updown_as_set(attrs.getValue("req_resource_set_as"))
    except KeyError:
      self.req_resource_set_as = None
    try:
      self.req_resource_set_ipv4 = rpki_updown_ipv4_set(attrs.getValue("req_resource_set_ipv4"))
    except KeyError:
      self.req_resource_set_ipv4 = None
    try:
      self.req_resource_set_ipv6 = rpki_updown_ipv6_set(attrs.getValue("req_resource_set_ipv6"))
    except KeyError:
      self.req_resource_set_ipv6 = None
    self.status = attrs.getValue("status")

  def toXML(self):
    xml = ('\
    <certificate cert_url="%s"\n\
                 cert_ski="%s"\n\
                 cert_aki="%s"\n\
                 cert_serial="%s"\n\
                 resource_set_as="%s"\n\
                 resource_set_ipv4="%s"\n\
                 resource_set_ipv6="%s"\n' \
           % (self.cert_url, self.cert_ski, self.cert_aki, self.cert_serial,
              self.resource_set_as, self.resource_set_ipv4, self.resource_set_ipv6))
    if self.req_resource_set_as:
      xml += ('                 req_resource_set_as="%s"\n' % self.req_resource_set_as)
    if self.req_resource_set_ipv4:
      xml += ('                 req_resource_set_ipv4="%s"\n' % self.req_resource_set_ipv4)
    if self.req_resource_set_ipv6:
      xml += ('                 req_resource_set_ipv6="%s"\n' % self.req_resource_set_ipv6)
    xml += ('                 status="%s">' % self.status)
    xml += base64.b64encode(self.cert) + "</certificate>\n"
    return xml

class rpki_updown_class(object):

  def __init__(self, attrs):
    self.class_name = attrs.getValue("class_name")
    self.cert_url = attrs.getValue("cert_url")
    self.cert_ski = attrs.getValue("cert_ski")
    self.resource_set_as = rpki_updown_as_set(attrs.getValue("resource_set_as"))
    self.resource_set_ipv4 = rpki_updown_ipv4_set(attrs.getValue("resource_set_ipv4"))
    self.resource_set_ipv6 = rpki_updown_ipv6_set(attrs.getValue("resource_set_ipv6"))
    try:
      self.suggested_sia_head = attrs.getValue("suggested_sia_head")
    except KeyError:
      self.suggested_sia_head = None
    self.certs = []

  def toXML(self):
    xml = ('\
  <class class_name="%s"\n\
         cert_url="%s"\n\
         cert_ski="%s"\n\
         resource_set_as="%s"\n\
         resource_set_ipv4="%s"\n\
         resource_set_ipv6="%s"' \
           % (self.class_name, self.cert_url, self.cert_ski,
              self.resource_set_as, self.resource_set_ipv4, self.resource_set_ipv6))
    if self.suggested_sia_head:
      xml += ('\n         suggested_sia_head="%s"' % (self.suggested_sia_head))
    xml += ">\n"
    for cert in self.certs:
      xml += cert.toXML()
    xml += "    <issuer>" + base64.b64encode(self.issuer) + "</issuer>\n  </class>\n"
    return xml

class rpki_updown_list(rpki_updown_msg):

  def __str__(self):
    return "RPKI list request"

class rpki_updown_list_response(rpki_updown_msg):

  def __init__(self):
    self.resource_classes = []

  def startElement(self, name, attrs):
    if name == "class":
      self.resource_classes.append(rpki_updown_class(attrs))
    elif name == "certificate":
      self.resource_classes[-1].certs.append(rpki_updown_cert(attrs))

  def endElement(self, name, text):
    if name == "certificate":
      self.resource_classes[-1].certs[-1].cert = base64.b64decode(text)
    elif name == "issuer":
      self.resource_classes[-1].issuer = base64.b64decode(text)

  def innerToXML(self):
    xml = ""
    for c in self.resource_classes:
      xml += c.toXML()
    return xml

class rpki_updown_issue(rpki_updown_msg):

  def startElement(self, name, attrs):
    assert name == "request"
    self.class_name = attrs.getValue("class_name")
    try:
      self.req_resource_set_as = rpki_updown_as_set(attrs.getValue("req_resource_set_as"))
    except KeyError:
      self.req_resource_set_as = None
    try:
      self.req_resource_set_ipv4 = rpki_updown_ipv4_set(attrs.getValue("req_resource_set_ipv4"))
    except KeyError:
      self.req_resource_set_ipv4 = None
    try:
      self.req_resource_set_ipv6 = rpki_updown_ipv6_set(attrs.getValue("req_resource_set_ipv6"))
    except KeyError:
      self.req_resource_set_ipv6 = None

  def endElement(self, name, text):
    assert name == "request"
    self.pkcs10 = base64.b64decode(text)

  def innerToXML(self):
    xml = ('  <request class_name="%s"' % self.class_name)
    if self.req_resource_set_as:
      xml += ('\n           req_resource_set_as="%s"' % self.req_resource_set_as)
    if self.req_resource_set_ipv4:
      xml += ('\n           req_resource_set_ipv4="%s"' % self.req_resource_set_ipv4)
    if self.req_resource_set_ipv6:
      xml += ('\n           req_resource_set_ipv6="%s"' % self.req_resource_set_ipv6)
    return xml + ">" + base64.b64encode(self.pkcs10) + "</request>\n"

class rpki_updown_issue_response(rpki_updown_list_response):

  def innerToXML(self):
    assert len(self.resource_classes) == 1
    return rpki_updown_list_response.innerToXML(self)

class rpki_updown_revoke(rpki_updown_msg):

  def __str__(self):
    return 'RPKI %s class_name %s ski %s' % (self.type, self.class_name, self.ski)

  def startElement(self, name, attrs):
    self.class_name = attrs.getValue("class_name")
    self.ski = attrs.getValue("ski")

  def innerToXML(self):
    return ('  <key class_name="%s" ski="%s" />\n' % (self.class_name, self.ski))

class rpki_updown_revoke_response(rpki_updown_revoke): pass

class rpki_updown_error_response(rpki_updown_msg):

  def __str__(self):
    return "RPKI error %d" % (self.status)

  def innerToXML(self):
    return '  <status>%d</status>\n' % self.status

  def endElement(self, name, text):
    if name == "status":
      self.status = int(text)
    elif name == "last_message_processed":
      self.last_message_processed = text
    elif name == "description":
      self.description = text

class rpki_updown_sax_handler(xml.sax.handler.ContentHandler):

  def __init__(self):
    self.text = ""
    self.obj = None

  def startElementNS(self, name, qname, attrs):
    return self.startElement(name[1], attrs)

  def endElementNS(self, name, qname):
    return self.endElement(name[1])

  def startElement(self, name, attrs):
    if name == "message":
      assert int(attrs.getValue("version")) == 1
      type = attrs.getValue("type")
      if self.obj == None:
        self.obj = {
          "list"                  : rpki_updown_list(),
          "list_response"         : rpki_updown_list_response(),
          "issue"                 : rpki_updown_issue(),
          "issue_response"        : rpki_updown_issue_response(),
          "revoke"                : rpki_updown_revoke(),
          "revoke_response"       : rpki_updown_revoke_response(),
          "error_response"        : rpki_updown_error_response()
        }[type]
      assert self.obj != None
      self.obj.type = type
      self.obj.sender = attrs.getValue("sender")
      self.obj.recipient = attrs.getValue("recipient")
      self.obj.msg_ref = int(attrs.getValue("msg_ref"))
    else:
      assert self.obj != None
      self.obj.startElement(name, attrs)

  def characters(self, content):
    self.text += content

  def endElement(self, name):
    assert self.obj != None
    if name != "message":
      self.obj.endElement(name, self.text)
    self.text = ""

files = glob.glob("up-down-protocol-samples/*.xml")
files.sort()
for f in files:
# try:

    handler = rpki_updown_sax_handler()

#   parser = xml.sax.make_parser()
#   parser.setContentHandler(handler)
#   parser.parse(f)

    fh = open(f, "r")
    x = fh.read()
    fh.close()
    xml.sax.parseString(x, handler)

    obj = handler.obj
    print "-- " + str(obj) + "\n"
    x = obj.toXML()
    print x
    print relaxng(x, "up-down-medium-schema.rng")

# except Exception, err:
#   print "? " + str(err) + "\n"
