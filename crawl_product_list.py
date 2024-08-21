from playwright.sync_api import sync_playwright
import csv
import time
from bs4 import BeautifulSoup

def crawl_suncushion_list_html(playwright_page, page):
    url = f"https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100110003&fltDispCatNo=&prdSort=03&pageIdx={page}&rowsPerPage=24&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100110003_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%EC%84%A0%EC%8A%A4%ED%8B%B1&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd="
    playwright_page.goto(url)
    time.sleep(3)
    html = playwright_page.content()
    return html

def parse_suncushion_list(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select(".prd_info")
    data = []
    for item in items:
        brand = item.select_one(".tx_brand").get_text(strip = True)
        name = item.select_one(".tx_name").get_text(strip = True)
        link = item.select_one("a")["href"]

        data.append({
            "product_brand" : brand,
            "product_name" : name,
            "product_link" : link
        })
    return data

def write_data(data):
    with open("./data/sunstick_sales_list.csv", "w") as fw:
        writer = csv.DictWriter(fw, fieldnames=["product_name", "product_brand", "product_link"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    num_pages = 2
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        playwright_page = browser.new_page()
        total_data = []
        for i in range(num_pages):
            html = crawl_suncushion_list_html(playwright_page, i+1)
            data = parse_suncushion_list(html)
            total_data.extend(data)
    write_data(total_data)
    print("collected:", len(total_data))