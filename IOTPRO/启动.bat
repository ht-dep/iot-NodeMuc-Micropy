@echo off
cd %~dp0

set rootPath=%~dp0\python\
set path=%SystemRoot%\System32;

REM @%SystemRoot%\System32\cmd /k

start "��Ϣ����---redis����" C:\Redis\redis-server.exe &
start "������͸---NAT����" natNet.py &
start "�м��---MIDDLE����" server_middle.py &
 
start "WEB---FLASK����" web_server.py &

start "��̨---WEBSOCKET����" websocket_end.py &








