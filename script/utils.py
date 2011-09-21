# -*- coding: utf-8 -*-
import htmlentitydefs
import re
 
# 実体参照 & 文字参照を通常の文字に戻す
def htmlentity2unicode(text):
    """
    >>> text = u"&gt;&quot;&lt;&#25991;&#23383;&#x53C2;&#x7167; &amp; &#x5B9F;&#x4F53;&#21442;&#29031;"
    >>> print htmlentity2unicode(text).encode('utf-8')
    >"<文字参照 & 実体参照
    """

    # 正規表現のコンパイル
    reference_regex = re.compile(r'&(#x?[0-9a-f]+|[a-z]+);', re.IGNORECASE)
    num16_regex = re.compile(r'#x\d+', re.IGNORECASE)
    num10_regex = re.compile(r'#\d+', re.IGNORECASE)
     
    result = u''
    i = 0
    while True:
        # 実体参照 or 文字参照を見つける
        match = reference_regex.search(text, i)
        if match is None:
            result += text[i:]
            break
         
        result += text[i:match.start()]
        i = match.end()
        name = match.group(1)
         
        # 実体参照
        if name in htmlentitydefs.name2codepoint.keys():
            result += unichr(htmlentitydefs.name2codepoint[name])
        # 文字参照
        elif num16_regex.match(name):
            # 16進数
            result += unichr(int(u'0'+name[1:], 16))
        elif num10_regex.match(name):
            # 10進数
            result += unichr(int(name[1:]))
 
    return result


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags = (doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))



