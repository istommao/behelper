# coding: utf-8
import sys
import base64
import hashlib
import json
import time

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


def rfc_link(keyword):
    return 'https://tools.ietf.org/html/rfc{}'.format(keyword)


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


def car_search(keyword):
    """car search."""
    dataset = {
        '冀A': '石家庄市',
        '冀B': '唐山市',
        '冀C': '秦皇岛市',
        '冀D': '邯郸市',
        '冀E': '邢台市',
        '冀F': '保定市',
        '冀G': '张家口市',
        '冀H': '承德市',
        '冀J': '沧州市',
        '冀R': '廊坊市',
        '冀S': '沧州市',
        '冀T': '衡水市',
        '豫A': '郑州市',
        '豫B': '开封市',
        '豫C': '洛阳市',
        '豫D': '平顶山市',
        '豫E': '安阳市',
        '豫F': '鹤壁市',
        '豫G': '新乡市',
        '豫H': '焦作市',
        '豫J': '濮阳市',
        '豫K': '许昌市',
        '豫L': '漯河市',
        '豫M': '三门峡市',
        '豫N': '商丘市',
        '豫P': '周口市',
        '豫Q': '驻马店市',
        '豫R': '南阳市',
        '豫S': '信阳市',
        '豫U': ' 济源市',
        '云A': '昆明市',
        '云A-V': '东川市',
        '云C': '昭通市',
        '云D': '曲靖市',
        '云E': '楚雄彝族自治州',
        '云F': '玉溪市',
        '云G': '红河哈尼族彝族自治州',
        '云H': '文山壮族苗族自治州',
        '云J': '思茅市',
        '云K': '西双版纳傣族自治州',
        '云L': '大理白族自治州',
        '云M': '保山市',
        '云N': '德宏傣族景颇族自治州',
        '云P': '丽江市',
        '云Q': '怒江傈僳族自治州',
        '云R': '迪庆藏族自治州',
        '云S': '临沧地区',
        '辽A': '沈阳市',
        '辽B': '大连市',
        '辽C': '鞍山市',
        '辽D': '抚顺市',
        '辽E': '本溪市',
        '辽F': '丹东市',
        '辽G': '锦州市',
        '辽H': '营口市',
        '辽J': '阜新市',
        '辽K': '辽阳市',
        '辽L': '盘锦市',
        '辽M': '铁岭市',
        '辽N': '朝阳市',
        '辽P': '葫芦岛市',
        '黑A': '哈尔滨市',
        '黑B': '齐齐哈尔市',
        '黑C': '牡丹江市',
        '黑D': '佳木斯市',
        '黑E': '大庆市',
        '黑F': '伊春市',
        '黑G': '鸡西市',
        '黑H': '鹤岗市',
        '黑J': '双鸭山市',
        '黑K': '七台河市',
        '黑L': '松花江地区（已并入哈尔滨市，车牌未改）',
        '黑M': '绥化市',
        '黑N': '黑河市',
        '黑P': '大兴安岭地区',
        '黑R': '农垦系统',
        '湘A': '长沙市',
        '湘B': '株洲市',
        '湘C': '湘潭市',
        '湘D': '衡阳市',
        '湘E': '邵阳市',
        '湘F': '岳阳市',
        '湘G': '张家界市',
        '湘H': '益阳市',
        '湘J': '常德市',
        '湘K': '娄底市',
        '湘L': '郴州市',
        '湘M': '永州市',
        '湘N': '怀化市',
        '湘U': '湘西土家族苗族自治州',
        '新A': '乌鲁木齐市',
        '新B': '昌吉回族自治州',
        '新C': '石河子市',
        '新D': '奎屯市',
        '新E': '博尔塔拉蒙古自治州',
        '新F': '伊犁哈萨克自治州直辖县',
        '新G': '塔城市',
        '新H': '阿勒泰市',
        '新J': '克拉玛依市',
        '新K': '吐鲁番市',
        '新L': '哈密市',
        '新M': '巴音郭愣蒙古自治州',
        '新N': '阿克苏市',
        '新P': '克孜勒苏柯尔克孜自治州',
        '新Q': '喀什市',
        '新R': '和田市',
        '鲁A': '济南市',
        '鲁B': '青岛市',
        '鲁C': '淄博市',
        '鲁D': '枣庄市',
        '鲁E': '东营市',
        '鲁F': '烟台市',
        '鲁G': '潍坊市',
        '鲁H': '济宁市',
        '鲁J': '泰安市',
        '鲁K': '威海市',
        '鲁L': '日照市',
        '鲁M': '滨州市',
        '鲁N': '德州市',
        '鲁P': '聊城市',
        '鲁Q': '临沂市',
        '鲁R': '菏泽市',
        '鲁S': '莱芜市',
        '鲁U': '青岛市增补',
        '鲁V': '潍坊市增补',
        '鲁Y': '烟台市增补',
        '皖A': '合肥市',
        '皖B': '芜湖市',
        '皖C': '蚌埠市',
        '皖D': '淮南市',
        '皖E': '马鞍山市',
        '皖F': '淮北市',
        '皖G': '铜陵市',
        '皖H': '安庆市',
        '皖J': '黄山市',
        '皖K': '阜阳市',
        '皖L': '宿州市',
        '皖M': '滁州市',
        '皖N': '六安市',
        '皖P': '宣城市',
        '皖Q': '巢湖市',
        '皖R': '池州市',
        '皖S': '亳州市',
        '浙A': '杭州市',
        '浙B': '宁波市',
        '浙C': '温州市',
        '浙D': '绍兴市',
        '浙E': '湖州市',
        '浙F': '嘉兴市',
        '浙G': '金华市',
        '浙H': '衢州市',
        '浙J': '台州市',
        '浙K': '丽水市',
        '浙L': '舟山市',
        '苏A': '南京市',
        '苏B': '无锡市',
        '苏C': '徐州市',
        '苏D': '常州市',
        '苏E': '苏州市',
        '苏F': '南通市',
        '苏G': '连云港市',
        '苏H': '淮安市',
        '苏J': '盐城市',
        '苏K': '扬州市',
        '苏L': '镇江市',
        '苏M': '泰州市',
        '苏N': '宿迁市',
        '赣A': '南昌市',
        '赣B': '赣州市',
        '赣C': '宜春市',
        '赣D': '吉安市',
        '赣E': '上饶市',
        '赣F': '抚州市',
        '赣G': '九江市',
        '赣H': '景德镇市',
        '赣J': '萍乡市',
        '赣K': '新余市',
        '赣L': '鹰潭市',
        '赣M': '南昌市,省直系统',
        '桂A': '南宁市',
        '桂B': '柳州市',
        '桂C': '桂林市',
        '桂D': '梧州市',
        '桂E': '北海市',
        '桂F': '崇左市',
        '桂G': '来宾市',
        '桂H': '桂林地区',
        '桂J': '贺州市',
        '桂K': '玉林市',
        '桂L': '百色市',
        '桂M': '河池市',
        '桂N': '钦州市',
        '桂P': '防城港市',
        '桂R': '贵港市',
        '鄂A': '武汉市',
        '鄂B': '黄石市',
        '鄂C': '十堰市',
        '鄂D': '荆州市',
        '鄂E': '宜昌市',
        '鄂F': '襄樊市',
        '鄂G': '鄂州市',
        '鄂H': '荆门市',
        '鄂J': '黄冈市',
        '鄂K': '孝感市',
        '鄂L': '咸宁市',
        '鄂M': '仙桃市',
        '鄂N': '潜江市',
        '鄂P': '神农架林区',
        '鄂Q': '恩施土家族苗族自治州',
        '鄂R': '天门市',
        '鄂S': '随州市',
        '甘A': '兰州市',
        '甘B': '嘉峪关市',
        '甘C': '金昌市',
        '甘D': '白银市',
        '甘E': '天水市',
        '甘F': '酒泉市',
        '甘G': '张掖市',
        '甘H': '武威市',
        '甘J': '定西市',
        '甘K': '陇南市',
        '甘L': '平凉市',
        '甘M': '庆阳市',
        '甘N': '临夏回族自治州',
        '甘P': '甘南藏族自治州',
        '陕A': '西安市',
        '陕B': '铜川市',
        '陕C': '宝鸡市',
        '陕D': '咸阳市',
        '陕E': '渭南市',
        '陕F': '汉中市',
        '陕G': '安康市',
        '陕H': '商洛市',
        '陕J': '延安市',
        '陕K': '榆林市',
        '陕V': '杨凌高新农业示范区',
        '晋A': '太原市',
        '晋B': '大同市',
        '晋C': '阳泉市',
        '晋D': '长治市',
        '晋E': '晋城市',
        '晋F': '朔州市',
        '晋H': '忻州市',
        '晋J': '吕梁地区',
        '晋K': '晋中市',
        '晋L': '临汾市',
        '晋M': '运城市',
        '蒙A': '呼和浩特市',
        '蒙B': '包头市',
        '蒙C': '乌海市',
        '蒙D': '赤峰市',
        '蒙E': '呼伦贝尔市',
        '蒙F': '兴安盟',
        '蒙G': '通辽市',
        '蒙H': '锡林郭勒盟',
        '蒙J': '乌兰察布盟',
        '蒙K': '鄂尔多斯市',
        '蒙L': '巴彦淖尔盟',
        '蒙M': '阿拉善盟',
        '贵A': '贵阳市',
        '贵B': '六盘水市',
        '贵C': '遵义市',
        '贵D': '铜仁市',
        '贵E': '黔西南布依族苗族自治州',
        '贵F': '毕节市',
        '贵G': '安顺市',
        '贵H': '黔东南苗族侗族自治州',
        '贵J': '黔南布依族苗族自治州',
        '吉A': '长春市',
        '吉B': '吉林市',
        '吉C': '四平市',
        '吉D': '辽源市',
        '吉E': '通化市',
        '吉F': '白山市',
        '吉G': '白城市',
        '吉H': '延边朝鲜族自治州',
        '吉J': '松原市',
        '吉K': '长白山',
        '闽A': '福州市',
        '闽B': '莆田市',
        '闽C': '泉州市',
        '闽D': '厦门市',
        '闽E': '漳州市',
        '闽F': '龙岩市',
        '闽G': '三明市',
        '闽H': '南平市',
        '闽J': '宁德市',
        '闽K': '省直系统',
        '粤A': '广州市',
        '粤B': '深圳市',
        '粤C': '珠海市',
        '粤D': '汕头市',
        '粤E': '佛山市',
        '粤F': '韶关市',
        '粤G': '湛江市',
        '粤H': '肇庆市',
        '青A': '西宁市',
        '青B': '海东市',
        '青C': '海北藏族自治州',
        '青D': '黄南藏族自治州',
        '青E': '海南藏族自治州',
        '青F': '果洛藏族自治州',
        '青G': '玉树藏族自治州',
        '青H': '海西蒙古族藏族自治州',
        '粤J': '江门市',
        '粤K': '茂名市',
        '粤L': '惠州市',
        '粤M': '梅州市',
        '粤N': '汕尾市',
        '粤P': '河源市',
        '粤Q': '阳江市',
        '粤R': '清远市',
        '粤S': '东莞市',
        '粤T': '中山市',
        '粤U': '潮州市',
        '粤V': '揭阳市',
        '粤W': '云浮市',
        '粤X': '顺德区',
        '川A': '成都市',
        '川B': '绵阳市',
        '川C': '自贡市',
        '川D': '攀枝花市',
        '川E': '泸州市',
        '川F': '德阳市',
        '川H': '广元市',
        '川J': '遂宁市',
        '川K': '内江市',
        '川L': '乐山市',
        '川M': '资阳市',
        '川N': '',
        '川P': '',
        '川Q': '宜宾市',
        '川R': '南充市',
        '川S': '达州市',
        '川T': '雅安市',
        '川U': '阿坝藏族羌族自治州',
        '川V': '甘孜藏族自治州  海南省（琼）',
        '川W': '凉山彝族自治州',
        '川X': '广安市',
        '川Y': '巴中市',
        '川Z': '眉山市',
        '藏A': '拉萨市',
        '藏B': '昌都地区',
        '藏C': '山南地区',
        '藏D': '日喀则地区',
        '藏E': '那曲地区',
        '藏F': '阿里地区',
        '藏G': '林芝地区',
        '藏H': '驻四川省天全县车辆管理所',
        '藏J': '驻青海省格尔木市车辆管理所',
        '粤Y': '南海区',
        '粤Z': '港澳进入内地车辆',
        '琼A': '海口市',
        '琼B': '三亚市',
        '琼C': '琼海市',
        '琼D': '五指山市',
        '琼E': '洋浦开发区',
        '宁A': '银川市',
        '宁B': '石嘴山市',
        '宁C': '银南市',
        '宁D': '固原市',
        '宁E': '中卫市',
        '渝A': '重庆市区（江南）',
        '渝B': '重庆市区（江北）',
        '渝C': '永川区',
        '渝F': '万州区',
        '渝G': '涪陵区',
        '渝H': '黔江区',
        '京A': '北京市',
        '京B': '北京市',
        '京C': '北京市',
        '京D': '北京市',
        '京E': '北京市',
        '京F': '北京市',
        '京G': '北京市',
        '京H': '北京市',
        '京J': '北京市',
        '京K': '北京市',
        '京L': '北京市',
        '京M': '北京市',
        '京Y': '北京市',
        '津A': '天津市',
        '津B': '天津市',
        '津C': '天津市',
        '津D': '天津市',
        '津E': '天津市',
        '津F': '天津市',
        '津G': '天津市',
        '津H': '天津市',
        '沪A': '上海市',
        '沪B': '上海市',
        '沪C': '上海市',
        '沪D': '上海市',
        '沪R': '崇明、长兴、横沙'
    }

    return dataset.get(keyword.upper(), '未知')


def unicode_handler(data):
    result = data.decode('unicode_escape')
    return result


def get_random_string(length,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    import random
    length = int(length)
    return ''.join(random.choice(allowed_chars) for i in range(length))


def behelp_handler(*arg):
    results = [
        'unicode 将字符串中的unicode转为中文',
        'md5 md5加密',
        'b64encode base64 编码',
        'b64decode base64 解码',
        'randstr 生成随机字符串',
        'len 计算字符串长度',
    ]

    return results


def json_format(data):
    data = data.replace("'", '"')

    data = json.loads(data)

    return json.dumps(data, indent=4, ensure_ascii=False, separators=(',', ': '))


def timestamp_handler(data):
    now = time.time()
    if data == 'now':
        return int(now)
    else:
        return int(now)


CMD_DICT = {
    'md5encode': md5_encode,
    'bs64encode': base64_encode,
    'bs64decode': base64_decode,
    'len': len_func,
    'check_idcard': check_idcard,
    'ord': ascii_ord,
    'chr': ascii_chr,
    'car': car_search,
    'rfc': rfc_link,
    'httpcode': http_code,
    'unicode': unicode_handler,
    'randstr': get_random_string,
    'behelp': behelp_handler,
    'jsonformat': json_format,
    'timestamp': timestamp_handler
}


def main(wf):
    cmd = None

    if len(wf.args) == 2:
        cmd, keyword = wf.args
    elif len(wf.args) == 1:
        keyword = wf.args[0]
    else:
        keyword = ''.join(wf.args[1:])
        cmd = wf.args[0]

    if keyword:
        keyword = keyword.encode('utf-8')

    if not cmd or cmd not in CMD_DICT:
        wf.add_item(title=u'不支持的编码格式，目前只支持(md5,base64)')
    elif cmd and cmd in CMD_DICT:
        func = CMD_DICT[cmd]
        try:
            retdata = func(keyword)
        except TypeError:
            wf.add_item(title=u'编码错误，请检查您输入的参数是否正确!')
        else:
            show_data(cmd, keyword, retdata)

    wf.send_feedback()


def show_data(cmd, keyword, retdata):
    if not isinstance(retdata, list):
        retdata = [retdata]

    for result in retdata:
        wf.add_item(title='{}: {}'.format(cmd, keyword), subtitle=result,
                    arg=result, valid=True)


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
