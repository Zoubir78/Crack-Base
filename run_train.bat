@echo off
REM Chemin vers l'installation d'Anaconda
set "CONDA_PATH=C:\Users\z.marouf-araibi\AppData\Local\anaconda3"
REM Ajout de Conda au chemin
set "PATH=%CONDA_PATH%;%CONDA_PATH%\Scripts;%CONDA_PATH%\Library\bin;%PATH%"
REM Activer l'environnement Conda
call %CONDA_PATH%\Scripts\activate.bat DLTA-AI
REM Exécuter le script Python
python C:\Users\z.marouf-araibi\Desktop\Crack-Base\mmdetection\tools\train.py
pause

