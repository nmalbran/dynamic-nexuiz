import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

INICIAL_LOG_FOLDER = os.path.join(ROOT, 'Nexuiz', 'data')
FINAL_LOG_FOLDER = os.path.join(ROOT, 'Nexuiz', 'data', 'logs')
STATS_FOLDER = os.path.join(ROOT, 'stats')
LOGFILE_RE = '^20\d{6}.*(dm|ctf|tdm)\.log$'
MINPLAYERS = 3

def get_all_log_files():
    regex = re.compile(LOGFILE_RE)
    return [os.path.join(INICIAL_LOG_FOLDER, f) for f in os.listdir(INICIAL_LOG_FOLDER) if regex.match(f)]

def parse_log(full_logfile):
    logfile = os.path.basename(full_logfile)
    statfile = 'Nexuiz-Statistics-%s-%s.html' % (logfile[0:8], logfile[19:-4])
    statfile = os.path.join(STATS_FOLDER, statfile)
    os.system('nexlogparser %s -n %s -o %s -p nexuiz_log_parser.players.PLAYERS' % (full_logfile, MINPLAYERS, statfile))

def move_parsed_log(logfile):
    shutil.move(logfile, FINAL_LOG_FOLDER)

def main():
    for log in get_all_log_files():
        parse_log(log)
        move_parsed_log(log)

if __name__ == '__main__':
    main()