# -*- mode: python -*-
a = Analysis(['Spice.py'],
             pathex=['C:\\Users\\Zunayed Hassan\\PycharmProjects\\spice'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'Spice.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='Spy.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'Spice.exe.app'))
