#!/usr/bin/env python
# Script to pull down RPMs from an online repo, then
# unpack via the rpm2cpio mechanism.

import urllib.request
import shutil
import subprocess
import os, os.path

def fix_links():
	for dirpath, dirnames, filenames in os.walk(os.getcwd()):
		for i in filenames:
			test_relpath = os.path.join(dirpath, name)
			test_fullpath = os.getcwd() + test_relpath
			if os.path.islink(test_fullpath):
				target = os.readlink(test_relpath)
				new_path = os.path.relpath(target, start=dirpath)
				os.remove(test_relpath)
				os.symlink(test_fullpath, new_path)

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
	#a = subprocess.Popen('rpm2cpio', stdin = open(output_file, 'r'), stdout=subprocess.PIPE)
	#b = subprocess.Popen(['cpio', '-i', '--make-directories'], stdin=a.stdout, stdout=subprocess.PIPE)
	#a.stdout.close()
        #print(b.communicate()[0])
	subprocess.call('rpm2cpio < ' + output_file + ' | cpio -id', shell=True)

if __name__ == __main__:
	fix_links()

