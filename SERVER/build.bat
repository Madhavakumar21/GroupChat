mkdir dist
cd src
pyinstaller --onefile group_chat_server.py
rmdir /s .\build
del *.spec
cd ..
move src\dist\group_chat_server.exe .\dist
rmdir src\dist
