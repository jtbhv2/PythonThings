# -*- mode: python ; coding: utf-8 -*-
import glob
import os

flagsFolder = r'C:\\Users\\brian.stlouis\\OneDrive - City of Memphis\\Desktop\\FlagProject\\.venv\\Lib\\site-packages\\flagpy\\flags'
flagDfPath = r'C:\\Users\\brian.stlouis\\OneDrive - City of Memphis\\Desktop\\FlagProject\\.venv\\Lib\\site-packages\\flagpy\\flag_df.csv'

# Collect all .pkl files inside flags folder
flagsFiles = [(f, 'flagpy/flags') for f in glob.glob(os.path.join(flagsFolder, '*.pkl'))]

datas = [
    (flagDfPath, 'flagpy'),
] + flagsFiles

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

hiddenimports = collect_submodules('numpy')
datas = collect_data_files('numpy', include_py_files=True)

a = Analysis(
    ['flag.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='flag',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='flag'
)
