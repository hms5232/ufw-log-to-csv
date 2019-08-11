# ufw-log-to-csv

## 緣起　Introduction
在啟用[UFW（Uncomplicated Firewall）](https://zh.wikipedia.org/wiki/Uncomplicated_Firewall)後有時候會打開防火牆產生的日誌看看，但看幾次總覺得原生出來的不太容易閱讀或統計之類的，因此動手寫了一個小程式來幫忙轉成csv。

## 使用說明　Manual
※關於紀錄中各項目代表的意思可參見 https://askubuntu.com/questions/1116145/understanding-ufw-log 。  
請將`ufw_log_to_csv.py`和`ufw.log`放在同個目錄下（可將log複製出來或將`ufw_log_to_csv.py`放進去，推薦前者）後執行：  

    cd [檔案所在位置]
    py ufw_log_to_csv.py

之後程式會自己尋找`ufw.log`這個檔案並輸出成`ufw_log.csv`（可自行替換程式碼中輸出和輸入的檔名以符合自己需求）

## 已知問題　Known issues
1. 在 ID 和 PROTO 兩個欄位之間有時會出現[「DF」（don't fragment）](https://askubuntu.com/questions/143371/what-do-ufws-audit-log-entries-mean)導致部分紀錄的欄位歪掉
2. 在封包類型（倒數第二項資料，例如：SYN）這欄中有時會不只有一種封包，導致欄位歪掉。例如：`ACK PSH`或`CWR ECE SYN`等


## 許可　License
請見 [LICENSE](https://github.com/hms5232/ufw-log-to-csv/blob/master/LICENSE) 頁面。
  
See [LICENSE](https://github.com/hms5232/ufw-log-to-csv/blob/master/LICENSE).
