import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR,
    EXPECTED_STATUS,
    MAIN_DOC_URL,
    MAIN_PEP_URL,
    PATTERN_PYTHON_VERSION_STATUS,
    PATTERN_ZIP_A4,
)
from exceptions import ParserFindTagException
from outputs import control_output
from utils import find_tag, get_pep_status, get_response


def whats_new(session):
    def postprocessing(tag):
        return tag.text.replace("\n", " ").strip("¶ \r\t")

    whats_new_url = urljoin(MAIN_DOC_URL, "whatsnew/")
    response = get_response(session, whats_new_url)
    soup = BeautifulSoup(response.text, features="lxml")
    articles = (
        urljoin(whats_new_url, link.a["href"])
        for link in find_tag(soup, "div", {"class": "toctree-wrapper compound"}).find_all(class_="toctree-l1")
    )
    result = [("Ссылка на статью", "Заголовок", "Редактор, Aвтор")]
    for url in tqdm(articles, desc="Обработка URL адресов статей о Python-е."):
        soup = BeautifulSoup(get_response(session, url).text, features="lxml")
        h1_tag, dl_tag = find_tag(soup, tag="h1"), find_tag(soup, tag="dl")
        result.append((url, postprocessing(h1_tag), postprocessing(dl_tag)))
    return result


def latest_versions(session):
    def link_parser(tag, regexp):
        match = re.search(regexp, str(tag))
        version = match.group(1) or match.group(3)
        status = match.group(2) or match.group(4)
        return (tag.get("href"), version, status)

    results = [("Ссылка на документацию", "Версия", "Статус")]
    response = get_response(session, MAIN_DOC_URL)
    soup = BeautifulSoup(response.text, features="lxml")
    tag_version_links = find_tag(soup, "div", {"class": "sphinxsidebarwrapper"}).find_all(
        "a", text=re.compile(PATTERN_PYTHON_VERSION_STATUS)
    )
    results.extend(link_parser(link, PATTERN_PYTHON_VERSION_STATUS) for link in tag_version_links)
    if not results:
        error_msg = "Не найдена ни одна ссылка."
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, "download.html")
    response = get_response(session, downloads_url)
    soup = BeautifulSoup(response.text, features="lxml")
    main_tag = find_tag(soup, "div", {"role": "main"})
    table_tag = find_tag(main_tag, "table", {"class": "docutils"})
    a_tag = find_tag(table_tag, "a", {"href": re.compile(PATTERN_ZIP_A4)})
    if not a_tag:
        error_msg = "Ссылка для скачивания не найдена."
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    pdf_a4_link = a_tag["href"]
    filename = pdf_a4_link.split("/")[-1]
    if not pdf_a4_link.startswith("http"):
        pdf_a4_link = urljoin(downloads_url, pdf_a4_link)
    downloads_dir = BASE_DIR / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = get_response(session, pdf_a4_link)
    with open(archive_path, "wb") as file:
        file.write(response.content)
    logging.info("Архив был загружен и сохранён: %s", archive_path)


def pep(session):
    def get_link(tag):
        link = find_tag(tag, "a")["href"]
        if not link.startswith("http"):
            link = urljoin(MAIN_PEP_URL, link)
        return link

    def tr_preprocessing(tag):
        td_tag = tag.find_all("td")
        char = td_tag[0].text[1:2]
        return EXPECTED_STATUS.get(char, [char]), get_link(td_tag[1])

    response = get_response(session, MAIN_PEP_URL)
    soup = BeautifulSoup(response.text, features="lxml")
    pep_index = find_tag(soup, tag="section", attrs={"id": "numerical-index"})
    pep_tr_list = find_tag(pep_index, tag="tbody").find_all("tr")
    result = [("Статус PEP", "Количество")]
    pep_status = {}
    for pep_tr in tqdm(pep_tr_list, desc="Обработка списка PEP"):
        status = get_pep_status(session, *tr_preprocessing(pep_tr))
        pep_status[status] = pep_status.get(status, 0) + 1
    result.extend(zip(pep_status.keys(), pep_status.values()))
    result.append(("Всего:", len(pep_tr_list)))
    return result


MODE_TO_FUNCTION = {
    "whats-new": whats_new,
    "latest-versions": latest_versions,
    "download": download,
    "pep": pep,
}


def main():
    configure_logging()
    logging.info("Парсер запущен!")
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info("Аргументы командной строки: %s", args)
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    results = MODE_TO_FUNCTION[args.mode](session)
    if results:
        control_output(results, args)
    logging.info("Парсер завершил работу.")


if __name__ == "__main__":
    main()
