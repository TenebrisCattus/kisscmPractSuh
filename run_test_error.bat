@echo off
rem Проверка ошибки загрузки несуществующей VFS:
python -m src.main --vfs "non_existent_folder" --script "script_stage3.txt"
pause