"""By using execfile(this_file, dict(__file__=this_file)) you will
activate this virtualenv environment.
This can be used when you must use an existing Python interpreter, not
the virtualenv bin/python
"""

try:
    __file__
except NameError:
    raise AssertionError(
        "You must run this like execfile('/var/www/trans/venv/bin/active_this.py', dict(__file__='/var/www/trans/venv/bin/activate_this.py'))")
import sys
import os

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
site_packages = os.path.join(base, 'lib', 'python%s' % sys.version[:3], 'site-packages')
prev_sys_path = list(sys.path)
import site
site.addsitedir(site_packages)
sys.real_prefix = sys.prefix
sys.prefix = base
# Move the added items to the front of the path:
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path
