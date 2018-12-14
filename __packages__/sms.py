import wx
import __packages__.connector as connector
from ObjectListView import ObjectListView, ColumnDefn
from twilio.rest import Client
import datetime

class SmsFrame(wx.Dialog):
	"""docstring for SmsFrame"""
	def __init__(self, *arg, **kwargs):
		super(SmsFrame, self).__init__(*arg, **kwargs, size=(700, 500))
		panel = wx.Panel(self)
		panel.SetBackgroundColour(wx.WHITE)
		wx.StaticText(self, -1, "Penerima", pos=(10, 10))
		self.nomor  = wx.TextCtrl(self, -1, pos=(10, 40), size=(300, 30))
		self.boxmsg = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, pos=(330, 40), size=(330, 350))
		self.send = wx.Button(self,  -1, "Kirim", pos=(330, 400))
		wx.Button(self, -1, "Batal", pos=(420, 400))
		self.pilihb = wx.Button(self, -1 , "Pilih", pos=(510, 400))
		self.pilihb.Bind(wx.EVT_BUTTON, self.pilih)
		self.send.Bind(wx.EVT_BUTTON, self.kirim)

		self.dataOlv = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER, pos=(10, 100), size=(300,350))
		self.dataOlv.SetColumns([
			ColumnDefn("No", "left", 150, "no_telp"),
			ColumnDefn("Nama", "left", 100, "nama")
			])
		query = ("SELECT nama_pel, no_telp FROM tb_member")
		stmt = ''
		hasil = connector.Execute(query, stmt, 4)
		sql = hasil["Data"]
		data = []
		for i in sql:
			dict = {"no_telp": i[0], "nama": i[1]} 
			data.append(dict)

		self.dataOlv.SetObjects(data)

		self.SetTitle("Sms Gateway")
		self.Show(True)
	def kirim(self, e):
		no_telp = self.nomor.GetValue()
		msg = self.boxmsg.GetValue()
		
		account_sid = "AC3cddc95d61ca0bb2e33dc5f8b48c93e8"
		auth_token = "f8d01a882f7e58b8b87d34fe1c6f1865"

		client = Client(account_sid, auth_token)

		message = client.messages.create(
			        to=no_telp,
			        from_="+15863718428",
			        body=msg
			    )
			    
		tglhari = datetime.datetime.now().date()
		query = ("INSERT INTO tb_sms_terkirim (status, no_telp, tanggal, keterangan) VALUES (%s,%s,%s,%s)")
		stmt = ("terkirim", no_telp, tglhari, msg)
		connector.Execute(query, stmt, 1)
	def pilih(self, e):
		ind = self.dataOlv.GetFirstSelected()
		if ind >= 0 :
			self.item = self.dataOlv.GetItem(ind, 1)
			self.nomor.SetValue(self.item.GetText())
