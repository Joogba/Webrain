from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import bs4
import sys
import time

#멘더빌리티 로그인
def login(user_name, user_password):
    driver.find_element_by_xpath('//input[@tabindex="1"]').send_keys(user_name)

    driver.find_element_by_xpath('//input[@tabindex="2"]').send_keys(user_password)

    driver.find_element_by_xpath('//a[@tabindex="4"]').click()

# 워크시트 체크
def check_worksheet(cbx1, cbx2, cbx3, cbx4, cbx5, cbx_All = False, cbx_None = False):
    driver.find_element_by_id('didNone').click()

    if cbx_All is True and cbx_None is False:
        driver.find_element_by_id('didAll')
        return

    if cbx_None is True and cbx_All is False:
        driver.find_element_by_id('didNone')
        return

    if cbx1 is True:
        driver.find_element_by_id('cbx11').click()
    if cbx2 is True:
        driver.find_element_by_id('cbx12').click()
    if cbx3 is True:
        driver.find_element_by_id('cbx13').click()
    if cbx4 is True:
        driver.find_element_by_id('cbx14').click()
    if cbx5 is True:
        driver.find_element_by_id('cbx15').click()

    driver.find_element_by_class_name('finishTestBadge').click()

# 프로그레스 테스트 소제목 크롤링
def get_progress_test_small_title():
    for a in driver.find_elements(By.XPATH, '//div[@class="testH"]/span'):
        print(a.text)

def get_question_category_text():
    header_div = driver.find_element_by_xpath('//div[@aria-expanded="true"]')
    text = header_div.find_element_by_xpath('div/div/div/span').text

    if len(text) == 0:
        return 'no smalltitle'
    else:
        return text

# 소제목마다 질문 리스트 얻기
def get_progress_test_question_list(category_number):
    question_category = get_question_category_text()
    for a in driver.find_elements_by_class_name('testformBg'):
        question_td_list = a.find_elements(By.XPATH, 'td') # 질문정보 0~3 (text~moreinfo)

        if len(question_td_list[0].text) is 0: # text 길이가 0이면 아무것도안함
            continue

        progress_question_information['id_num'].append(int(question_td_list[0].get_attribute('id')[8:]))
        progress_question_information['text'].append(question_td_list[0].text)
        progress_question_information['question_category'].append(question_category)
        progress_question_information['frequency'].append(question_td_list[2]) # 빈도입력 tr
        progress_question_information['question_category_number'].append(category_number)

def click_open_question_get_list_button(): # 질문 열고 정보 얻기
    count = 0
    for a in driver.find_elements_by_xpath('//div[@role="tab"]'):
        a.click()
        driver.implicitly_wait(2)
        time.sleep(2)
        get_progress_test_question_list(count)
        count += 1

def print_question_info(): # 질문 정보 출력
    small = 'a'

    for i in range(len(progress_question_information['text'])):
        if small != progress_question_information['question_category'][i]:
            small = progress_question_information['question_category'][i]
            print(' ')
            print(small, '=======', progress_question_information['question_category_number'][i])

        print(progress_question_information['text'][i])
        print(progress_question_information['id_num'][i])
        print(progress_question_information['question_category_number'][i])

def click_frequency_button(frequency_list): #빈도 입력
    question_count = 0
    for a in driver.find_elements_by_xpath('//div[@role="tab"]'): # 탭열고 클릭
        a.click()
        driver.implicitly_wait(1)
        time.sleep(1)

        for a in driver.find_elements_by_class_name('testformBg'):
            question_td_list = a.find_elements(By.XPATH, 'td')  # 질문정보 0~3 (text~moreinfo)

            if len(question_td_list[0].text) is 0:  # text 길이가 0이면 아무것도안함
                continue

            path = 'div[%d]' % question_list[question_count]
            question_td_list[2].find_element_by_xpath(path).click()
            question_count += 1

if __name__ == "__main__":

    progress_question_information = {'text' : [], 'id_num' : [], 'frequency' : [],
                                     'question_category' : [], 'question_category_number' :[]}
    question_list = [4 for _ in range(200)]

    driver = webdriver.Chrome('chromedriver')

    driver.get('https://app2.mendability.com/Members/Default.aspx')

    login('moohanit@naver.com', 'tomato0803')

    driver.find_element_by_id('ProgerssPanel1_worksheetButton1_imgBtnNewTest').click()

    driver.implicitly_wait(5)

    check_worksheet(False,True,True,False,False)

    click_open_question_get_list_button()

    print_question_info()

    click_frequency_button(question_list)

