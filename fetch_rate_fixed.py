from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
import os

# 設定絕對路徑
folder_path = r"D:\台灣失業人口"
chrome_driver_path = os.path.join(folder_path, "chromedriver.exe")
output_json = os.path.join(folder_path, "data.json")

# 啟動瀏覽器
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# 開啟網站
driver.get("https://www.stat.gov.tw/Point.aspx?sid=t.3&n=3582&sms=11480")

# ✅ 等待「失業率」文字出現在頁面
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '失業率')]"))
)

# 抓渲染後的 HTML
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# 搜尋失業率欄位（排除季節調整）
rate = "無資料"
for tr in soup.find_all("tr"):
    tds = tr.find_all("td")
    if tds and "失業率" in tds[0].text and "季節" not in tds[0].text:
        rate = tds[1].text.strip().split("（")[0]
        break

# 輸出為 JSON
with open(output_json, "w", encoding="utf-8") as f:
    json.dump({"unemployment_rate": rate}, f, ensure_ascii=False)

print("✅ 成功擷取失業率：", rate)
print("📁 已儲存至：", output_json)
