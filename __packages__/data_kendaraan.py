import wx
import __packages__.connector as connector
import datetime
from ObjectListView import ObjectListView, ColumnDefn
import __packages__.Kepentingan as kp

class data_Kendaraan(wx.Dialog):
	"""docstring for data_Kendaraan"""
	def __init__(self, *arg, **kwargs):
		super(data_Kendaraan, self).__init__(*arg, **kwargs, pos=(300, 50) ,size=(900,600))
		
		self.SetTitle("Data Kendaraan")
		panel = wx.Panel(self)
		panel.SetBackgroundColour(wx.WHITE)

		#tampil data
		self.tampilMysql()


		#label-label
		wx.StaticText(self, -1, "Nomor Plat             :", pos=(30, 20))
		wx.StaticText(self, -1, "Nama Pelanggan   :", pos=(30, 50))
		wx.StaticText(self, -1, "No Telp                    :", (30, 80))
		wx.StaticText(self, -1, "Merk                        :", (30, 110))
		wx.StaticText(self, -1, "Model                      :", (30, 140))
		wx.StaticText(self, -1, "Perusahaan     :", (500, 20))
		wx.StaticText(self, -1, "Warna              :", (500, 50))
		wx.StaticText(self, -1, "Jenis                 :", (500, 80))
		wx.StaticText(self, -1, "Tahun              :", (500, 110))

		#textbox-textbox
		self.txtNomor = wx.TextCtrl(self, -1, pos=(150, 20), size=(30, 25))
		wx.TextCtrl(self, -1, pos=(190, 20), size=(50, 25))
		wx.TextCtrl(self, -1, pos=(250, 20), size=(50, 25))
		self.txtNama = wx.TextCtrl(self, -1, pos=(150, 50), size=(250, 25))
		self.txtTelp = wx.TextCtrl(self, -1, pos=(150, 80), size=(250, 25))
		self.txtMerk = wx.TextCtrl(self, -1, pos=(150, 110), size=(250, 25))
		self.txtModel = wx.TextCtrl(self, -1, pos=(150, 140), size=(250, 25))
		self.txtPerusahaan = wx.TextCtrl(self, -1, pos=(600, 20), size=(250, 25))
		self.txtWarna = wx.TextCtrl(self, -1, pos=(600, 50), size=(250, 25))
		pilihanJenis = ["Mobil", "Motor"]
		self.txtJenis = wx.ComboBox(self, choices = pilihanJenis, pos=(600, 80), size=(250, 25))
		pilihanTahun = ["1996 - 2000", "2001 - 2004", "2005 - 2009", "2010 - 2014", "2015 - 2019"]
		self.txtTahun = wx.ComboBox(self, choices = pilihanTahun, pos=(600, 110), size=(250, 25))
		pilihanSort = ["Nomor Plat", "Nama", "Tanggal", "Jenis", "Perusahaan"]
		self.txtSort = wx.ComboBox(self, choices=pilihanSort, pos=(300, 191.5), size=(190, 24))
		self.txtSort.SetValue("Nama")
		self.txtSearch = wx.TextCtrl(self, -1, pos=(600, 191.5), size=(250, 24))
		self.txtPilihan = wx.TextCtrl(self, -1)
		self.txtPilihan.SetValue("add")
		self.txtPilihan.Hide()

		#button-button
		self.btnsave = wx.Button(self, -1, "Save", pos=(500, 140))
		self.btnCancel = wx.Button(self, -1, "Cancel", pos=(600, 140))
		self.btnEdit = wx.Button(self, -1, "Edit", pos=(30, 190))
		self.btnDelete = wx.Button(self, -1, "Delete", pos=(120, 190))
		self.btnSort = wx.Button(self, -1, "Sort By", pos=(210, 190))
		self.btnSearch = wx.Button(self, -1, "Search", pos=(500, 190))
		self.btnkepentingan = wx.Button(self, -1, "Kepentingan", pos=(700, 140))

		#event-event
		self.btnsave.Bind(wx.EVT_BUTTON, self.saveData)
		self.btnEdit.Bind(wx.EVT_BUTTON, self.editData)
		self.btnDelete.Bind(wx.EVT_BUTTON, self.deleteData)
		self.btnCancel.Bind(wx.EVT_BUTTON, self.cancelBtn)
		self.txtSearch.Bind(wx.EVT_TEXT, self.searching)
		self.btnkepentingan.Bind(wx.EVT_BUTTON, self.tampil)

		self.dataOlv = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER, pos=(10, 230), size=(850, 300))
		self.setDataMobil()

		
		self.Centre()

		self.Show(True)
	def tampil(self, e):
		hasil = kp.KepentinganFrame(self)
		hasil.Show(True)
	def searching(self, e):
		self.setSearch()
		self.setDataMobil()
	def setSearch(self):
		varSearch = self.txtSearch.GetValue()
		valSort = self.txtSort.GetValue()

		if valSort == "Nomor Plat":
			query = ("SELECT * FROM tb_member WHERE plate LIKE %s")
		elif valSort == "Tanggal":
			query = ("SELECT * FROM tb_member WHERE added_date LIKE %s")
		elif valSort == "Perusahaan":
			query = ("SELECT * FROM tb_member WHERE perusahaan LIKE %s")
		elif valSort == 'Jenis':
			query = ("SELECT * FROM tb_member WHERE jenis LIKE %s")
		else:
			query = ("SELECT * FROM tb_member WHERE nama_pel LIKE %s")
		stmt = ("%" + varSearch + "%")
		self.datasek = []
		hasil = connector.Execute(query, stmt, 3)
		if hasil != 'Koneksi Gagal':
			data = hasil['Data']
			for i in data:
				self.tanggalIni = str(i[2])
				dict = {'plate': i[0], 'nama': i[1], 'tanggal': "{0}".format(self.tanggalIni[:10]), 'warna': i[4], 'merk': i[5], 'perusahaan': i[6],'model': i[7], 'tahun': i[8], 'jenis': i[9], "telp":i[10]}
				self.datasek.append(dict)

		else:
			wx.MessageBox(message="Cek Koneksi Anda", caption="Error", style=wx.OK | wx.ICON_INFORMATION)
	def setDataMobil(self, data=None):
		self.dataOlv.SetColumns([
				ColumnDefn("Plate", "left", 100, "plate"),
				ColumnDefn("Nama", "left", 100, "nama"),
				ColumnDefn("Telp", "left", 100, "telp"),
				ColumnDefn("Added", "left", 90, "tanggal"),
				ColumnDefn("Jenis","left", 70,  "jenis"),
				ColumnDefn("Merk", "left", 100, "merk"),
				ColumnDefn("Perusahaan", "left", 102, "perusahaan"),
				ColumnDefn("Model", "left", 100, "model"),
				ColumnDefn("Warna", "left", 100, "warna"),
				ColumnDefn("Tahun", "left", 100, "tahun")
			])
		if self.txtSearch != '':
			self.setSearch()
			self.dataOlv.SetObjects(self.datasek)
		else:
			self.dataOlv.SetObjects(self.dataMobil)
	def tampilMysql(self):
		self.dataMobil = []
		#--Getting Data Mobil From Mysql
		query = "SELECT * FROM tb_member ORDER BY added_date DESC"
		stmt = ''
		hasil = connector.Execute(query, stmt, 2)
		if hasil != 'Koneksi Gagal':
			data = hasil['Data']
			for i in data:
				self.tanggalIni = str(i[2])
				dict = {'plate': i[0], 'nama': i[1], 'tanggal': "{0}".format(self.tanggalIni[:10]), 'warna': i[4], 'merk': i[5], 'perusahaan': i[6],'model': i[7], 'tahun': i[8], 'jenis': i[9], "telp":i[10]}
				self.dataMobil.append(dict)

		else:
			wx.MessageBox(message="Cek Koneksi Anda", caption="Error", style=wx.OK | wx.ICON_INFORMATION)
		#--end
	def saveData(self, e):

		self.getValueTextBox()

		if self.txtPilihan.GetValue() == 'add':

			if self.nomor == '' or self.nama == '' or self.telp == '' or self.merk == '' or self.model == '' or self.perusahaan == '' or self.warna == '' or self.jenis == '' or self.tahun == '':
				dlg = wx.MessageDialog(self, "Pastikan Data Sudah Penuh", "Perhatian", wx.OK | wx.ICON_INFORMATION)
				dlg.ShowModal()
				return
			else:
				query = ("INSERT INTO tb_member (plate, nama_pel, added_date, warna, merk, perusahaan, model, tahun, jenis, no_telp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

				stmt = (self.nomor.upper(), self.nama, datetime.datetime.now(), self.warna.upper(), self.merk.upper(), self.perusahaan.upper(), self.model.upper(), self.tahun, self.jenis.upper(), self.telp)
				hasil = connector.Execute(query, stmt, 1)
				self.tampilMysql()
				self.setDataMobil()
				self.delValueTextBox()
		elif self.txtPilihan.GetValue() == "edit":
			query = ("UPDATE tb_member SET nama_pel = %s, warna = %s, merk = %s, perusahaan = %s, model = %s, tahun = %s, jenis = %s, no_telp = %s WHERE plate = %s")
			stmt = (self.nama, self.warna.upper(), self.merk.upper(), self.perusahaan.upper(), self.model.upper(), self.tahun, self.jenis.upper(), self.telp, self.nomor.upper())
			connector.Execute(query, stmt, 1)
			self.tampilMysql()
			self.setDataMobil()
			self.delValueTextBox()

		self.txtPilihan.SetValue('add')
		self.txtNomor.Enable()
	def editData(self, e):
		ind = self.dataOlv.GetFirstSelected()
		if ind >= 0:
			self.item = self.dataOlv.GetItem(ind)
			self.item2 = self.dataOlv.GetItem(ind, 1)
		query = ("SELECT * FROM tb_member WHERE plate = %s and nama_pel = %s")
		stmt = (self.item.GetText(), self.item2.GetText())
		hasil = connector.Execute(query, stmt, 4)
		data = hasil['Data']
		self.txtNomor.SetValue(data[0][0])
		self.txtNama.SetValue(data[0][1])
		self.txtTelp.SetValue(data[0][10])
		self.txtMerk.SetValue(data[0][5])
		self.txtModel.SetValue(data[0][7])
		self.txtPerusahaan.SetValue(data[0][6])
		self.txtWarna.SetValue(data[0][4])
		self.txtJenis.SetValue(data[0][9])
		self.txtTahun.SetValue(data[0][8])
		self.txtPilihan.SetValue("edit")
		self.txtNomor.Disable()
	def deleteData(self, e):
		ind = self.dataOlv.GetFirstSelected()
		if ind >= 0:
			self.item = self.dataOlv.GetItem(ind)
			self.item2 = self.dataOlv.GetItem(ind, 1)
		query = ("DELETE FROM tb_member WHERE plate = %s and nama_pel = %s")
		stmt = (self.item.GetText(), self.item2.GetText())
		connector.Execute(query, stmt, 1)
		self.tampilMysql()
		self.setDataMobil()
	def cancelBtn(self, e):
		self.delValueTextBox()
		self.txtNomor.Enable()
		self.txtPilihan.SetValue('add')

	def getValueTextBox(self):
		self.nomor = self.txtNomor.GetValue()
		self.nama = self.txtNama.GetValue()
		self.telp = self.txtTelp.GetValue()
		self.merk = self.txtMerk.GetValue()
		self.model = self.txtModel.GetValue()
		self.perusahaan = self.txtPerusahaan.GetValue()
		self.warna = self.txtWarna.GetValue()
		self.jenis = self.txtJenis.GetValue()
		self.tahun = self.txtTahun.GetValue()
	def delValueTextBox(self):
		self.txtNomor.SetValue('')
		self.txtNama.SetValue('')
		self.txtTelp.SetValue('')
		self.txtMerk.SetValue('')
		self.txtModel.SetValue('')
		self.txtPerusahaan.SetValue('')
		self.txtWarna.SetValue('')
		self.txtJenis.SetValue('')
		self.txtTahun.SetValue('')
