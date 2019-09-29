
# 密码强度要求：
# （1）长度应在8位以上，特别重要的设备或系统应保证在12位以上；
# （2）密码中应至少包含大写字母、小写字母、数字、符号中的3类以上；
# （3）不使用任何连续的字母、数字或字符（包括在键盘上位置连续）；
# （4）不使用与公司相关、与部门相关的字符（例如：nsfocus、lvmeng）作为密码中的一部分。

import re
import easygui

# 长度应在8位以上
def proLENGTH(password):
    return True if len(password) >= 8 else False

# 是否包含三类以上字符，包含返回True
def proCONTAIN(password):
    p1 = 1 if re.compile('[A-Z]+').findall(password) else 0  # 大写字符
    p2 = 1 if re.compile('[a-z]+').findall(password) else 0 # 小写字符
    p3 = 1 if re.compile('[0-9]+').findall(password) else 0  # 数字
    p4 = 1 if re.compile('[-(\+)~!@`#$%^&*\{\}.\[\]_\?<\=>,\|\\\]').findall(password) else 0  # 特殊字符

    return True if p1 + p2 + p3 + p4 >= 3 else False

# 匹配 Nsfoucs，不包含返回True
def proNSFOCUS(password):
    rules = r'n(s|\$|5)f(o|@)cu(s|\$|5)'
    result = re.search(rules, password, re.I)

    return True if result == None else False

# 匹配 Lvmeng，不包含返回True
def proLVMENG(password):
    rules = r'(l|1)vmen(g|9)'
    result = re.search(rules, password, re.I)

    return True if result == None else False

# 匹配 连续字符（包括键盘连续），不包含返回True
def proOTHER(password):

    # 连续数字
    if re.findall('(`(?=0)|0(?=1)|1(?=2)|2(?=3)|3(?=4)|4(?=5)|5(?=6)|6(?=7)|7(?=8)|8(?=9)|9(?=0)){2}\S', password): return False

    # 键盘连续符号
    if re.findall('(~(?=!)|!(?=@)|@(?=#)|#(?=\$)|\$(?=%)|%(?=\^)|\^(?=&)|\&(?=\*)|\*(?=\()|\((?=\))|\)(?=_)|_(?=\+)){2}\S', password): return False
    if re.findall('(~(?=!)|!(?=@)|@(?=#)|#(?=\$)|\$(?=%)|%(?=\^)|\^(?=&)|\&(?=\*)|\*(?=\()|\((?=\))|\)(?=-)|-(?=\=)){2}\S', password): return False
    if re.findall('(0(?=_)|_(?=\+)){2}\S', password): return False
    if re.findall('(0(?=-)|-(?=\=)){2}\S', password): return False
    
    if re.findall('(p(?=\[)|\{(?=\})|\}(?=\|)){2}\S', password, re.I): return False
    if re.findall('(p(?=\[)|\[(?=\])|\](?=\\\)){2}\S', password, re.I): return False

    if re.findall('(l(?=:)|:(?=")){2}\S', password, re.I): return False
    if re.findall('(l(?=;)|;(?=\')){2}\S', password, re.I): return False

    if re.findall('(m(?=<)|<(?=>)|>(?=\?)){2}\S', password, re.I): return False
    if re.findall('(m(?=,)|,(?=.)|.(?=/)){2}\S', password, re.I): return False

    # 键盘连续字母
    if re.findall('(q(?=w)|w(?=e)|e(?=r)|r(?=t)|t(?=y)|y(?=u)|u(?=i)|i(?=o)|o(?=p)){2}',password, re.I): return False
    if re.findall('(a(?=s)|s(?=d)|d(?=f)|f(?=g)|g(?=h)|h(?=j)|j(?=k)|k(?=l)){2}',password, re.I): return False      
    if re.findall('(z(?=x)|x(?=c)|c(?=v)|v(?=b)|b(?=n)|n(?=m)){2}', password, re.I): return False

    return True
                     
# 新功能
def TODO(password):
    pass

# 主函数，对功能进行总体调用
def SecurityCheck(password): # return all([proLENGTH(password), proCONTAIN(password), proNSFOCUS(password), proLVMENG(password), proOTHER(password)])
    if not proLENGTH(password): return 'Length Problem'
    if not proCONTAIN(password): return 'Contain Problem'
    if not proNSFOCUS(password) & proLVMENG(password): return 'Contain Company'
    if not proOTHER(password): return 'Continuous letters'
    return 'Well Done'

# 检测界面 Demo  
def GUI():
    while True:
        password = easygui.enterbox('Enter your password to check for compliance', 'Weak Password')
        easygui.msgbox(SecurityCheck(password))
 
if __name__ == "__main__":
    GUI()
    