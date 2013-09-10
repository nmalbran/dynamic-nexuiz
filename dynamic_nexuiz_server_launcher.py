#!/usr/bin/python
import os
import socket
from optparse import OptionParser
import subprocess
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
NEXUIZ_ROOT = os.path.join(ROOT, 'Nexuiz')
TEAMTALK_ROOT = os.path.join(ROOT, 'teamtalk')

DEFAULT_GAMETYPE = 'ctf'
DEFAULT_MINPLAYERS = 8
DEFAULT_MAPS_URL = ':8080/maps/'
DEFAULT_FRAGLIMIT = 15
DEFAULT_MESSAGE = "Welcome to SkyRyu Nexuiz Server"

DEFAULT_HFS_EXE = os.path.join(ROOT, 'hfs.exe')
DEFAULT_TEAMTALKD = os.path.join(TEAMTALK_ROOT, 'teamtalkd')
DEFAULT_TEAMTALK_CONFIG_FILENAME = os.path.join(TEAMTALK_ROOT, 'tt4svc.xml')
DEFAULT_NEXUIZ_SERVER = 'nexuiz-linux-686-dedicated'


class DynamicConfigWriter:

    def __init__(self, gametype, minplayers, teamtalk_config_filename, url, nexuiz_folder, fraglimit, message):
        self.nexuiz_config_filename = "00_server_%s.cfg" % gametype
        self.full_nexuiz_config_filename = os.path.join(nexuiz_folder, 'data', self.nexuiz_config_filename)

        self.teamtalk_config_filename = teamtalk_config_filename

        self.ip = self._get_ip()
        self.minplayers = minplayers
        self.url = url
        self.logfile = "%s-%s.log" % (self._get_time(), os.path.splitext(self.nexuiz_config_filename)[0])
        self.fraglimit = fraglimit
        self.message = message
        self.print_conf()

    def get_nexuiz_config_filename(self):
        return self.nexuiz_config_filename

    def print_conf(self):
        print "Local IP is:", self.ip
        print "minplayers:", self.minplayers
        print "fraglimit_override:", self.fraglimit
        print "config file:", self.nexuiz_config_filename
        print "url:", self.url
        print "logfile:", self.logfile
        print "welcome message:", self.message
        print ""

    def update_config(self):
        self.update_nexuiz_config()
        self.update_teamtalk_config()

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

    def _get_time(self):
        return time.strftime("%Y%m%d")

    def update_nexuiz_config(self):
        print "Updating Nexuiz Config"
        target_file = open(self.full_nexuiz_config_filename, 'w')
        for line in open(self.full_nexuiz_config_filename + '.base'):

            if line.startswith('sv_curl_defaulturl http://'):
                line = 'sv_curl_defaulturl http://%s%s\n' % (self.ip, self.url)

            elif line.startswith('minplayers'):
                line = 'minplayers %d\n' % self.minplayers

            elif line.startswith('log_file'):
                line = 'log_file "%s"\n' % self.logfile

            elif line.startswith('fraglimit_override'):
                line = 'fraglimit_override %d\n' % self.fraglimit

            elif line.startswith('sv_motd'):
                line = 'sv_motd "%s"\n' % self.message

            target_file.write(line)

        target_file.close()
        print "Done\n"

    def update_teamtalk_config(self):
        print "Updating Teamtalk Config"
        target_file = open(self.teamtalk_config_filename, 'w')
        for line in open(self.teamtalk_config_filename + '.base'):
            if line.startswith('        <bind-ip>'):
                line = '        <bind-ip>%s</bind-ip>\n' % self.ip

            target_file.write(line)

        target_file.close()
        print "Done\n"



def main():
    parser = OptionParser()
    parser.add_option('-t', '--gametype', help="Type of Game [ctf|dm]", choices=['ctf', 'dm'], default=DEFAULT_GAMETYPE)
    parser.add_option('-n', '--minplayers', type="int", help="Minimum number of players", default=DEFAULT_MINPLAYERS)
    parser.add_option('-k', '--fraglimit', type="int", help="Number of frags to end the game", default=DEFAULT_FRAGLIMIT)
    parser.add_option('--url', help="Url for maps downloading", default=DEFAULT_MAPS_URL)
    parser.add_option('-m', '--message', help="welcome message", default=DEFAULT_MESSAGE)

    parser.add_option('-l', '--launch', action="store_true", help="Launch the servers: HFS, Teamtalk and Nexuiz (on linux)", default=False)

    parser.add_option('--hfs', help="HFS executable by wine", default=DEFAULT_HFS_EXE)
    parser.add_option('--teamtalk', help="teamtalkd file", default=DEFAULT_TEAMTALKD)
    parser.add_option('--ttconfig', help="Configuration file for teamtalk server", default=DEFAULT_TEAMTALK_CONFIG_FILENAME)
    parser.add_option('--nexuiz', help="Nexuiz executable", default=DEFAULT_NEXUIZ_SERVER)
    parser.add_option('--nexuiz_folder', help="Nexuiz folder", default=NEXUIZ_ROOT)

    parser.add_option('--nott', dest='tt', action='store_false', help="Don't start teamtalk", default=True)
    parser.add_option('--nonex', dest='nex', action='store_false', help="Don't start Nexuiz nor HFS", default=True)


    (options, args) = parser.parse_args()

    dcw = DynamicConfigWriter(gametype=options.gametype,
                              minplayers=options.minplayers,
                              teamtalk_config_filename=options.ttconfig,
                              nexuiz_folder=options.nexuiz_folder,
                              url=options.url,
                              fraglimit=options.fraglimit,
                              message=options.message)

    if options.nex:
        dcw.update_nexuiz_config()
    if options.tt:
        dcw.update_teamtalk_config()

    print "Nexuiz Folder: %s" % options.nexuiz_folder
    print "Nexuiz: %s" % options.nexuiz
    print "HFS.exe: %s" % options.hfs
    print "Teamtalkd: %s" % options.teamtalk
    print "Teamtalk config: %s" % options.ttconfig
    print ""

    if options.launch:
        if options.tt:
            print "Launching TeamTalk"
            if options.nex:
                command = '%s -nd -c %s &' % (options.teamtalk, options.ttconfig)
            else:
                command = '%s -nd -c %s' % (options.teamtalk, options.ttconfig)
            os.system(command)
            print "Done\n"

        if options.nex:
            print "Launching HFS"
            os.system('wine %s &' % options.hfs)
            print "Done\n"

            print "Launching Nexuiz Server"
            full_nexuiz = os.path.join(options.nexuiz_folder, options.nexuiz)
            os.chdir(options.nexuiz_folder)
            os.system('%s +serverconfig %s' % (full_nexuiz, dcw.get_nexuiz_config_filename()))


if __name__ == '__main__':
    main()