from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

class Job:
    def __init__(self,name) -> None:
        self.name=name
    def open_chrome(self):
        chrome_driver_path = r"F:\python3.11\chromedriver.exe"
        options = Options()
        options.headless = False
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    def give_me_job(self):
        driver=self.open_chrome()
        driver.get("https://www.zhipin.com/beijing/?seoRefer=index")
        wait = WebDriverWait(driver, 10)
        time.sleep(2)
        search_box = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ipt-search')))
        search_box.send_keys(self.name)

        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-search"]')))
        driver.execute_script("arguments[0].click();", search_button)

        for t in range(100):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                # jobs=driver.find_elements(By.CLASS_NAME,'text-cut')
                # sals=driver.find_elements(By.CLASS_NAME,'right-salary text-cut')
                # coms=driver.find_elements(By.CLASS_NAME,'left-detail-company text-cut')
                # texs=driver.find_elements(By.CLASS_NAME,'left-detail-nature text-cut')
                # dets=driver.find_elements(By.CLASS_NAME,'left-tag')
                get_element_texts_by_class = lambda class_name: [element.text for element in driver.find_elements(By.CLASS_NAME, class_name)]
                get_element_texts_by_xpath = lambda xpath: [element.text for element in driver.find_elements(By.XPATH, xpath)]

                # //*[@id="list"]/div[1]/div[1]/a/div/div[1]/div[1]/div/div
                jobs = get_element_texts_by_xpath('//span[@class="job-name"]')
                sals = get_element_texts_by_xpath('//span[@class="salary"]')
                coms = get_element_texts_by_xpath('//a[@ka="search_list_company_1_custompage"]')
                nars = get_element_texts_by_xpath('//ul[@class="tag-list"]/li[1]')
                dets = get_element_texts_by_class('info-desc')

                print("Jobs:", jobs,len(jobs))
                print("Salaries:", sals,len(sals))
                print("Companies:",coms,len(coms))
                print("Nature of Jobs:",nars, len(nars))
                print("Details:", dets,len(dets))

                data_length = len(jobs)
                csv_file = rf'{self.name}.csv'
                def dt(d,i):
                    return d[i] if i < data_length else ''
                with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    # writer.writerow(['Job', 'Salary', 'Company', 'Nature', 'Details'])
                    for i in range(data_length):
                        try:
                            writer.writerow([jobs[i], dt(sals, i), dt(coms, i),dt(nars, i),dt(dets, i)])
                        except:
                            continue
                with open(f'{self.name}.txt','a') as tt:
                    tt.write('\n'.join(','.join(e for e in lst) for lst in [jobs,sals,coms,nars,dets]))
                print(f"{csv_file} for {t+1} is ok.")
                time.sleep(2)
                # driver.find_element(By.CLASS_NAME, 'btn-next').click()
                try:
                    button = driver.find_element(By.CLASS_NAME, 'ui-icon-arrow-right')
                    driver.execute_script("arguments[0].click();", button)
                except:
                    # wait = WebDriverWait(driver, 10)
                    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-icon-arrow-right")))
            except Exception as e:
                print(f'{e}:{t+1}')
                continue

        driver.quit()

if __name__=='__main__':
    # Law=Job('法务')
    # Data=Job('数据')
    # Law.give_me_job()
    # Data.give_me_job()
