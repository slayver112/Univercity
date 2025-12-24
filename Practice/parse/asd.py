import os
import csv
import urllib.request
import re


class parsing_site:
    def __init__(self,name: str,location: str,phone_number: str,working_hour: str = 'Отсутствует',website: str = ''):
        self.name = name
        self.location = location
        self.phone_number = phone_number
        self.working_hour = working_hour
        self.website = website

    def _arr_info(self):
        return [self.name,self.location,self.phone_number,self.working_hour,self.website]

    @staticmethod
    def csv_writer(centers):
        headers = ['Имя','Адрес','Телефон','Часы','Ссылка на сайт']
        file_exists = os.path.exists('answer/spravochnik.csv')
        if not file_exists:
            os.makedirs(os.path.dirname('answer/spravochnik.csv'), exist_ok=True)
        with open('answer/spravochnik.csv', mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='-')
            if not file_exists:
                writer.writerow(headers)
            for center in centers:
                writer.writerow(center._get_data())


def request_realization():
    url = 'https://msk.spravker.ru/avtoservisy-avtotehcentry/'
    auto_centers = []
    main_pattern = r'(?s)<div class="widgets-list__item">(.*?)(?=<div class="widgets-list__item">|$)'
    name_p = r'class="org-widget-header__title-link">(.*?)</a>'
    addr_p = r'meta--location">\s*(.*?)\s*</span>'
    phone_p = r'Телефон</span>.*?class="spec__value">(.*?)</dd>'
    hours_p = r'Часы работы</span>.*?class="spec__value">(.*?)</dd>'
    site_p = r'Сайт</span>.*?data-url="([^"]+)"'
    with urllib.request.urlopen(url) as response:
        html_content = response.read().decode('utf-8')
    unions = re.findall(main_pattern, html_content)
    for union in unions:
        name = re.search(name_p, union, re.DOTALL)
        address = re.search(addr_p, union, re.DOTALL)
        phone = re.search(phone_p, union, re.DOTALL)
        hours = re.search(hours_p, union, re.DOTALL)
        site_match = re.search(site_p, union, re.DOTALL)
        site_url = 'Отсутствует'
        if site_match:
            data_url = site_match.group(1).strip()
            site_url = data_url.replace('&amp;', '&')
        auto_center = parsing_site(
            name=name.group(1).strip() if name else 'Отсутствует',
            location=address.group(1).strip() if address else 'Отсутствует',
            phone_number=phone.group(1).strip() if phone else 'Отсутствует',
            working_hour=hours.group(1).strip() if hours else 'Отсутствует',
            website=site_url
        )
        auto_centers.append(auto_center)
    return auto_centers


def in_csv(centers):
    parsing_site.csv_writer(centers)


def main():
    centers = request_realization()
    in_csv(centers)


if __name__ == '__main__':
    main()