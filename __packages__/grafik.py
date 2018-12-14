import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib import style
import connector as connector
import datetime



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
    	ys.append(int(row[0]))
    query = ("SELECT count(a.plate), a.tgl_kunjungan FROM tb_kunjungan as a, tb_member as b WHERE a.plate = b.plate and b.jenis='motor' GROUP BY a.tgl_kunjungan")
    stmt = ''
    hasil = connector.Execute(query, stmt, 4)
    for row in hasil["Data"]:
    	xs2.append(str(row[1]))
    	zs.append(int(row[0]))
    
    dates1 = [datetime.datetime.strptime(s, '%Y-%m-%d').date() for s in xs]
    dates2 = [datetime.datetime.strptime(s, '%Y-%m-%d').date() for s in xs2]


    
    ax1.clear()
    ax1.plot(dates2, zs, label="Motor", lw=2, marker='o')
    ax1.plot(dates1, ys, label="Mobil", lw=2, marker='s')
    ax1.legend(loc='best')
    ax1.set_ylabel("Jumlah Kendaraan")
    hfmt = mdates.DateFormatter('%d %b')
    ax1.xaxis.set_major_formatter(hfmt)
    ax1.xaxis.set_major_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.suptitle('Grafik Kendaraan')

plt.show()
