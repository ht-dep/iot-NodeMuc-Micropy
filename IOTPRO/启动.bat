@echo off
cd %~dp0

set rootPath=%~dp0\python\
set path=%SystemRoot%\System32;

REM @%SystemRoot%\System32\cmd /k

start  "��Ϣ����---redis����" /min C:\Redis\redis-server.exe  &
start "������͸---NAT����" /min natNet.py BIN  &
start "�м��---MIDDLE����" /min server_middle.py   &
 
start "WEB---FLASK����" /min web_server.py   &

start "��̨---WEBSOCKET����" /min  websocket_end.py   &








