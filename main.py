import wx
import wx.grid
import sys
import __packages__.data_kendaraan as data_kendaraan
import cv2
import os
import time
import requests
import base64
import json
import __packages__.connector as connector
from ObjectListView import ObjectListView, ColumnDefn
import datetime
import __packages__.Kepentingan as kp
import calendar
import subprocess
from twilio.rest import Client
import __packages__.sms as sms
import __packages__.sms_archive as arch
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

class plateRecognition(wx.Frame):
	"""docstring for plateRecognition"""
	def __init__(self, *args, **kwargs):
		super(plateRecognition, self).__init__(*args, **kwargs)
		
		loc = wx.Icon("images/license_plate.png", wx.BITMAP_TYPE_ANY)
		self.SetIcon(loc)


		self.basicGui()
	def basicGui(self):
		menuBar = wx.MenuBar()
		#set up Menu Bar
		fileButton = wx.Menu()
		messageButton = wx.Menu()
		dataButton = wx.Menu()
		grafikButton = wx.Menu()
		settingButton = wx.Menu()
		helpButton = wx.Menu()

		panel = wx.Panel(self)
		panel.SetBackgroundColour(wx.WHITE)
		#Start Menu Bar Item
		#---File Item--#
		#openItem = fileButton.Append(wx.ID_OPEN, '&Open', "Open Button")
		#saveItem = fileButton.Append(wx.ID_SAVE, '&Save', 'Save Button')
		exitItem = fileButton.Append(wx.ID_EXIT, '&Exit', "Exit Button")
		#--Data Item--#
		mobilItem = dataButton.Append(wx.ID_ANY, '&Data Kendaraan', "Data Kendaraan")
		#--Grafik Item--#
		perhariItem = grafikButton.Append(wx.ID_ANY, "&Grafik kendaraan", "Grafik Kendaraan Per Hari")
		messageItem = messageButton.Append(wx.ID_ANY, "&Kirim SMS", "Kirim SMS")
		messageItem2 = messageButton.Append(wx.ID_ANY, "&SMS Terkirim", "SMS Terkirim")
		#End Menu Bar Item

		#Appending to Form
		menuBar.Append(fileButton, 'File')
		menuBar.Append(dataButton, 'Data')
		menuBar.Append(grafikButton, 'Grafik')
		menuBar.Append(messageButton, "Message")

                
		self.SetMenuBar(menuBar)
		#event
		self.Bind(wx.EVT_MENU, self.Quit, exitItem)
		self.Bind(wx.EVT_MENU, self.data_kendaraan_Click, mobilItem)
		self.Bind(wx.EVT_MENU, self.sms_click, messageItem)
		self.Bind(wx.EVT_MENU, self.archived, messageItem2)
		self.Bind(wx.EVT_MENU, self.graphic , perhariItem)

		#Create Tab
		nb = wx.Notebook(panel)
		tab2 = TabTwo(nb)
		tab3 = TabThree(nb)
		nb.AddPage(tab2, "Recognition")
		nb.AddPage(tab3, "Manual")

		sizer = wx.BoxSizer()
		sizer.Add(nb, 1, wx.EXPAND)
		panel.SetSizer(sizer)
		#----End Tab----
		tglhari = datetime.datetime.now().date()
		try:
			query = ("select a.keterangan2, b.no_telp, a.id_kunjungan from tb_kunjungan as a, tb_member as b WHERE a.plate = b.plate and a.status='belum' and a.rekomendasi = %s")
			stmt = (str(tglhari))
			hasil = connector.Execute(query, stmt, 3)
			for row in hasil["Data"]:
				
				account_sid = "AC3cddc95d61ca0bb2e33dc5f8b48c93e8"
				auth_token = "f8d01a882f7e58b8b87d34fe1c6f1865"

				client = Client(account_sid, auth_token)

				message = client.messages.create(
				        to=row[1],
				        from_="+15863718428",
				        body=row[0]
				    )
				print(message.sid)
				query = ("UPDATE tb_kunjungan set status = %s WHERE tgl_kunjungan = %s")
				stmt = ("terkirim",str(tglhari))
				connector.Execute(query, stmt, 1)
				query = ("INSERT INTO tb_sms_terkirim (id_kunjungan, status, no_telp, tanggal, keterangan) VALUES (%s,%s,%s,%s,%s)")
				stmt = (row[2], "terkirim", row[1], tglhari, row[0])
				connector.Execute(query, stmt, 1)
			if hasil == 'Koneksi Gagal':
				self.textStat = 'Not Connected'
			else:
				self.textStat = "Connected"
		except Exception as e:
			self.textStat = 'Not Connected'

		today = datetime.datetime.now()
		self.StatusBar = self.CreateStatusBar(3)
		self.StatusBar.SetStatusText("Welcome To ALPR System")
		self.StatusBar.SetStatusWidths([500,600,100])
		self.StatusBar.SetStatusText(calendar.day_name[today.weekday()]+','+' '+'{0}'.format(str(today)[:10]), 1)
		self.StatusBar.SetStatusText("Status : "+self.textStat, 2)
		self.Show()
		
		self.SetTitle('Automatic License Plate Recognition')
		
		self.Show(True)
		self.Maximize()
	#funtion event
	def Quit(self, e):
		self.Close()
	def data_kendaraan_Click(self, e):
		'''win = data_Kendaraan(self)
		win.Show()'''
		win = data_kendaraan.data_Kendaraan(self)
		win.Show(True)
	def sms_click(self, e):
		app = sms.SmsFrame(self)
		app.Show(True)
	def archived(self, e):
		app = arch.SmsFrame(self)
		app.Show(True)
	def graphic(self, e):
		style.use('fivethirtyeight')
		fig = plt.figure(figsize=(10,6))
		ax1 = fig.add_subplot(1,1,1)
		fig.canvas.set_window_title("Grafik")

		def animate(i):
		    
		    xs = []
		    ys = []
		    zs = []
		    xs2 =[]
		    query = ("SELECT count(a.plate), a.tgl_kunjungan FROM tb_kunjungan as a, tb_member as b WHERE a.plate = b.plate and b.jenis='mobil' GROUP BY a.tgl_kunjungan")
		    stmt = ''
		    hasil = connector.Execute(query, stmt, 4)
		    for row in hasil["Data"]:
		    	xs.append(str(row[1]))
		    	ys.append(row[0])
		    query = ("SELECT count(a.plate), a.tgl_kunjungan FROM tb_kunjungan as a, tb_member as b WHERE a.plate = b.plate and b.jenis='motor' GROUP BY a.tgl_kunjungan")
		    stmt = ''
		    hasil = connector.Execute(query, stmt, 4)
		    for row in hasil["Data"]:
		    	xs2.append(str(row[1]))
		    	zs.append(row[0])
		    print(xs2)


		    
		    ax1.clear()
		    ax1.plot(xs2, zs, label="Motor")
		    ax1.plot(xs, ys, label="Mobil")
		    ax1.legend(loc='best')
		    ax1.set_ylabel("Jumlah Kendaraan")

		ani = animation.FuncAnimation(fig, animate, interval=1000)
		plt.suptitle('Grafik Kendaraan')
		plt.show()
class TabTwo(wx.Panel):
	"""docstring for TabTwo"""
	capture = ''
	def __init__(self, parent, capture=capture):
		wx.Panel.__init__(self, parent)
		
		self.photoDefault = "images/no_webcam.jpg"
		self.pathp = ''
		
		#pic = wx.Image(self.photoDefault, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		#wx.StaticBitmap(self, -1, pic, (50,20), (1000,300))
		bitmap = wx.Bitmap(self.photoDefault)
		bitmap = scale_bitmap(bitmap, 640, 380)
		control = wx.StaticBitmap(self, -1, bitmap)
		control.SetPosition((50,280)) #50, 420

		self.text = wx.StaticText(self, -1, "B805WYN", (790,280))
		font = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
		self.text.SetFont(font)

		#Button
		self.btnOpenFile = wx.Button(self, -1, "Open File", pos=(720, 320), size=(120, 30))
		self.btnStart = wx.Button(self, -1, "Start", pos=(720, 350), size=(120, 30))
		self.btnStop = wx.Button(self, -1, "Stop", pos=(720, 350), size=(120, 30))
		self.btnRecog = wx.Button(self, -1, "Recognize", pos=(720, 380), size=(120, 30))
		self.btntambahData = wx.Button(self, -1, "Tambah Data", pos=(850, 320), size=(120, 30))
		self.btnKepen = wx.Button(self, -1, "Tambah Kepentingan", pos=(850, 350), size=(120,30))


		#
		
		#event
		self.btnStop.Hide()
		self.btnStart.Bind(wx.EVT_BUTTON, self.start)
		self.btnStop.Bind(wx.EVT_BUTTON, self.stop)
		self.btnOpenFile.Bind(wx.EVT_BUTTON, self.openFile)
		self.btnRecog.Bind(wx.EVT_BUTTON, self.recognition)
		self.btnKepen.Bind(wx.EVT_BUTTON, self.kepentingan)
		self.btntambahData.Bind(wx.EVT_BUTTON, self.tambahData)

		#bx = wx.StaticBox(self, 1, pos=(690,9), size=(300, 140))
		#customize
		self.btnStart.SetBitmap(wx.Bitmap("images/rec.png"))
		self.btnStop.SetBitmap(wx.Bitmap("images/stop.png"))
		self.btnOpenFile.SetBitmap(wx.Bitmap("images/folder(1).png"))
		self.btnRecog.SetBitmap(wx.Bitmap("images/eye-button.png"))
		#camera setup

		#videoWarper = wx.StaticBox(self, label="Video",size=(400,300))
		#videoBoxSizer = wx.StaticBoxSizer(videoWarper, wx.VERTICAL)

		parent.Centre()
		self.Show()
		
		#hasil Recog
		text = wx.StaticText(self, -1, "Nomor Plat     :", (1020, 30))
		text = wx.StaticText(self, -1, "Daerah             :", (1020, 50))

		self.plateNumberPlat = wx.StaticText(self, -1, "Unknown", (1140, 30))
		daerahPlat = wx.StaticText(self, -1, "Unknown", (1140, 50))
		
		
		#-----Database------
		text = wx.StaticText(self, -1, "Name               :", (1020, 70))
		text = wx.StaticText(self, -1, "Date Added     :", (1020, 90))
		text = wx.StaticText(self, -1, "Latest Visit       :", (1020, 110))
		text = wx.StaticText(self, -1, "Visit                  :", (1020, 130))
		text = wx.StaticText(self, -1, "Kepentingan   :", (1020, 150))
		text = wx.StaticText(self, -1, "Tanggal Rekom  :", (1020, 150))

		self.nameDatabaseRecog = wx.StaticText(self, -1, "Unknown", (1140, 70))
		self.dateAddedRecog = wx.StaticText(self, -1, "Unknown", (1140, 90))
		self.latestVisitDatabaseRecog = wx.StaticText(self, -1, "Unknown", (1140, 110))
		self.visitDatabaseRecog = wx.StaticText(self, -1, "Unknown", (1140, 130))
		self.kepentinganText = wx.StaticText(self, -1, "Unknown", (1140, 150))
		self.rekomendasiText = wx.StaticText(self, -1, "Unknown", (1140, 170))

		#end Recog
		#list Recognition
		self.dataOlv = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER, pos=(50, 20), size=(950, 250))
		#list candidates
		self.dataOlvCand = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER, pos=(1020, 270), size=(310, 200))
		self.dataMobilTampil = []
		#List Credit Digunakan
		labelCredit = wx.StaticText(self, -1, "Credit 2000 / Month", pos=(1020, 503))
		self.dataOlvCre = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER, pos=(1020, 520), size=(320,150))
		self.dataCredit = []
		self.btnRecog.Disable()

	def tambahData(self, e):
		ind = self.dataOlv.GetFirstSelected()
		if ind >= 0:
			self.item = self.dataOlv.GetItem(ind)
		print(ind)
		app = data_kendaraan.data_Kendaraan(self)
		app.Show(True)

	def kepentingan(self, e):
		hasil = kp.KepentinganFrame(self)
		hasil.Show(True)

	def start(self, e):
		self.capture = cv2.VideoCapture(0)
		videoFrame = wx.Panel(self, -1, pos=(50,280),size=(640,380))
		ShowCapture(videoFrame, self.capture)
		self.btnStart.Hide()
		self.btnStop.Show()
		self.btnRecog.Enable()
		self.pathp = ''
		
	def stop(self, e):
		self.btnStart.Show()
		self.btnStop.Hide()
		bitmap = wx.Bitmap(self.photoDefault)
		bitmap = scale_bitmap(bitmap, 640, 380)
		control = wx.StaticBitmap(self, -1, bitmap)
		control.SetPosition((50,280))
		self.btnRecog.Disable()
		
		self.capture.release()
	def openFile(self, e):
		openFileDialog = wx.FileDialog(self, "Open", "", "",
										"Image File (*.jpg, *.png)|*.jpg",
										wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

		openFileDialog.ShowModal()
		#Pake If kjklnjaksjdhkdj
		self.pathp = openFileDialog.GetPath()
		bitmap = wx.Bitmap(openFileDialog.GetPath())
		bitmap = scale_bitmap(bitmap, 640, 380)
		control = wx.StaticBitmap(self, -1, bitmap)
		control.SetPosition((50,280))
		openFileDialog.Destroy()
		self.btnRecog.Enable()
		
	def recognition(self, e):
		
		
		print(self.pathp)
		if self.pathp == '':
			self.ret, self.image = self.capture.read()
			print(self.ret)
			print(self.image)
			if os.path.exists("itemp\plate\plat1.jpg"):
				self.imageName = "itemp\plate\plat_{0}.jpg".format(int(time.time()))
				cv2.imwrite(self.imageName, self.image)
				self.jsonName = "itemp\json\json_{0}.json".format(int(time.time()))
				
			else:
				self.imageName = "itemp\plate\plat1.jpg"
				cv2.imwrite(self.imageName, self.image)
				self.jsonName = "itemp\json\json1.json"

			bitmap = wx.Bitmap(self.imageName)
			bitmap = scale_bitmap(bitmap, 280, 200)
			control = wx.StaticBitmap(self, -1, bitmap)
			control.SetPosition((720,420))
			IMAGE_PATH = self.imageName
		else:
			IMAGE_PATH = self.pathp
		SECRET_KEY = 'sk_42b18388bc96def5ad015425'
		with open(IMAGE_PATH, 'rb') as image_file:
			img_base64 = base64.b64encode(image_file.read())
		url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=id&secret_key=%s' % (SECRET_KEY)
		try:
			r = requests.post(url, data = img_base64)
		except Exception as e:

			print("Error: Kendaraan Tidak Ditemukan")
			return
		data_file = json.dumps(r.json(), indent=2)
		
		data = json.loads(str(data_file))
		hasil = data['results'][0]
		tanggalini = datetime.datetime.now()
		query = ("SELECT keterangan2, rekomendasi FROM tb_kunjungan WHERE plate = %s and tgl_kunjungan = %s")
		stmt = (hasil['plate'], "{0}".format(str(tanggalini)[:10]))
		datarek = connector.Execute(query, stmt, 4)
		hasilrek = datarek["Data"]
		print(hasilrek)
		if len(hasilrek) > 0:
			self.kepentinganText.SetLabel(str(hasilrek[0][0]))
			self.rekomendasiText.SetLabel(str(hasilrek[0][1]))
		else:
			self.kepentinganText.SetLabel("Belum Terdaftar")
			self.rekomendasiText.SetLabel("Belum Terdaftar")

		query = ("SELECT * FROM tb_member WHERE plate IN (%s)")
		stmt = (hasil['plate'])
		hasilSql = connector.Execute(query, stmt, 3)
		dataSql = hasilSql['Data']
		print(dataSql)
		if len(dataSql) > 0:
			self.dict = {"camera":"Camera 1", "time":str(datetime.datetime.now().time()), "merk":dataSql[0][5], "perusahaan":dataSql[0][6], "model":dataSql[0][7], "warna":dataSql[0][4], "tahun":dataSql[0][8], "plate":hasil['plate']}
		else:
			self.plateMobil = hasil['plate']
			self.warnaMobil = hasil["vehicle"]['color'][0]['name'].upper()
			self.merkMobil = hasil["vehicle"]['make_model'][0]['name'].upper(),
			self.perusahaanMobil = hasil["vehicle"]['make'][0]['name'].upper()
			self.tahunMobil = str(hasil["vehicle"]['year'][0]['name'])
			self.modelMobil = hasil["vehicle"]['body_type'][0]['name'].upper()
			self.dict = {"camera":"Camera 1", "time":str(datetime.datetime.now().time()), "merk":self.merkMobil, "perusahaan":self.perusahaanMobil, "model":self.modelMobil, "warna":self.warnaMobil, "tahun":self.tahunMobil, "plate":self.plateMobil}

		self.plateNumberPlat.SetLabel(hasil['plate'])
		self.text.SetLabel(hasil['plate'])
		if len(dataSql) > 0:
			tanggal = str(dataSql[0][2])
			self.nameDatabaseRecog.SetLabel(dataSql[0][1])
			self.dateAddedRecog.SetLabel("{0}".format(tanggal[:10]))
			self.latestVisitDatabaseRecog.SetLabel(str(dataSql[0][11]))

			

			query = ("SELECT * FROM tb_kunjungan WHERE plate IN (%s)")
			stmt = (hasil['plate'])
			jmlSql = connector.Execute(query, stmt, 3)
			datajmlh = jmlSql['Data']
			self.visitDatabaseRecog.SetLabel(str(len(datajmlh) + 1))

			query = ("INSERT INTO tb_kunjungan (plate, tgl_kunjungan) VALUES (%s, %s)")
			stmt = (dataSql[0][0], datetime.datetime.now())
			hasilSql = connector.Execute(query, stmt, 1)

			query = ("UPDATE tb_member SET latest_visit = %s WHERE plate = %s")
			stmt = (datetime.datetime.now(),dataSql[0][0])
			hasilSql = connector.Execute(query, stmt, 1)

			
		else:
			self.nameDatabaseRecog.SetLabel("Tidak Terdaftar")
			self.dateAddedRecog.SetLabel("Tidak Terdaftar")
			self.latestVisitDatabaseRecog.SetLabel("Hari Ini")
			self.visitDatabaseRecog.SetLabel("1")

			query = ("INSERT INTO tb_kunjungan (plate, tgl_kunjungan) VALUES (%s, %s)")
			stmt = (hasil['plate'], datetime.datetime.now())
			hasilSql = connector.Execute(query, stmt, 1)

		candidates = hasil['candidates']
		e = []
		for i in candidates:
		    Candidates = {'confidences': str(int(i['confidence']))+ " " + "%", 'plate':i['plate']}
		    e.append(Candidates)

		self.dataOlv.SetColumns([
				ColumnDefn("Camera", "left", 100, "camera"),
				ColumnDefn("Time", "left", 100, "time"),
				ColumnDefn("Plate", "left", 100, "plate"),
				ColumnDefn("Merk", "left", 100, "merk"),
				ColumnDefn("Perusahaan", "left", 102, "perusahaan"),
				ColumnDefn("Model", "left", 100, "model"),
				ColumnDefn("Warna", "left", 100, "warna"),
				ColumnDefn("Tahun", "left", 100, "tahun")
			])
		
		
		self.dataMobilTampil.append(self.dict)
		self.dataOlv.SetObjects(self.dataMobilTampil)


		self.dataOlvCand.SetColumns([
			ColumnDefn("Plate", 'left', 100, 'plate'),
			ColumnDefn("confidence", 'left', 100, 'confidences')
			])
		self.dataOlvCand.SetObjects(e)
		credit = {"credit": 2000, "digunakan": data['credits_monthly_used'], "sisa": 2000-int(data['credits_monthly_used'])}
		self.dataOlvCre.SetColumns([
			ColumnDefn("Credit", "left", 100, "credit"),
			ColumnDefn("Digunakan", "left", 100, "digunakan"),
			ColumnDefn("Sisa", "left", 100, "sisa")
			])
		self.dataCredit.append(credit)
		self.dataOlvCre.SetObjects(self.dataCredit)

		
class TabThree(wx.Panel):
	"""docstring for TabThree"""
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		wx.StaticText(self, -1, "Masukkan Nomor Plat", pos=(10, 10))
		self.TxtPlate = wx.TextCtrl(self, -1, pos=(10, 40))
		self.btnRecog = wx.Button(self, -1, "Recognize", pos=(10, 70), size=(110, 30))
		self.btnRecog.Bind(wx.EVT_BUTTON, self.recognize)

		#hasil Recog
		text = wx.StaticText(self, -1, "Nomor Plat     :", (200, 30))
		text = wx.StaticText(self, -1, "Daerah             :", (200, 50))

		self.plateNumberPlat = wx.StaticText(self, -1, "Unknown", (300, 30))
		daerahPlat = wx.StaticText(self, -1, "Unknown", (300, 50))
		
		
		#-----Database------
		text = wx.StaticText(self, -1, "Name               :", (200, 70))
		text = wx.StaticText(self, -1, "Date Added     :", (200, 90))
		text = wx.StaticText(self, -1, "Latest Visit       :", (200, 110))
		text = wx.StaticText(self, -1, "Visit                  :", (200, 130))
		text = wx.StaticText(self, -1, "Kepentingan   :", (200, 150))
		text = wx.StaticText(self, -1, "Tanggal Rekomendasi:  :", (200, 170))

		self.nameDatabaseRecog = wx.StaticText(self, -1, "Unknown", (300, 70))
		self.dateAddedRecog = wx.StaticText(self, -1, "Unknown", (300, 90))
		self.latestVisitDatabaseRecog = wx.StaticText(self, -1, "Unknown", (300, 110))
		self.visitDatabaseRecog = wx.StaticText(self, -1, "Unknown", (300, 130))
		self.kepentinganText = wx.StaticText(self, -1, "Unknown", (300, 150))
		self.rekomendasiText = wx.StaticText(self, -1, "Unknown", (340, 170))

		wx.StaticLine(self, -1, style=wx.HORIZONTAL, pos=(500, 20), size=(3, 200))
		wx.StaticText(self, -1, "Kepentingan", pos=(520, 20))

		self.keterangan = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, size=(300, 70), pos=(520 ,40))

		self.labeltglrekomendasi = wx.StaticText(self, -1, "Tanggal Rekomendasi", pos=(870, 20))
		self.tanggal = wx.adv.DatePickerCtrl(self, -1, pos=(870, 40), style = wx.adv.DP_DROPDOWN)

		self.labelket = wx.StaticText(self, -1, "Keterangan", pos=(870, 70))
		self.keteranganrek = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, size=(300, 70), pos=(870, 100))

		#wx.StaticLine(panel, -1, style=wx.VERTICAL, pos=(340, 10), size=(2, 200))
		self.button1 = wx.Button(self, -1, "Tambah", pos=(870, 210 ))
		self.button2 = wx.Button(self, -1, "Batal", pos=(970, 210))

		self.button1.Bind(wx.EVT_BUTTON, self.simpan)
		self.button2.Bind(wx.EVT_BUTTON, self.batal)
		#end Recog

		self.dataOlv = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER, pos=(20, 270), size=(1200, 400))

		self.dataOlv.SetColumns([
				ColumnDefn("Camera", "left", 100, "camera"),
				ColumnDefn("Time", "left", 100, "time"),
				ColumnDefn("Plate", "left", 100, "plate"),
				ColumnDefn("Merk", "left", 100, "merk"),
				ColumnDefn("Perusahaan", "left", 102, "perusahaan"),
				ColumnDefn("Model", "left", 100, "model"),
				ColumnDefn("Warna", "left", 100, "warna"),
				ColumnDefn("Tahun", "left", 100, "tahun")
			])
		

	def simpan(self, e):
		try:
			plate = self.TxtPlate.GetValue()
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
	def batal(self, e):
		pass
	def recognize(self, e):
		query = ("SELECT * FROM tb_member WHERE plate = %s")
		stmt = (self.TxtPlate.GetValue())
		hasil = connector.Execute(query, stmt, 3)
		dataSql = hasil["Data"]
		if len(dataSql) == 0:
			dlg = wx.MessageDialog(self, "Data Belum Ada", "Perhatian", wx.OK|wx.ICON_INFORMATION)
			dlg.ShowModal()


		if len(dataSql) > 0:
			self.dict = [{"camera":"Camera 1", "time":str(datetime.datetime.now().time()), "merk":dataSql[0][5], "perusahaan":dataSql[0][6], "model":dataSql[0][7], "warna":dataSql[0][4], "tahun":dataSql[0][8], "plate": self.TxtPlate.GetValue().upper()}]
			self.dataOlv.SetObjects(self.dict)
		tanggalini = datetime.datetime.now()
		query = ("SELECT keterangan2, rekomendasi FROM tb_kunjungan WHERE plate = %s and tgl_kunjungan = %s")
		stmt = (self.TxtPlate.GetValue(), "{0}".format(str(tanggalini)[:10]))
		datarek = connector.Execute(query, stmt, 4)
		hasilrek = datarek["Data"]
		print(hasilrek)
		if len(hasilrek) > 0:
			self.kepentinganText.SetLabel(hasilrek[0][0])
			self.rekomendasiText.SetLabel(str(hasilrek[0][1]))
		else:
			self.kepentinganText.SetLabel("Belum Terdaftar")
			self.rekomendasiText.SetLabel("Belum Terdaftar")

		
		platea = self.TxtPlate.GetValue()
		self.plateNumberPlat.SetLabel(self.TxtPlate.GetValue().upper())
		if len(dataSql) > 0:
			tanggal = str(dataSql[0][2])
			self.nameDatabaseRecog.SetLabel(dataSql[0][1])
			self.dateAddedRecog.SetLabel("{0}".format(tanggal[:10]))
			self.latestVisitDatabaseRecog.SetLabel(str(dataSql[0][11]))

			

			query = ("SELECT * FROM tb_kunjungan WHERE plate IN (%s)")
			stmt = (platea)
			jmlSql = connector.Execute(query, stmt, 3)
			datajmlh = jmlSql['Data']
			self.visitDatabaseRecog.SetLabel(str(len(datajmlh) + 1))

			query = ("INSERT INTO tb_kunjungan (plate, tgl_kunjungan) VALUES (%s, %s)")
			stmt = (dataSql[0][0], datetime.datetime.now())
			hasilSql = connector.Execute(query, stmt, 1)

			query = ("UPDATE tb_member SET latest_visit = %s WHERE plate = %s")
			stmt = (datetime.datetime.now(),dataSql[0][0])
			hasilSql = connector.Execute(query, stmt, 1)

			
		else:
			self.nameDatabaseRecog.SetLabel("Tidak Terdaftar")
			self.dateAddedRecog.SetLabel("Tidak Terdaftar")
			self.latestVisitDatabaseRecog.SetLabel("Hari Ini")
			self.visitDatabaseRecog.SetLabel("1")

			query = ("INSERT INTO tb_kunjungan (plate, tgl_kunjungan) VALUES (%s, %s)")
			stmt = (platea, datetime.datetime.now())
			hasilSql = connector.Execute(query, stmt, 1)


class ShowCapture(wx.Panel):
    def __init__(self, parent, capture, fps=24):
        wx.Panel.__init__(self, parent, wx.ID_ANY, (0,0), (640, 380))

        self.capture = capture
        ret, frame = self.capture.read()

        height, width = frame.shape[:2]

        parent.SetSize((width, height))

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.bmp = wx.Bitmap.FromBuffer(width, height, frame)

        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)


        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)




    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, event):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()
def scale_bitmap(bitmap, width, height):
	image = wx.ImageFromBitmap(bitmap)
	image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
	result = wx.BitmapFromImage(image)
	return result


		
def main():
	app = wx.App()
	plateRecognition(None)
	app.MainLoop()
main()
		
