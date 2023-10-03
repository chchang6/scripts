#!/usr/bin/env python
# Script to pull down RPMs from an online repo, then
# unpack via the rpm2cpio mechanism.

import urllib.request
import shutil
import subprocess
import os, os.path
import re

def fix_links():
	for dirpath, dirnames, filenames in os.walk(os.getcwd()):
		print(dirpath, dirnames, filenames)
		for name in filenames:
			test_fullpath = os.path.join(dirpath, name)
			if os.path.islink(test_fullpath):
				try: # Is link broken?
					os.stat(test_fullpath)
				except FileNotFoundError: # Yes
					print('Working on', test_fullpath)
					target = os.readlink(test_fullpath)
					new_path = get_relative_path(target,dirpath)
					print('new_path is', new_path)
					os.remove(test_fullpath)
					os.symlink(new_path, test_fullpath)

def get_relative_path(abs_old_target, abs_new_target):
	old_list = re.split('/', abs_old_target)[1:-1] # /usr/lib64 -> ['usr', 'lib64', 'test1']
	new_list = re.split('/', abs_new_target)[1:] # /a/b/usr/lib64 -> ['a', 'b', 'usr', 'lib64', 'test1']
	index = new_list.index(old_list[0])  # 2
	num_relpath_markers = len(new_list) - index  # 5 - 2 = 3
	new_list = ['..' for i in range(num_relpath_markers)]
	new_list.extend(old_list)
	return '/'.join(new_list)

def install_wine():
	URL = 'https://archive.fedoraproject.org/pub/epel/7/x86_64/Packages/w/'
	package_dict = {'':'x86_64', 'alsa':'x86_64', 'capi':'x86_64',
		'cms':'x86_64', 'common':'noarch', 'core':'x86_64',
		'courier-fonts':'noarch', 'desktop':'noarch', 'devel':'x86_64',
		'filesystem':'noarch','fixedsys-fonts':'noarch',
		'fonts':'noarch', 'ldap':'x86_64', 'marlett-fonts':'noarch',
		'ms-sans-serif-fonts':'noarch', 'openal':'x86_64',
		'pulseaudio':'x86_64', 'small-fonts':'noarch',
		'symbol-fonts':'noarch', 'system-fonts':'noarch', 'systemd':'noarch',
		'tahoma-fonts':'noarch', 'tahoma-fonts-system':'noarch',
		'twain':'x86_64',
		'wingdings-fonts':'noarch', 'wingdings-fonts-system':'noarch'}
	
	for i in package_dict:
		if i == '':
			target_filename = 'wine' + i + '-3.0-1.el7.' + package_dict[i] + '.rpm'
		else:
			target_filename = 'wine-' + i + '-3.0-1.el7.' + package_dict[i] + '.rpm'
		output_file = target_filename
		url = URL + target_filename
		with urllib.request.urlopen(url) as response, open(output_file, 'wb') as out_file:
			shutil.copyfileobj(response, out_file)
		out_file.close()
		_install_RPM(output_file)

def _install_RPM(filename):
	#a = subprocess.Popen('rpm2cpio', stdin = open(filename, 'r'), stdout=subprocess.PIPE)
	#b = subprocess.Popen(['cpio', '-i', '--make-directories'], stdin=a.stdout, stdout=subprocess.PIPE)
	#a.stdout.close()
        #print(b.communicate()[0])
	subprocess.call('rpm2cpio < ' + filename + ' | cpio -id', shell=True)

if __name__ == '__main__':
#	install_wine()
	fix_links()

