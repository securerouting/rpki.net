# $Id$

import POW, POW.pkix, base64, rpki.ipaddrs, rpki.resource_set

Alice_EE = """
MIIDGDCCAgCgAwIBAgIJANkdU8+R7K3dMA0GCSqGSIb3DQEBBQUAMCQxIjAgBgNV
BAMTGVRlc3QgQ2VydGlmaWNhdGUgQWxpY2UgQ0EwHhcNMDcwNjE5MTk1MzE4WhcN
MDcwNzE5MTk1MzE4WjAkMSIwIAYDVQQDExlUZXN0IENlcnRpZmljYXRlIEFsaWNl
IEVFMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzxuYZsSzM7J4D/GN
TiSB/EzRF7U91bYIoqZHG/NcLePFJfHKvKd7LuRNXI4WXrUjQ+6VlcQGdPfo6uvZ
9r/UKocS3ATc7p28CkMNM99RcLM4OWg70021MwmS04CaMpUftsQCtSwAVrWkL3dM
C9LuMdChA619q1x56RGrBeqgnk9NfHahUjmqjhUVQejTk2fYfLcINdxUwOQP9GT5
bQLhf5hxq+QsixyBjB0BE/h1KxCRJITu5JLzCZIxHxMeN/MdDz3T0m1Vhwd7KZZS
H1Iq5WIBArhzuLQsekSL4GmDLXSxuLi68w8W53YEpc4hRzS29+p1mMK5bZMttvYN
hfoVOQIDAQABo00wSzAJBgNVHRMEAjAAMB0GA1UdDgQWBBTDNm3cT2DjtkzqsI7N
hTSoXmbGsDAfBgNVHSMEGDAWgBRqTejqD9pJQzENNALChYOBrglzEzANBgkqhkiG
9w0BAQUFAAOCAQEAZac7WWRWCItjea9O6YJgB1EUy0NdN7rRuzQSJg9LQfsevwJK
s2R/gV6RF8c53BnexUoVOu5VxSFZin9qRMMZxEMzo3TlFY2JuhPchLFrnYQ5SsjL
w25iLY9xaswZoaAdu4HG5IbN+Drew4Hlfqfoqgi1x79MbL4i+xdPjrHjV+5T/bLE
hADax/Ki7qWOMW2eMWIYuhyHwlqaJaa4xvgSuBdzccPur9nYuYyMQhR5FEtiBrFk
H+SG3DPUYnJjHo/0hqZ+cRRtoNJO00gfgzDUYGIrDak4aGapJsGcJ5/6xIvYKrpu
mkmvYl9m3IB1QYSAtu+0C98ShPgIFNqLvWOceA==
"""

APNIC_Root = """
MIIHMjCCBhqgAwIBAgIBcjANBgkqhkiG9w0BAQsFADBNMS4wLAYDVQQDEyVEZW1v
IEFQTklDIFJPT1QgQ0EgLSBOb3QgZm9yIHJlYWwgdXNlMRswGQYJKoZIhvcNAQkB
FgxjYUBhcG5pYy5uZXQwHhcNMDYxMTE2MDU1MDEwWhcNMDcxMTE2MDU1MDEwWjA2
MTQwMgYDVQQDEytEZW1vIFByb2R1Y3Rpb24gQVBOSUMgQ0EgLSBOb3QgZm9yIHJl
YWwgdXNlMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA64tZcEhcMvdF
s0sXVF+op473Px/0ANRBHKl772wzTIBno6I4+RNmh8zkasTh6aKhNwcpkc03AaTs
cFmPrlq5PREyZrO1vzq6McShEH5/FcVLUcHKKq46/f+0mx7ec/ExaeRljHJeIVxJ
TuKUrs87PbPYBz+KI6bjb4e0ICsVgomat6DphPPd3krCBJVNqBD6W2UCv1huK9Kx
6egiWaqAYzcrI3W0TFNA5+RUnjnybB0qg1pOkdgKDOEFnIkl0MnX4ENSWNOnezHF
myV3ypJ+42Zllu5OZacqbPh+UJzHv4rMdfKjwpvn1ofiqglYG74HY2lzXSUyYPuA
cZX9572A9wIDAQABo4IEMjCCBC4wDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8E
BAMCAQYwHQYDVR0OBBYEFKuuiK1khrgRO46sfDwFBwJRwqkcMB8GA1UdIwQYMBaA
FKb6Y78FHkIsdnueF/Hxm4ZnWDKNMBgGA1UdIAEB/wQOMAwwCgYIKwYBBQUHDgIw
PQYDVR0fBDYwNDAyoDCgLoYscnN5bmM6Ly9yZXBvc2l0b3J5LmFwbmljLm5ldC9B
UE5JQy9BUE5JQy5jcmwwTwYIKwYBBQUHAQEEQzBBMD8GCCsGAQUFBzAChjNyc3lu
YzovL3JlcG9zaXRvcnkuYXBuaWMubmV0L1RSVVNUQU5DSE9SUy9hcG5pYy5jZXIw
WwYIKwYBBQUHAQsETzBNMEsGCCsGAQUFBzAFhj9yc3luYzovL3JlcG9zaXRvcnku
YXBuaWMubmV0L0FQTklDL3E2NklyV1NHdUJFN2pxeDhQQVVIQWxIQ3FSdy8wggJF
BggrBgEFBQcBCAEB/wSCAjQwggIwoIICLDCCAigCAgCtAgICqQICBMUCAgTRAgIE
1QICBOICAgZ7AgIGqDAIAgIG6AICBukCAgb1AgIHOwICB/oCAghgAgIJUTAIAgIJ
wQICCeACAgnpAgIJ+gICCgMwCAICCgkCAgoKAgIKiQICCpICAgqZAgIKxAICCswC
AgrUAgILBwICC1sCAgtjMAgCAgttAgILbgICDR0CAg0jAgINNgICDT8CAg1DAgIN
hAICDYYCAg2gAgINtgICDd4wCAICDeYCAg3nAgIN/wICDhUCAg4YMAgCAg5NAgIO
TjAIAgIOaQICDm0CAg5/AgIOhTAIAgIOowICDqQwCAICDq0CAg6uAgIOvQICDr8C
Ag7IMAgCAg7KAgIOywICDuUCAg7xAgIO/DAIAgIO/wICDwACAg9ZAgIPgQICD4gC
Ag+nAgIPyAICD9ECAg/aAgIP3AICECYCAhAuAgIQPjAIAgIQTgICEE8CAhBlAgIQ
agICEJsCAhCyAgIRADAIAgIRHQICER4CAhFPMAgCAhFRAgIRUgICEaMCAhGwAgIR
ugICEfICAhH9MAgCAhIAAgITAAICE2EwCAICE5kCAhOaAgITuwICE90CAhPfAgIW
TQICF7QCAhgTAgIYdgICGdsCAhn4AgIb2wICHAcwCAICHSsCAh4qAgIerwICHt0w
CAICJAACAif/AgIqNwICLMswCAICRAACAkf/AgJM+TAIAgJcAAICX/8wCgIDAJQA
AgMAl/8wewYIKwYBBQUHAQcBAf8EbDBqMDQEAgABMC4wCAMCAToDAgE8MAgDAgB5
AwIAfgMCAJYDAgCjAwIBygMCAdIwCAMCAdoDAgDeMDIEAgACMCwDBAEgAQIDBAIg
AQwDBAEgAUQwDAMEByABgAMEBCABoDAKAwICJAMEAyQAQDANBgkqhkiG9w0BAQsF
AAOCAQEAxjUMY1cBdWUXWmPOwK6zk8E7BOVR3U7U62AfYqlE75cjt2RhRQBcc0XP
tEG8rl6DJMmzH6XB0+czrsUijeBdRBeC+WTMbJd1ZMzgqrqHgXI0CjdjPMR0k6Dx
qpsdDXmlIuAIUHy/GISIel9N/eXSu8ctsWXV2YYlaf7WVGHIhmJs03iSu324vJSk
vhlLtNxdV+neQhkXT54mrx7mADxWYz5+rjWFvJuiOfQicXJI4uh5oAN8POcfx4hu
7xYYqCunudhilCEz53CCcjzCAx5pW1jl32YdguWEwTf6ttwTnTsXQ0a+waMk4ljw
uMsR5Xzvy12ti/m+7MSTLR1kMxJOFA==
"""

alice = base64.b64decode(Alice_EE)
apnic = base64.b64decode(APNIC_Root)

verbose = True

for der in (alice, apnic):
  print POW.derRead(POW.X509_CERTIFICATE, der).pprint()
  cert = POW.pkix.Certificate()
  cert.fromString(der)
  if verbose:
    for oid, crit, val in cert.getExtensions():
      print "  OID: ", oid, POW.pkix.oid2obj(oid)
      print "  Val:", val
      print
  if False:
    val = [x[2] for x in cert.getExtensions() if x[0] == POW.pkix.obj2oid("sbgp-ipAddrBlock")]
    if val:
      for fam in val[0]:
        afi = (ord(fam[0][0]) << 8) + ord(fam[0][1])
        addrlen = { 1 : 32, 2 : 128 }[afi]
        addrtype = { 1 :  rpki.ipaddrs.v4addr, 2 : rpki.ipaddrs.v6addr }[afi]
        if len(fam[0]) > 2:
          safi = ord(fam[0][2])
        else:
          safi = None
        if fam[1][0] == 'inherit':
          vals = None
        else:
          vals = []
          for aor in fam[1][1]:
            def b2l(x, y): return (x << 1) | y
            if aor[0] == 'addressRange':
              min = reduce(b2l, aor[1][0], 0L)
              max = reduce(b2l, aor[1][1], 0L)
              min <<= addrlen - len(aor[1][0])
              max <<= addrlen - len(aor[1][1])
              max |= (1 << (addrlen - len(aor[1][1]))) - 1
              min = addrtype(min)
              max = addrtype(max)
              txt = "%s-%s" % (min, max)
              vals.append((txt, min, max))
            else:
              prefix = reduce(b2l, aor[1], 0L)
              prefix <<= addrlen - len(aor[1])
              prefixlen = len(aor[1])
              prefix = addrtype(prefix)
              txt = "%s/%d" % (prefix, prefixlen)
              vals.append((txt, prefix, prefixlen))
        print afi, safi, vals
  else:
    rs = rpki.resource_set.parse_extensions(cert.getExtensions())
    print rs
