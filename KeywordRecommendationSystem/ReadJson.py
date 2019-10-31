import json
import re
def readJson(data):
    list = []
    for num in range(0, len(json.loads(data))):
        try:
            anounce = json.loads(data)[num]['good']
        except:
            continue
        for innum in range(0, len(anounce)):
            list.append(anounce[innum])
    return list

def getGoodname(data):
    startStr = "产品名称："
    endStr = "；规格型号："
    patternStr = r'%s(.+?)%s' % (startStr, endStr)
    p = re.compile(patternStr, re.IGNORECASE)
    m = re.findall(p, data)
    print(m)


if __name__ == '__main__':
    data = [{
        "type": 1,
        "id": 1,
        "tenderContent": "1",
        "tenderContentName": "成交",
        "good": [{
            "title": "HPLaserJet MFP M72630dn 黑白激光数码复合机",
            "amount": 0,
            "count": 14700.0,
            "univalent": 0.0,
            "quantum": 0,
            "providerName": "重庆市香晓科技有限责任公司",
            "providerID": "130117343190712482",
            "projectDirectoryCode": "A",
            "feeScale": "无",
            "feeMoney": 0.0,
            "resultType": 1,
            "providerRealName": "万小礼",
            "providerMobile": "18983335336",
            "sum": 0.0
        }]
    }]
    # readJson(data)



    data = r':"交货时间：采购合同签订后120个工作日内交货并完成安装调试；交货地点：采购人指定地点。","agentFee":0,"feeScale":"100万元*1.5%+29.998*1.1%=18299.8元","feeMoney":"18299.8","projectDirectoryCode":"A","resultType":"1","proAddress":"成都市锦江区锦华路一段8号1-3幢30楼2号","providerRealName":"尚进","providerMobile":"13808066772","models":"产品名称：三维激光扫描仪；规格型号：ScanStation  P50；数量：1；单价：115.28万元等。","providerID":"485998428464144385","providerName":"成都赛纬科技有限公司"}],"isWritting":false,"tenderContent":1,"showUnivalent":false,"showQuantum":false,"tenderContentName":"成交","shortProvider":"","type":1}]'
    getGoodname(data)
