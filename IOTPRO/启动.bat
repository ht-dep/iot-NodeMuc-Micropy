@echo off
cd %~dp0

set rootPath=%~dp0\python\
set path=%SystemRoot%\System32;

REM @%SystemRoot%\System32\cmd /k

start  "消息队列---redis服务" /min C:\Redis\redis-server.exe  &
start "内网穿透---NAT服务" /min natNet.py BIN  &
start "中间件---MIDDLE服务" /min server_middle.py   &
 
start "WEB---FLASK服务" /min web_server.py   &

start "后台---WEBSOCKET服务" /min  websocket_end.py   &








