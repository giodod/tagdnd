import wx
import subprocess as sub
########################################################################
class MyFileDropTarget(wx.FileDropTarget):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, window,mylabel):
        """Constructor"""
        wx.FileDropTarget.__init__(self)
        self.window = window
	self.mylabel = mylabel
 	self.fileTextCtrl = wx.TextCtrl(window,
                                        style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY)

	self.fileTextCtrl.SetDropTarget(self)
	self.fileTextCtrl.WriteText(self.mylabel)
	myTextAttr=wx.TextAttr(wx.RED)
        font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        myTextAttr.SetFont(font)
	self.fileTextCtrl.SetStyle(0,self.fileTextCtrl.GetLastPosition(),myTextAttr)
    #----------------------------------------------------------------------
    def CleanStart(self, mylabel):
        """
        To reuse box you must fill again begin data
        """
	self.mylabel = mylabel
	self.fileTextCtrl.Clear()
	self.fileTextCtrl.WriteText(self.mylabel)
	myTextAttr=wx.TextAttr(wx.RED)
        font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        myTextAttr.SetFont(font)
	self.fileTextCtrl.SetStyle(0,self.fileTextCtrl.GetLastPosition(),myTextAttr)
    #----------------------------------------------------------------------
    def OnDropFiles(self, x, y, filenames):
        """
        When files are dropped, write where they were dropped and then
        the file paths themselves
        """
        self.window.SetInsertionPointEnd()
        self.fileTextCtrl.WriteText("\n+ %d" %
                              (len(filenames)))

	for filepath in filenames:
            #self.fileTextCtrl.WriteText('.')
	    output=sub.check_output("~/tmsu-x86_64-0.5.2/bin/tmsu tag \""+filepath+"\" "+self.mylabel, shell=True)
	    print(output)



########################################################################
class DnDPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
	self.boxdrops=[]
    	self.n_start=0
    	self.n_winsize=15
	self.labels=self.GetTags()
	self.nmax=len(self.labels)
        labels=self.labels
	if(len(labels)<self.n_winsize):
		self.n_winsize=len(labels)
	print(labels)
	print(self.n_winsize)
	for i in range(0,self.n_winsize):
		self.boxdrops.append(MyFileDropTarget(self,labels[i]))
		print(labels[i])
        lbl = wx.StaticText(self, label="Tags:"+str(self.nmax)+"\nDrag some files\nin Tag-Target:")
        sizer = wx.GridSizer(4)
        #sizer.Add(lbl, 0, wx.ALL, 5)
	# the edit control - one line version.
	vbox = wx.BoxSizer(wx.VERTICAL)
        self.editname = wx.TextCtrl(self, value="New Tag")
        m_newtag = wx.Button(self, wx.ID_ANY, "Add tag")
        m_newtag.Bind(wx.EVT_BUTTON, self.AddTag)
        refresh = wx.Button(self, id=wx.ID_ANY, label="Refresh")
        refresh.Bind(wx.EVT_BUTTON, self.onRefreshTags)
        vbox.Add(lbl, 0, wx.ALL, 1)
	vbox.Add(self.editname, 0, wx.ALL, 1)
	vbox.Add(m_newtag, 0, wx.ALL, 1)
 	vbox.Add(refresh, 0, wx.ALL, 1)
	sizer.Add(vbox, 0, wx.ALL, 1)
	
	vbox2 = wx.BoxSizer(wx.VERTICAL)
        avanti = wx.Button(self, wx.ID_ANY, "--->>")
        avanti.Bind(wx.EVT_BUTTON, self.Avanti)
        indietro = wx.Button(self, id=wx.ID_ANY, label="<<---")
        indietro.Bind(wx.EVT_BUTTON, self.Indietro)
        vbox2.Add(avanti, 0, wx.ALL, 2)
	vbox2.Add(indietro, 0, wx.ALL, 2)


	for i in range(0, self.n_winsize):
		sizer.Add(self.boxdrops[i].fileTextCtrl, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(vbox2, 0, wx.ALL, 2)
        self.SetSizer(sizer)
	

    #----------------------------------------------------------------------
    def SetInsertionPointEnd(self):
        """
        Put insertion point at end of text control to prevent overwriting
        """
        for i in range(0, self.n_winsize):
		self.boxdrops[i].fileTextCtrl.SetInsertionPointEnd()

    #----------------------------------------------------------------------
    def updateText(self, text):
        """
        Write text to the text control
        """
        #self.file_drop_target.fileTextCtrl.WriteText(text)
        #self.file_drop_target2.fileTextCtrl.WriteText(text)
 	donothing=1

    #----------------------------------------------------------------------
    def AddTag(self,text):
        """
        Write text to the text control
        """
        #self.file_drop_target.fileTextCtrl.WriteText(text)
        #self.file_drop_target2.fileTextCtrl.WriteText(text)
	tagname=self.editname.GetLineText(0)
	print(tagname)
	output=sub.check_output("~/tmsu-x86_64-0.5.2/bin/tmsu tag -c "+tagname, shell=True)
	print(output)
 	donothing=1
    #----------------------------------------------------------------------
    def onRefreshTags(self,text):
        """
        Write text to the text control
        """
	self.labels=self.GetTags()
	self.nmax=len(self.labels)
	self.n_start=0
	self.onRefreshDrops(text)
 
    #----------------------------------------------------------------------
    def onRefreshDrops(self,text):
        """
        Write text to the text control
        """
        #self.file_drop_target.fileTextCtrl.WriteText(text)
        #self.file_drop_target2.fileTextCtrl.WriteText(text)
    	for i in range(0, self.n_winsize):
		self.boxdrops[i].CleanStart(self.labels[i+self.n_start])
		#print("pos:"+str(i)+"val "+self.labels[i+self.n_start])
   	donothing=1
    
    #----------------------------------------------------------------------
    def GetTags(self):
        """
        GetTags from External
        """
        output=sub.check_output("~/tmsu-x86_64-0.5.2/bin/tmsu tags", shell=True)
        print(output)
        labels=output.split()
        return labels
    #----------------------------------------------------------------------
    def Avanti(self,text):
        """
        avanti
        """
        self.n_start=self.n_start+self.n_winsize
	#print("n_start sarebbe:"+str(self.n_start))
        if self.n_start > (self.nmax-self.n_winsize) :
		self.n_start = self.nmax - self.n_winsize
	print("controllato:"+str(self.n_start))
	#self.onRefreshDrops(text)

    #----------------------------------------------------------------------
    def Indietro(self,text):
        """
        indietro
        """
	self.n_start=self.n_start-self.n_winsize
        #print("n_start sarebbe:"+str(self.n_start))
        if self.n_start < 0 :
		self.n_start = 0
	#print("controllato:"+str(self.n_start))
	self.onRefreshDrops(text)


########################################################################
class DnDFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="Tags 4")
        panel = DnDPanel(self)
        self.Show()

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = DnDFrame()
    app.MainLoop()
