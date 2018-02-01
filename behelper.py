# coding: utf-8
import sys
import base64
import hashlib
import json

import urllib
import urllib2

from workflow import Workflow3


HTTP_CODES = {
    '100': 'Continue    服务器仅接收到部分请求，但是一旦服务器并没有拒绝该请求，客户端应该继续发送其余的请求。',
    '101': 'Switching Protocols 服务器转换协议：服务器将遵从客户的请求转换到另外一种协',
    '200': 'OK  请求成功（其后是对GET和POST请求的应答文档。）',
    '201': 'Created 请求被创建完成，同时新的资源被创建。',
    '202': 'Accepted    供处理的请求已被接受，但是处理未完成。',
    '203': 'Non-authoritative Information   文档已经正常地返回，但一些应答头可能不正确，因为使用的是文档的拷贝。',
    '204': 'No Content  没有新文档。浏览器应该继续显示原来的文档。如果用户定期地刷新页面，而Servlet可以确定用户文档足够新，这个状态代码是很有用的。',
    '205': 'Reset Content   没有新文档。但浏览器应该重置它所显示的内容。用来强制浏览器清除表单输入内容。',
    '206': 'Partial Content 客户发送了一个带有Range头的GET请求，服务器完成了它。',
    '300': 'Multiple Choices    多重选择。链接列表。用户可以选择某链接到达目的地。最多允许五个地址。',
    '301': 'Moved Permanently   所请求的页面已经转移至新的url。',
    '302': 'Found   所请求的页面已经临时转移至新的url。',
    '303': 'See Other   所请求的页面可在别的url下被找到。',
    '304': 'Not Modified    未按预期修改文档。客户端有缓冲的文档并发出了一个条件性的请求（一般是提供If-Modified-Since头表示客户只想比指定日期更新的文档）。服务器告诉客户，原来缓冲的文档还可以继续使用。',
    '305': 'Use Proxy   客户请求的文档应该通过Location头所指明的代理服务器提取。',
    '306': 'Unused  此代码被用于前一版本。目前已不再使用，但是代码依然被保留。',
    '307': 'Temporary Redirect  被请求的页面已经临时移至新的url。',
    '400': 'Bad Request 服务器未能理解请求。',
    '401': 'Unauthorized    被请求的页面需要用户名和密码。',
    '402': 'Payment Required    此代码尚无法使用。',
    '403': 'Forbidden   对被请求页面的访问被禁止。',
    '404': 'Not Found   服务器无法找到被请求的页面。',
    '405': 'Method Not Allowed  请求中指定的方法不被允许。',
    '406': 'Not Acceptable  服务器生成的响应无法被客户端所接受。',
    '407': 'Proxy Authentication Required   用户必须首先使用代理服务器进行验证，这样请求才会被处理。',
    '408': 'Request Timeout 请求超出了服务器的等待时间。',
    '409': 'Conflict    由于冲突，请求无法被完成。',
    '410': 'Gone    被请求的页面不可用。',
    '411': 'Length Required "Content-Length" 未被定义。如果无此内容，服务器不会接受请求。',
    '412': 'Precondition Failed 请求中的前提条件被服务器评估为失败。',
    '413': 'Request Entity Too Large    由于所请求的实体的太大，服务器不会接受请求。',
    '414': 'Request-url Too Long    由于url太长，服务器不会接受请求。当post请求被转换为带有很长的查询信息的get请求时，就会发生这种情况。',
    '415': 'Unsupported Media Type  由于媒介类型不被支持，服务器不会接受请求。',
    '416': '服务器不能满足客户在请求中指定的Range头。',
    '417': 'Expectation Failed',
    '428': 'Precondition Required (要求先决条件)',
    '429': 'Too Many Requests (太多请求)',
    '431': 'Request Header Fields Too Large (请求头字段太大)',
    '500': 'Internal Server Error   请求未完成。服务器遇到不可预知的情况。',
    '501': 'Not Implemented 请求未完成。服务器不支持所请求的功能。',
    '502': 'Bad Gateway 请求未完成。服务器从上游服务器收到一个无效的响应。',
    '503': 'Service Unavailable 请求未完成。服务器临时过载或当机。',
    '504': 'Gateway Timeout 网关超时。',
    '505': 'HTTP Version Not Supported  服务器不支持请求中指明的HTTP协议版本。',
    '511': 'Network Authentication Required (要求网络认证)'
}


def http_code(keyword):
    return HTTP_CODES.get(keyword, '未找到对应的 HTTP Code')


def md5_encode(keyword):
    m = hashlib.md5()
    m.update(keyword)
    return m.hexdigest()


def ascii_ord(keyword):
    try:
        return ord(keyword)
    except TypeError:
        return '请输入单个字符'


def ascii_chr(keyword):
    try:
        return chr(int(keyword))
    except (ValueError, TypeError):
        return '请输入一个整数'


def base64_encode(keyword):
    return base64.b64encode(keyword)


def base64_decode(keyword):
    return base64.b64decode(keyword)


def len_func(keyword):
    return len(unicode(keyword, 'utf-8'))


def check_idcard(keyword):
    """Check idcard."""
    url = 'http://id.8684.cn/ajax.php?act=check'

    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    values = {'userId': keyword}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)

    response = urllib2.urlopen(req)

    result = response.read()
    dictdata = json.loads(result)

    if dictdata.get('valid') != u'有':
        return u'请输入有效的身份证号码!'

    birthday = u'{}-{}-{}'.format(dictdata.get('year'),
                                  dictdata.get('month'),
                                  dictdata.get('day'))
    compstr = u'{place} {sex} {birthday}'.format(
        place=dictdata.get('place'), sex=dictdata.get('sex'),
        birthday=birthday)

    return compstr


CMD_DICT = {
    'md5encode': md5_encode,
    'bs64encode': base64_encode,
    'bs64decode': base64_decode,
    'len': len_func,
    'check_idcard': check_idcard,
    'ord': ascii_ord,
    'chr': ascii_chr,
    'httpcode': http_code
}


def main(wf):
    cmd = None
    if len(wf.args) == 2:
        cmd, keyword = wf.args
    elif len(wf.args) == 1:
        keyword = wf.args[0]
    else:
        keyword = None

    if keyword:
        keyword = keyword.encode('utf-8')

    if not cmd or cmd not in CMD_DICT:
        wf.add_item(title=u'不支持的编码格式，目前只支持(md5,base64)')
    elif cmd and cmd in CMD_DICT:
        func = CMD_DICT[cmd]
        try:
            result = func(keyword)
        except TypeError:
            wf.add_item(title=u'编码错误，请检查您输入的参数是否正确!')
        else:
            wf.add_item(title='{}: {}'.format(cmd, keyword), subtitle=result,
                        arg=result, valid=True)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
