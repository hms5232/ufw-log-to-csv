#!/usr/bin/python3
# file encoding=utf-8

"""
author: hms5232
source code on https://github.com/hms5232/ufw-log-to-csv
"""


import datetime


def main():
	# try...expect...finally...
	# 用 with 資源會自動釋放
	# ※※ >>>  ↓↓↓↓↓↓↓ change input filename here if you want <<< ※※
	with open('ufw.log', 'r', encoding='UTF-8') as f:
		ufw_logs = f.readlines()  # 逐行讀取並存入 list
		now_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # 取得現在時間並格式化
		# ※※ >>>  ↓↓↓↓↓↓↓↓↓↓↓ change output filename here if you want <<< ※※
		with open("ufw"+now_time+".csv", 'a', encoding='UTF-8') as o:  # o of "output"
			csv_title = '"月","日","時間","主機名稱","kernel 時間","動作","IN","OUT","MAC", "來自(src)", "DST", "LEN","TOS","PREC","TTL","ID","協定(PROTO)","來源埠(SPT)","DPT","WINDOW","RES","Control Bits / flags","URGP"\n'
			output = csv_title  # 輸出到 csv 的內容
			# 讀取每一筆紀錄
			for i in range(len(ufw_logs)):
				print("正在處理第", i+1, "筆紀錄...", end='\r')
				output = output + '"' + ufw_logs[i][0:3] + '",' + '"' + ufw_logs[i][4:6] + '",' + '"' + ufw_logs[i][7:16] + '",'  # 時間
				output = output + get_kernel_name(ufw_logs[i])  # kernel名稱另外這邊就先抓
				output = output + get_expect_time(ufw_logs[i])

			o.write(output)  # 寫入csv
			print(end='\n\n')  # 讓之前 print 出來的東西不會被覆蓋（\r\n）順便排版


# 抓取 kernel 之後的部分
def get_expect_time(log_string):
	log_string = log_string[16:]  # 把前面已經擷取的時間部分切掉
	result = ''  # 擷取出來的內容
	while len(log_string) > 2:  # 這筆紀錄還沒跑完
		# Re:從零開始
		starttag = 0
		endtag = 0
		if log_string.find('[') != -1:  # 先抓有[]的
			starttag = log_string.find('[')
			endtag = log_string.find(']')
			result = result + '"' + log_string[starttag+1:endtag] + '",'
			log_string = log_string[endtag+1:]  # 去掉]後從空格開始
		elif log_string.find(' ') != -1:  # 再抓剩下的
			# TODO: 竟然有個什麼DF的害我欄位歪掉不說還要另外寫判斷
			starttag = log_string.find(' ')
			log_string_tmp = log_string[starttag+1:]
			endtag = log_string_tmp.find(' ') + 1
			# 如果是有=的話就只抓=後面的部分
			ptr_equal = log_string[starttag+1:endtag].find('=')
			# 因為在RES之後flag有可能不只一個，所以在RES之後到URGP之間通通抓出來
			isRES = False
			if ptr_equal != -1:  # 有=
				if log_string[starttag+1:ptr_equal+1] == "RES":
					isRES = True
				starttag = log_string.find('=')
			result = result + '"' + log_string[starttag+1:endtag] + '",'

			log_string = log_string[endtag:]  # 保留空格不切掉
			if isRES:
				# 抓取RES後面剩下的項目到URPG之前(control flags)
				tmp_index = 0
				# 擷取control flags和之後的內容
				tmp = log_string[1:].split(" ")  # 將剩下的字串用空格來分割並放進list
				while True:
					if tmp[tmp_index].find("=") >= 0:  # 如果發現=，代表已經擷取完畢了
						break
					tmp_index += 1
				S = ""
				for s in tmp[:tmp_index]:  # 開始拿出每個control flags
					S += s+"|"
				S = S[:-1]  # 拿掉最後一個|
				result = result + '"' + S + '",'
				# 將剩下的部分依照原本的邏輯處理
				ptr = log_string.find("=")
				while True:
					ptr -= 1
					if log_string[ptr] == " ":
						break
				log_string = log_string[ptr:]
				
				
	result = result + '\n'  # 一筆紀錄處理完了記得換行
	return result


# 擷取 kernel 的名字
def get_kernel_name(log_string):
	kernel_name = ''
	kernel_tag = 0
	if log_string.find('kernel') != -1:
		kernel_name = '"' + log_string[16:log_string.find('kernel')] + '",'
	return kernel_name


if __name__ == '__main__':
	main()
