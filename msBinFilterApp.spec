# -*- mode: python -*-
# used by pyinstaller to create .exe
# C:\apps\Anaconda2) C:\apps\eclipseRCP\workspace\MS_Bin_and_Filter>
# pyinstaller --onefile msBinFilterApp.spec
block_cipher = None


a = Analysis(['msBinFilterApp.py'],
             pathex=['C:\\apps\\eclipseRCP\\workspace\\MS_Bin_and_Filter'],
             binaries=[],
             datas=[('utils\\template.mzXML','utils')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='msBinFilterApp',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='msBinFilterApp')
