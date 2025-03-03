# -*- coding: utf-8 -*-
# Copyright: (c) 2017, SylvainCecchetto
# GNU General Public License v2.0+ (see LICENSE.txt or https://www.gnu.org/licenses/gpl-2.0.txt)

# This file is part of Catch-up TV & More

from __future__ import unicode_literals
import re

from codequick import Script
import urlquick

from codequick import Listitem, Route
# noinspection PyUnresolvedReferences
from codequick import Resolver
from resources.lib import resolver_proxy, web_utils


# TODO
# Replay add emissions
# Add info LIVE TV

URL_ROOT = 'http://www.dw.com'


@Resolver.register
def get_live_url(plugin, item_id, **kwargs):
    final_language = kwargs.get('language', Script.setting['dw.language'])

    video_url = ''
    resp = urlquick.get(URL_ROOT + '/%s' % final_language.lower())
    list_lives_datas = re.compile(r'name="file_name" value="(.*?)"').findall(
        resp.text)

    for live_datas in list_lives_datas:
        if 'm3u8' in live_datas:
            video_url = live_datas
    return resolver_proxy.get_stream_with_quality(plugin, video_url, manifest_type="hls")
