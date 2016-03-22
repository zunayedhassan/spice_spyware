# -*- mode: python -*-
a = Analysis(['SpiceReportUnlocker.py'],
             pathex=['C:\\Users\\Zunayed Hassan\\PycharmProjects\\spice_report_unlocker'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'SpiceReportUnlocker.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='Unlock.ico')
