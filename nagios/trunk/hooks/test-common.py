from common import ObjectTagCollection
import os

from tempfile import NamedTemporaryFile

""" This is meant to test the ObjectTagCollection bits. It should
    probably be made into a proper unit test. """

x = ObjectTagCollection('test-units')
y = ObjectTagCollection('test-relids')

o = NamedTemporaryFile(delete=False)
o2 = NamedTemporaryFile(delete=False)
o3 = NamedTemporaryFile(delete=True)
o.write('some content')
o.flush()

x.tag_object(o.name, 'box-9')
x.tag_object(o.name, 'nrpe-1')
y.tag_object(o.name, 'monitors:2')
x.tag_object(o2.name, 'box-10')
x.tag_object(o2.name, 'nrpe-2')
y.tag_object(o2.name, 'monitors:2')
x.tag_object(o3.name, 'other-0')
y.tag_object(o3.name, 'monitors:3')
x.untag_object(o.name, 'box-9')
x.cleanup_untagged()

if not os.path.exists(o.name):
    raise RuntimeError(o.name)

x.kill_tag('nrpe-1')
x.cleanup_untagged()

if os.path.exists(o.name):
    raise RuntimeError(o.name)

if not os.path.exists(o2.name):
    raise RuntimeError(o2.name)

y.kill_tag('monitors:2')
y.cleanup_untagged(['monitors:1','monitors:3'])

if os.path.exists(o.name):
    raise RuntimeError(o2.name)

if os.path.exists(o2.name):
    raise RuntimeError(o2.name)

x.destroy()
