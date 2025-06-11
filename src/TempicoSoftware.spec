# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src/main.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=['numpy.core._multiarray_tests'],
             hookspath=['installers/pyinstaller_hooks/'],
             hooksconfig={},
             runtime_hooks=[],
             excludes=['scipy.fft', 'scipy.integrate', 'scipy.interpolate', 'scipy.io', 'scipy.odr', 'scipy.signal', 'scipy.stats', 'scipy.cluster', 'scipy.ndimage', 'scipy.misc', 'PySide2.QtNetwork', 'PySide2.QtXml', 'PySide2.QtXmlPatterns', 'PySide2.QtPrintSupport', 'PySide2.QtMultimedia', 'PySide2.QtMultimediaWidgets', 'PySide2.QtOpenGL', 'PySide2.QtQml', 'PySide2.QtQuick', 'PySide2.QtQuickWidgets', 'PySide2.QtSql', 'PySide2.QtSvg', 'PySide2.QtTest', 'PySide2.QtWebEngine', 'PySide2.QtWebEngineWidgets', 'PySide2.QtWebSockets', 'PySide2.Qt3DRender', 'PySide2.QtSensors', 'PySide2.QtLocation', 'PySide2.Qt3DExtras', 'pyqtgraph.opengl', 'pyqtgraph.widgets.MatplotlibWidget', 'pyqtgraph.exporters.matplotlib', 'pyqtgraph.exporters.SVGExporter', 'pyqtgraph.dockarea', 'pyqtgraph.flowchart', 'numpy.random._examples', 'numpy.lib.recfunctions', 'pytz', 'packaging', 'virtualenv', 'distlib', 'importlib_metadata', 'platformdirs', 'pyinstaller_hooks_contrib', 'typing_extensions', 'pyinstaller_hooks_contrib'],
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
