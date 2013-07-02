Dynamic Nexuiz Server Launcher
==============================

Script to dynamically update some settings and launch Nexuiz Server, HFS and Teamtalk.
Work on Linux. Wine is required to launch HFS.


#### What it does

1. Update local ip in Nexuiz config file
2. Update custom settings in Nexuiz config file
3. Update local ip in teamtalk config file
4. Launch HFS with wine
5. Launch teamtalk
6. Launch Nexuiz



#### Example
	
	./dynamic_nexuiz_server_launcher.py -t dm -n 10 -l



#### Command line options

All command line options have default parameters specified below.

	Usage: dynamic_nexuiz_server_launcher.py [options]

	Options:
	  -h, --help            show this help message and exit

	  -t GAMETYPE, --gametype=GAMETYPE
	                        Type of Game [ctf|dm]
	  -n MINPLAYERS, --minplayers=MINPLAYERS
	                        Minimum number of players
	  --url=URL             Url for maps downloading

	  -l, --launch          Launch the servers: HFS, Teamtalk and Nexuiz (on
	                        linux)

	  --hfs=HFS             HFS executable by wine
	  --teamtalk=TEAMTALK   teamtalkd file
	  --ttconfig=TTCONFIG   Configuration file for teamtalk server
	  --nexuiz=NEXUIZ       Nexuiz executable
	  --nexuiz_folder=NEXUIZ_FOLDER
	                        Nexuiz folder



#### Default setup expected

	├── dynamic_nexuiz_server_launcher.py
	├── Nexuiz
	│   ├── nexuiz-linux-x86_64-dedicated
	│   ├── data
	│   │   ├── 00_server_ctf.cfg
	│   │   ├── 00_server_ctf.cfg.base
	│   │   ├── 00_server_dm.cfg
	│   │   ├── 00_server_dm.cfg.base
	│   │   └── ...
	│   └── ...
	│
	├── teamtalk
	│   ├── teamtalkd
	│   ├── tt4svc.xml
	│   └── tt4svc.xml.base
	│ 
	├── hfs.exe
	└── vfs.vfs

When editing server config files, edit `*.cfg.base` files. Then, the script will automatically update `*.cfg` files.



#### Default script parameters

These parameters describe the above setting, change at will for a different setup.
Also they can be passed as command line options (see above).


	ROOT
		Full path to dynamic_nexuiz_server_launcher.py
	NEXUIZ_ROOT
		Full path to Nexuiz folder
	TEAMTALK_ROOT
		Full path to teamtalk folder

	DEFAULT_GAMETYPE = 'ctf'
		Default gametype setting (ctf, dm ...)
	DEFAULT_MINPLAYERS = 8
		Default minplayers setting (int)
	DEFAULT_MAPS_URL = ':8080/maps/'
		Default url for maps download

	DEFAULT_HFS_EXE
		Full path to hfs executable
	DEFAULT_TEAMTALKD
		Full path to teamtalkd executable
	DEFAULT_TEAMTALK_CONFIG_FILENAME
		Full path to teamtalk config file
	DEFAULT_NEXUIZ_SERVER
		Nexuiz executable
