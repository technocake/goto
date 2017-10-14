from pywinauto.application import Application
import pywinauto
import warnings
# ignoring a lot of warnings to run python in 64bit mode for 
# 64bit applications and vice versa for 32bit. 
warnings.filterwarnings('ignore')
pywinauto.actionlogger.disable()

list_of_visible_windows = []
windows = pywinauto.findwindows.find_windows(enabled_only=True, visible_only=True)

for handle in windows:
	a = Application()
	a.connect(handle=handle)
	w = a.windows()[0]
	window = w.element_info
	#print("name: %s" % window.name)
	#print("pid: %d" % window.process_id)
	#print("visible: %s" % window.visible)
	if window.visible:
		list_of_visible_windows.append(window)

for w in list_of_visible_windows:
	print((w.process_id, w.name))