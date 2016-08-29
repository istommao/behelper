# coding: utf-8
import sys
import base64
import hashlib

from workflow import Workflow3


def md5_encode(keyword):
    m = hashlib.md5()
    m.update(keyword)
    return m.hexdigest()


def base64_encode(keyword):
    return base64.b64encode(keyword)


def base64_decode(keyword):
    return base64.b64decode(keyword)


def len_func(keyword):
    return len(unicode(keyword, 'utf-8'))


CMD_DICT = {
    'md5encode': md5_encode,
    'bs64encode': base64_encode,
    'bs64decode': base64_decode,
    'len': len_func,
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
