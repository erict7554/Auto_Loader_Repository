
[gcode_macro AUTO_LOADER_ON]
gcode:
  RUN_SHELL_COMMAND CMD=loader_on

[gcode_shell_command loader_on]
command: sudo sh Auto_Loader_Repository/auto_loader_start.sh 
timeout: 10000
verbose: True
