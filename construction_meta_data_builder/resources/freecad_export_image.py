import sys
import FreeCADGui as Gui
import Part
import tempfile

from pathlib import Path


Gui.SendMsgToActiveView("OrthographicCamera")
Gui.SendMsgToActiveView("ViewAxo")

view = Gui.ActiveDocument.ActiveView
view.saveImage(str(Path.cwd() / "image.png"), 1000, 1000, "White")

# Close active document
App.closeDocument(App.ActiveDocument.Name)
Gui.doCommand('exit()')
