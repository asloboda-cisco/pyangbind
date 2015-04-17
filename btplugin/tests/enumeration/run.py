#!/usr/bin/env python

import os, sys, getopt

TESTNAME="enumeration"

# generate bindings in this folder

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "k", ["keepfiles"])
  except getopt.GetoptError as e:
    print str(e)
    sys.exit(127)

  k = False
  for o, a in opts:
    if o in ["-k", "--keepfiles"]:
      k = True

  this_dir = os.path.dirname(os.path.realpath(__file__))
  os.system("/usr/local/bin/pyang --plugindir /Users/rjs/Code/pyangbind/btplugin -f bt -o %s/bindings.py %s/%s.yang" % (this_dir, this_dir, TESTNAME))

  from bindings import enumeration
  t = enumeration()

  for e in ["e", "f"]:
    assert hasattr(t.container, e), "container does not contain enumeration %s" % e

  t.container.e = "one"
  assert t.container.e == "one", "enumeration value was not correctly set (%s)" % \
    t.container.e

  catch = False
  try:
    t.container.e = "twentyseven"
  except:
    catch = True
  assert catch == True, "erroneous value was not caught by restriction handler (%s)" % \
    t.container.e

  assert t.container.f._default == "c", "erroneous default value for 'f' (%s)" % \
    t.container.f._default

  t.container.e = "two"
  assert t.container.e.getValue(mapped=True) == 42, "erroneously statically defined value returned (%s)" % \
    t.container.e.getValue(mapped=True)

  if not k:
    os.system("/bin/rm %s/bindings.py" % this_dir)
    os.system("/bin/rm %s/bindings.pyc" % this_dir)

if __name__ == '__main__':
  main()
