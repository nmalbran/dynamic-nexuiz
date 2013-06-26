#!/usr/bin/python
import os
import socket
from optparse import OptionParser
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
NEXUIZ_ROOT = os.path.join(ROOT, 'Nexuiz')
TEAMTALK_ROOT = os.path.join(ROOT, 'teamtalk')

DEFAULT_GAMETYPE = 'ctf'
DEFAULT_MINPLAYERS = 8
DEFAULT_MAPS_URL = ':8080/maps/'

DEFAULT_HFS_EXE = os.path.join(ROOT, 'hfs.exe')
DEFAULT_TEAMTALKD = os.path.join(TEAMTALK_ROOT, 'teamtalkd')
DEFAULT_TEAMTALK_CONFIG_FILENAME = os.path.join(TEAMTALK_ROOT, 'tt4svc.xml')
DEFAULT_NEXUIZ_SERVER = 'nexuiz-linux-x86_64-dedicated' 


class DynamicConfigWriter:

	def __init__(self, gametype, minplayers, teamtalk_config_filename, url, nexuiz_folder):
		self.nexuiz_config_filename = "00_server_%s.cfg" % gametype
		self.full_nexuiz_config_filename = os.path.join(nexuiz_folder, 'data', self.nexuiz_config_filename)

		self.teamtalk_config_filename = teamtalk_config_filename

		self.ip = self._get_ip()
		self.minplayers = minplayers
		self.url = url
		self.print_conf()

	def get_nexuiz_config_filename(self):
		return self.nexuiz_config_filename

	def print_conf(self):
		print "Local IP is:", self.ip
		print "minplayers:", self.minplayers
		print "config file:", self.nexuiz_config_filename
		print "url:", self.url
		print ""

	def update_config(self):
		print "Updating Nexuiz Config"
		self.update_nexuiz_config()
		print "Done\n"
		print "Updating Teamtalk Config"
		self.update_teamtalk_config()
		print "Done\n"

	def _get_ip(self):
	    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	    try:
	        s.connect(('google.com', 9))
	        ip = s.getsockname()[0]
	    except socket.error:
	        ip = socket.gethostbyname(socket.gethostname())
	    finally:
	        del s
	    return ip

	def update_nexuiz_config(self):
	    target_file = open(self.full_nexuiz_config_filename, 'w')
	    for line in open(self.full_nexuiz_config_filename + '.base'):

	        if line.startswith('sv_curl_defaulturl http://'):
	            line = 'sv_curl_defaulturl http://%s%s\n' % (self.ip, self.url)

	        elif line.startswith('minplayers'):
	        	line = 'minplayers %d\n' % self.minplayers

	        target_file.write(line)

	    target_file.close()

	def update_teamtalk_config(self):
	    target_file = open(self.teamtalk_config_filename, 'w')
	    for line in open(self.teamtalk_config_filename + '.base'):
	        if line.startswith('        <bind-ip>'):
	            line = '        <bind-ip>%s</bind-ip>\n' % self.ip

	        target_file.write(line)

	    target_file.close()



def main():
	parser = OptionParser()
	parser.add_option('-t', '--gametype', help="Tipo de juego [ctf|dm]", choices=['ctf', 'dm'], default=DEFAULT_GAMETYPE)
	parser.add_option('-n', '--minplayers', type="int", help="Numero de min players", default=DEFAULT_MINPLAYERS)
	parser.add_option('--url', help="Url para los mapas", default=DEFAULT_MAPS_URL)

	parser.add_option('-l', '--launch', action="store_true", help="Levantar los servidor: HFS, Teamtalk y Nexuiz (en linux)", default=False)

	parser.add_option('--hfs', help="Ejecutable del HFS", default=DEFAULT_HFS_EXE)
	parser.add_option('--teamtalk', help="Ejecutable del teamtalk server", default=DEFAULT_TEAMTALKD)
	parser.add_option('--ttconfig', help="Archivo de configuracion del Team Talk Server", default=DEFAULT_TEAMTALK_CONFIG_FILENAME)
	parser.add_option('--nexuiz', help="Ejecutable del servidor de Nexuiz", default=DEFAULT_NEXUIZ_SERVER)
	parser.add_option('--nexuiz_folder', help="Carpeta donde esta Nexuiz", default=NEXUIZ_ROOT)


	(options, args) = parser.parse_args()

	dcw = DynamicConfigWriter(gametype=options.gametype,
							  minplayers=options.minplayers,
							  teamtalk_config_filename=options.ttconfig,
							  nexuiz_folder=options.nexuiz_folder,
							  url=options.url)
	dcw.update_config()

	print "Nexuiz Folder: %s" % options.nexuiz_folder
	print "Nexuiz: %s" % options.nexuiz
	print "HFS.exe: %s" % options.hfs
	print "Teamtalkd: %s" % options.teamtalk
	print "Teamtalk config: %s" % options.ttconfig
	print ""

	if options.launch:
		print "Launching HFS"
		os.system('wine %s &' % options.hfs)
		print "Done"

		print "Launching TeamTalk"
		os.system('%s -nd -c %s &' % (options.teamtalk, options.ttconfig))
		print "Done"

		print "Launching Nexuiz Server"
		full_nexuiz = os.path.join(options.nexuiz_folder, options.nexuiz)
		os.chdir(options.nexuiz_folder)
		os.system('%s +serverconfig %s' % (full_nexuiz, dcw.get_nexuiz_config_filename()))


if __name__ == '__main__':
	main()