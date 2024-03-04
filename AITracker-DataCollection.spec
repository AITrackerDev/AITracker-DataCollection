# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['DataCollection.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/*', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AITracker-DataCollection',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='AITracker-DataCollection.app',
    icon=None,
    bundle_identifier=None,
    version='1.1.0',
    info_plist={
        'NSCameraUsageDescription':'The application needs access to the webcam in order to carry out the data collection process for our neural network.'
    }
)
