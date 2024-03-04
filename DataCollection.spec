# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['DataCollection.py'],
    pathex=[],
    binaries=[],
    datas=[('./assets/dot.png', './assets/dot.png'), ('./assets/haarcascade_eye.xml', './assets/haarcascade_eye.xml'), ('./assets/shape_predictor_68_face_landmarks.dat', './assets/shape_predictor_68_face_landmarks.dat')],
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
    name='DataCollection',
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
    name='DataCollection.app',
    icon=None,
    bundle_identifier=None,
)
