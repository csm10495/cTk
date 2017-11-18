import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from imports import *

class AbstractCtkObject(object):
    def __init__(self, *args, **kwargs):
        self._usedCells = set()

    def getUsedCells(self):
        ''' gets a set tuples of cells in use '''
        return self._usedCells

    def pack(self, *args, **kwargs):
        ''' encourage pack() not to get called as we are relying on grid() '''
        raise AttributeError("pack() is not supported. Only the grid system is supported")

    def addWidget(self, typ, name=None, toolTipText=None, x=0, y=0, gridKwargs=None, **kwargs):
        '''
        add a widget of a given type with a name of our choosing and an optional tool tip text to a given x, y cell
        pass the given gridKwargs to grid() and pass the remaining kwargs to the __init__ for the typ

        Can raise AttributeError if an overlapping cell is used
        '''
        if gridKwargs is None:
            gridKwargs = {}

        columnspan = gridKwargs.get('columnspan', 1)
        rowspan = gridKwargs.get('rowspan', 1)

        if int(columnspan) <= 0 or int(rowspan) <= 0:
            raise AttributeError("row/columnspan cannot be less than 1")

        for _x in range(x, x + columnspan):
            for _y in range(y, y + rowspan):
                if (_x, _y) in self._usedCells:
                    raise AttributeError("%d, %d is an overlapping cell" % (_x, _y))

                self._usedCells.add((_x, _y))

        tmp = typ(self, **kwargs)
        tmp.grid(row=y, column=x, **gridKwargs)

        if toolTipText is not None:
            toolTip = ToolTip(tmp, toolTipText)

            # If we have a name, save this as the ToolTip for that thing
            if name is not None:
                setattr(self, name + "ToolTip", toolTip)

        if name is not None:
            setattr(self, name, tmp)

    def expandRow(self, row, weight=1):
        '''
        expands a given row with a given weight
        '''
        self.rowconfigure(row, weight=weight)

    def expandColumn(self, column, weight=1):
        '''
        expands a given column with a given weight
        '''
        self.columnconfigure(column, weight=weight)

class CtkWindow(tk.Tk, AbstractCtkObject):
    '''
    a tk.Tk with all the features of the AbstractCtkObject
    '''
    def __init__(self, *args, **kwargs):
        '''
        all args/kwargs are passed to tk.Tk.__init__()
        '''
        tk.Tk.__init__(self, *args, **kwargs)
        AbstractCtkObject.__init__(self, *args, **kwargs)

class CtkFrame(tk.Frame, AbstractCtkObject):
    '''
    a tk.Frame with all the features of the AbstractCtkObject
    '''
    def __init__(self, *args, **kwargs):
        '''
        all args/kwargs are passed to tk.Frame.__init__()
        '''
        tk.Frame.__init__(self, *args, **kwargs)
        AbstractCtkObject.__init__(self, *args, **kwargs)

class _TestGui(CtkWindow):
    ''' this is an example gui '''
    def __init__(self):
        CtkWindow.__init__(self)
        self.title("Test GUI")
        self.addWidget(tk.Button, text="Show Messagebox", toolTipText="Will show the text in text box to the right in a message box", x=0, y=0, command=self.showMessageBox)
        self.addWidget(tk.Text, name="textMsgBox", x=1, y=0, height=1, gridKwargs={"sticky" : tk.NSEW})

        from widgets import ScrollableText
        self.addWidget(ScrollableText, name='scrollText', x=0, y=1, gridKwargs={"columnspan": 2, "sticky" : tk.NSEW})
        self.addWidget(tk.Button, text="Show Used Cells", x=0, y=2, command=self.showUsedCells)

        self.expandRow(1)
        self.expandColumn(1)
        self.mainloop()

    def showMessageBox(self):
        MessageBox.showinfo("Message", self.textMsgBox.get(1.0, tk.END))

    def showUsedCells(self):
        coordStr = ""
        for x, y in self.getUsedCells():
            coordStr += "(%d, %d)\n" % (x, y)
        self.scrollText.setText("\n%s\n" % (coordStr))

if __name__ == '__main__':
    g = _TestGui()