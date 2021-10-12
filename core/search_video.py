# (c) @AbirHasan2005

import requests
from urllib import parse
from typing import Union
from core.get_cookies import (
    get_cookies,
    set_cookies
)
from core.login import pdisk_login

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
search_api = "https://www.pdisk.net/api/video/search-my-video?dir_id=0&item_id=&title={}&pageSize=10&pageNo=1&desc=&status=&sortField=ctime&sortAsc=0&needDirName=true"


async def search_pdisk_videos(query: str, username: str, password: str) -> Union[dict, Exception]:
    try:
        cookies = await get_cookies(username, password)
        response = requests.get(search_api.format(parse.quote(query)), cookies={"Cookie": cookies}, headers={"User-Agent": user_agent})
        data = response.json()
        if data["msg"] == "Please login again":
            user_id, cookies = await pdisk_login(username, password)
            await set_cookies({
                "username": username,
                "password": password,
                "user_id": user_id,
                "cookies": cookies
            })
            return await search_pdisk_videos(query, username, password)
        else:
            return data
    except Exception as error:
        print(error)
        return error
