import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select


def crawler(id, pw):
    driver = webdriver.Chrome(
        '/Users/dain/Downloads/chromedriver_win32/chromedriver')

    # 3초 지연
    driver.implicitly_wait(3)
    driver.get('https://apply.likelion.org/accounts/login/?next=/apply/')

    # 로그인
    driver.find_element_by_name('username').send_keys(id)
    driver.find_element_by_name('password').send_keys(pw)

    driver.find_element_by_xpath(
        '/html/body/main/div[2]/div/div/div/form/div[3]/button').click()

    # 지원자 접수 번호 리스트
    univ_num = id.split("@")[0]
    driver.get(f'https://apply.likelion.org/apply/univ/{univ_num}')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    applicant_num_list = []

    for link in soup.select('#likelion_num > div.applicant_page > a'):
        applicant_num_list.append(link.attrs['href'].split('/')[3])

    # 지원자별 정보 크롤링
    result = [['applicant_num', 'name', 'year', 'faculty', 'phone',
               'email', 'link', 'file', 'first', 'second', 'third']]
    for applicant_num in applicant_num_list:
        driver.get(
            f'https://apply.likelion.org/apply/applicant/{applicant_num}')

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.select_one(
            '#likelion_num > div.col-md-6.col-xs-12.text-left.applicant_detail_page > h3').text
        year = soup.select_one(
            '#likelion_num > div:nth-child(2) > div:nth-child(1) > p:nth-child(1)').text
        faculty = soup.select_one(
            '#likelion_num > div:nth-child(2) > div:nth-child(1) > p:nth-child(3)').text
        phone = soup.select_one(
            '#likelion_num > div:nth-child(2) > div.row.s_mt > p:nth-child(1)').text
        email = soup.select_one(
            '#likelion_num > div:nth-child(2) > div.row.s_mt > p:nth-child(3)').text

        link = soup.select_one('#likelion_num > div:nth-child(4) > div').text
        try:
            file = soup.select_one(
                '#likelion_num > div:nth-child(6) > div > a').attrs['href']
        except:
            file = None
        first = soup.select_one(
            'body > div.answer_view > div > div:nth-child(1) > div.row.m_mt > div').text
        second = soup.select_one(
            'body > div.answer_view > div > div:nth-child(2) > div.row.m_mt > div').text
        third = soup.select_one(
            'body > div.answer_view > div > div:nth-child(3) > div.row.m_mt > div').text

        result.append(
            [applicant_num, name, year, faculty, phone, email, link, file, first, second, third])

        # 서류 접수 : 0 서류 탈락 : 1 서류 합격 : 2 면접 탈락 : 3 최종 합격 : 4
        Select(driver.find_element_by_name(
            'applicant_state')).select_by_value('0')
        driver.find_element_by_xpath(
            '//*[@id="likelion_num"]/div/div/div[1]/form/div[2]/button').click()

    return(result)
