import wx
import __packages__.connector as connector
import datetime
from ObjectListView import ObjectListView, ColumnDefn

class KepentinganFrame(wx.Dialog):
	"""docstring for MessageFrame"""
	def __init__(self, *args, **kwargs):
		super(KepentinganFrame, self).__init__(*args, **kwargs, size=(700, 300))
		self.SetTitle("Kepentingan")

		panel = wx.Panel(self, -1)
		self.labelplate = wx.StaticText(panel, -1, "Nomor Plat", pos=(10, 10))
		self.plate = wx.TextCtrl(panel, -1, pos=(10, 40))

		self.labelketerangan = wx.StaticText(panel, -1, "Keterangan", pos=(10, 70))
		self.keterangan = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE, size=(300, 70), pos=(10 ,110))

		self.labeltglrekomendasi = wx.StaticText(panel, -1, "Tanggal Rekomendasi", pos=(370, 10))
		self.tanggal = wx.adv.DatePickerCtrl(panel, -1, pos=(370, 40), style = wx.adv.DP_DROPDOWN)

		self.labelket = wx.StaticText(panel, -1, "Keterangan", pos=(370, 70))
		self.keteranganrek = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE, size=(300, 70), pos=(370, 110))

		wx.StaticLine(panel, -1, style=wx.VERTICAL, pos=(340, 10), size=(2, 200))
		self.button1 = wx.Button(panel, -1, "Tambah", pos=(370, 210 ))
		self.button2 = wx.Button(panel, -1, "Batal", pos=(470, 210))

		self.button1.Bind(wx.EVT_BUTTON, self.Simpan)
		self.Show(True)
	def Simpan(self, e):
		try:
	
			plate = self.plate.GetValue()
			keterangan = self.keterangan.GetValue()
			tanggal = self.tanggal.GetValue()
			keterangan2 = self.keteranganrek.GetValue()
			
			tanggalrek = "{0}-{1}-{2}".format(tanggal.GetYear(),int(tanggal.GetMonth())+1,tanggal.GetDay())
			tanggalini = datetime.datetime.now()
			tanggalini = "{0}".format(str(tanggalini)[:10])
			query = ("UPDATE tb_kunjungan set keterangan = %s , rekomendasi = %s, keterangan2 = %s WHERE plate = %s and tgl_kunjungan = %s")
			stmt = (keterangan, tanggalrek, keterangan2, plate, tanggalini)
			connector.Execute(query, stmt, 1)

			dlg = wx.MessageDialog(self, "Data Tersimpan", "Perhatian", wx.OK|wx.ICON_INFORMATION)
			dlg.ShowModal()
		except Exception as e:
			dlg = wx.MessageDialog(self, "Gagal Tersimpan", "Perhatian", wx.OK|wx.ICON_INFORMATION)
			dlg.ShowModal()

		

