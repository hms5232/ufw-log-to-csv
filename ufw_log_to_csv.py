# python3

"""
author: hms5232
source code on https://github.com/hms5232/ufw-log-to-csv
"""


def main():
	# try...expect...finally...
	# 用with資源會自動釋放
	with open('ufw.log', 'r', encoding='UTF-8') as f:
		ufw_logs = f.readlines()  # 逐行讀取並存入list
		with open('ufw_log.csv', 'a', encoding='UTF-8') as o:  # o of output
			log_items = ['IN', 'OUT', 'MAC', 'SRC', 'LEN']  #
			csv_title = '"月","日","時間","主機","unknown","動作","IN","OUT","來自(src)","LEN","TOS","PREC","TTL","ID","協定(PROTO)","SPT","DPT","WINDOW","RES","封包類型","URGP"\n'
			output = csv_title  # 輸出到csv的內容
			# 讀取每一筆紀錄
			for i in range(len(ufw_logs)):
				print("正在處理第", i+1, "筆資料")
				output = output + '"' + ufw_logs[i][0:3] + '",' + '"' + ufw_logs[i][4:6] + '",' + '"' + ufw_logs[i][7:16] + '",'  # 時間
				# TODO: kernel名稱另外這邊就先抓
				output = output + get_expect_time(ufw_logs[i])
			o.write(output)  # 寫入csv


# 抓取kernel之後的部分
def get_expect_time(log_string):
	log_string = log_string[16:]  # 把前面已經擷取的時間部分切掉
	result = ''  # 擷取出來的內容
	while len(log_string) != 1:  # 這筆紀錄還沒跑完
		# Re:從零開始
		starttag = 0
		endtag = 0
		# TODO: SYN沒有=
		if log_string.find('[') != -1:
			starttag = log_string.find('[')
			endtag = log_string.find(']')
			result = result + '"' + log_string[starttag+1:endtag] + '",'
			log_string = log_string[endtag+1:]
			continue
		elif log_string.find('=') != -1:
			starttag = log_string.find('=')
			endtag = log_string.find(' ')
			result = result + '"' + log_string[starttag+1:endtag] + '",'
			log_string = log_string[endtag+1:]
			continue
	result = result + ',\n'
	return result

if __name__ == '__main__':
	main()
