import os
import pyinotify
a = 0

wm = pyinotify.WatchManager()
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_OPEN | pyinotify.IN_MODIFY
class PTmp(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Create: %s" %  os.path.join(event.path, event.name)

    def process_IN_MODIFY(self, event):
        print "Modify: %s" %  os.path.join(event.path, event.name)

    def process_IN_DELETE(self, event):
        print "Remove: %s" %  os.path.join(event.path, event.name)

    def process_IN_OPEN(self, event):
        print "Opening: %s" %  os.path.join(event.path, event.name)


handler = PTmp()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('folder_path', mask, rec=True)
while notifier.check_events():  #loop in case more events appear while we are processing
    notifier.read_events()
    notifier.process_events()




