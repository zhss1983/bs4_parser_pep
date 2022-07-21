import logging

from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = "utf-8"
        return response
    except RequestException as exc:
        logging.exception("Возникла ошибка при загрузке страницы %s", url, stack_info=True)
        raise RequestException from exc


def find_tag(soup, tag=None, attrs=None):
    searched_tag = soup.find(name=(tag or []), attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f"Не найден тег {tag} {attrs}"
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def get_pep_status(session, pep_status, pep_url):
    response = get_response(session, pep_url)
    soup = BeautifulSoup(response.text, features="lxml")
    pep_status_table = find_tag(soup, "dl", {"class": "rfc2822 field-list simple"})
    status = pep_status_table.find("dt", text="Status")
    status = status.find_next_sibling("dd").text
    if status not in pep_status:
        error_msg = (
            f"Несовпадающие статусы:\n{pep_url}\nСтатус в карточке: " f"{status}\nОжидаемые статусы: {pep_status}"
        )
        logging.error(error_msg)
    return status
