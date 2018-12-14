import mysql.connector as cnx

data = {}
def Execute(query, stmt, pilihan):
	try:
		connect = cnx.connect(user='root', password='root', host='localhost', database='plate_recognition')
		cursor = connect.cursor(prepared=True)
		if stmt != '' and pilihan == 1:
			cursor.execute(query, stmt)
			connect.commit()
		elif stmt != '' and pilihan == 2:
			cursor.execute(query)
			data['Data'] = cursor.fetchall()
			return data
		elif stmt != '' and pilihan == 3:
			cursor.execute(query, (stmt,))
			data['Data'] = cursor.fetchall()
			return data
		else:
			cursor.execute(query, stmt)
			data['Data'] = cursor.fetchall()
			return data
	except Exception as e:
		string = 'Koneksi Gagal'
		print("Error :", e)
		return string



