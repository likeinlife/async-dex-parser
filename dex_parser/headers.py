parse_chapter_headers = {
	'Host': 'api.mangadex.org',
	'User-Agent': 'MaganDexParser',
	'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
	'Accept-Encoding': 'gzip, deflate, br',
	'Access-Control-Request-Method': 'POST',
	'Access-Control-Request-Headers': 'xlb-route',
	'Referer': 'https://mangadex.org/',
	'Origin': 'https://mangadex.org',
	'DNT': '1',
	'Connection': 'keep-alive',
	'Sec-Fetch-Dest': 'empty',
	'Sec-Fetch-Mode': 'cors',
	'Sec-Fetch-Site': 'same-site',
	'Sec-GPC': '1',
}
parse_chapter_params = {
	'forcePort443': 'false',
}

get_image_headers = {
	'User-Agent': 'MangaDexParser',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
	'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
	# 'Accept-Encoding': 'gzip, deflate, br',
	'DNT': '1',
	'Alt-Used': 'uploads.mangadex.org',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1',
	'Sec-Fetch-Dest': 'document',
	'Sec-Fetch-Mode': 'navigate',
	'Sec-Fetch-Site': 'none',
	'Sec-Fetch-User': '?1',
	'Sec-GPC': '1',
}
title_headers = {
	'User-Agent': 'MangaDexParser',
	'Accept': 'application/json, text/plain, */*',
	'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
	# 'Accept-Encoding': 'gzip, deflate, br',
	'Referer': 'https://mangadex.org/',
	'Origin': 'https://mangadex.org',
	'DNT': '1',
	'Connection': 'keep-alive',
	'Sec-Fetch-Dest': 'empty',
	'Sec-Fetch-Mode': 'cors',
	'Sec-Fetch-Site': 'same-site',
	'Sec-GPC': '1',
}
