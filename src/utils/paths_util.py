import os.path as osp
import os
import sys


os_home = osp.expanduser("~")
cwd = os.getcwd()
path_to_doc = osp.join(os_home, str('Documents'))
output_dir = osp.join(path_to_doc, str('workloggerOutput'))
log_dir = osp.join(cwd, str('logs'))