from selenium import webdriver

from models import TranslationGummy

# options = webdriver.ChromeOptions()
# options.add_argument("--ignore-certificate-errors")


# driver = webdriver.Chrome(chrome_options=options)
# driver.get("https://www.python.org")
# is_success = driver.save_screenshot("screenshot.png")
# print(is_success)


print("hoge")
gummy = TranslationGummy(gateway="useless", translator="deepl")
pdfpath = gummy.toPDF(url="https://www.nature.com/articles/ncb0800_500", path="sample.pdf", delete_html=True)
print(pdfpath)
