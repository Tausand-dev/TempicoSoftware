# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src/main.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['installers/pyinstaller_hooks/'],
             hooksconfig={},
             runtime_hooks=[],
             excludes=['scipy.cluster', 'scipy.constants', 'scipy.fft', 'scipy.integrate', 'scipy.interpolate', 'scipy.io', 'scipy.linalg', 'scipy.ndimage', 'scipy.odr', 'scipy.signal', 'scipy.sparse', 'scipy.spatial', 'scipy.stats', 'scipy._lib._uarray', 'scipy._lib.decorator', 'numpy.random', 'numpy.fft', 'numpy.linalg', 'numpy.ma'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='TempicoSoftware',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='Sources/tausand_small.ico')
