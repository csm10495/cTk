import sys

if sys.version_info.major == 2:
    import Tkinter as tk
    import tkMessageBox as MessageBox
    from idlelib.ToolTip import ToolTip
elif sys.version_info.major == 3:
    import tkinter as tk
    from tkinter import messagebox as MessageBox
    from idlelib.tooltip import ToolTip
