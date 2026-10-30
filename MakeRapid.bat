rem pyinstaller -F test_wx.py --collect-all wx --hidden-import wx --hidden-import wx._core

pyinstaller -F rapid-enter.py --clean --onefile --icon=ki_logo.ico --collect-all wx --hidden-import wx --hidden-import wx._core
pyinstaller -F rapid-station.py --clean --onefile --icon=ki_logo.ico --collect-all wx --hidden-import wx --hidden-import wx._core


