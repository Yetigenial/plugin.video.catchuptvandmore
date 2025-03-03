# -*- coding: utf-8 -*-
# Copyright: (c) 2022, itasli
# GNU General Public License v2.0+ (see LICENSE.txt or https://www.gnu.org/licenses/gpl-2.0.txt)

# This file is part of Catch-up TV & More

from __future__ import unicode_literals
import json

from codequick import Resolver
import urlquick

from resources.lib import resolver_proxy


URL_LIVE = {
    'showtv': 'https://www.showtv.com.tr/canli-yayin',
    'showturk': 'https://www.showturk.com.tr/canli-yayin',
    'showmax': 'http://showmax.com.tr/canliyayin',
    'haberturk': 'https://www.haberturk.com/canliyayin',
    'bloomberght': 'https://www.bloomberght.com/tv',
}


@Resolver.register
def get_live_url(plugin, item_id, **kwargs):

    resp = urlquick.get(URL_LIVE[item_id])
    root = resp.parse()

    if item_id == 'bloomberght':
        dict = json.loads(root.findall(".//div[@class='htplay_video']")[1].attrib['data-ht'])
    else:
        dict = json.loads(root.findall(".//div[@class='htplay_video']")[0].attrib['data-ht'])

    video_url = dict['ht_stream_m3u8']

    return resolver_proxy.get_stream_with_quality(plugin, video_url, manifest_type="hls")
