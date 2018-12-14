import wx
import __packages__.connector as connector
from ObjectListView import ObjectListView, ColumnDefn

class SmsFrame(wx.Dialog):
	"""docstring for SmsFrame"""
	def __init__(self, *arg, **kwargs):
		super(SmsFrame, self).__init__(*arg, **kwargs, size=(700, 500))
		panel = wx.Panel(self)
		panel.SetBackgroundColour(wx.WHITE)
		wx.StaticText(self, -1, "Cari", pos=(10, 10))
		wx.TextCtrl(self, -1, pos=(10, 40), size=(650, 30))
		

		self.dataOlv = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER, pos=(10, 100), size=(650,350))
		self.dataOlv.SetColumns([
			ColumnDefn("No", "left", 150, "no_telp"),
			ColumnDefn("Tanggal Terkirim","left", 130, "tgl"),
			ColumnDefn("Isi Pesan", "left", 240, 'isi')
			])
		
		query = ("SELECT a.no_telp, a.tanggal, a.keterangan  FROM tb_sms_terkirim as a")
		stmt = ''
		hasil = connector.Execute(query, stmt, 4)
		sql = hasil["Data"]
		data = []
		for i in sql:
			dict = {"no_telp": i[0], "tgl": i[1], "isi":i[2]} 
			data.append(dict)

		self.dataOlv.SetObjects(data)
		self.SetTitle("SMS Archive")
		self.Show(True)

