@echo off
cd %~dp0

set rootPath=%~dp0\python\
set path=%SystemRoot%\System32;

REM @%SystemRoot%\System32\cmd /k

start  "��Ϣ����---redis����" /min C:\Redis\redis-server.exe  &
start "������͸---NAT����" /min NAT.py BIN  &
start "�м��---MIDDLE����" /min MIDDLE.py   &
 
start "WEB---FLASK����" /min WEB.py   &

start "��̨---WEBSOCKET����" /min  END.py   &








