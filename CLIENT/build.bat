cd src
pyinstaller --onefile -w group_chat_client.py
rmdir /s .\build
del *.spec
cd ..
move src\dist\group_chat_client.exe .\dist
rmdir src\dist
