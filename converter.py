import requests 

class BotHandler:
    
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        print(result_json)
        return result_json
    
    def send_mp3(self, chat_id, url, reply_id=None):
        params = {'chat_id': chat_id, 'audio': url, 'reply_to_message_id': reply_id}
        method = 'sendAudio'
        resp = requests.post(self.api_url + method, params)
        return resp
    
    def get_last_update(self,offset):
        get_result = self.get_updates(offset)
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = []
        return last_update
        
    def getURL(self,text):
        import urllib
        import urllib2
        from bs4 import BeautifulSoup
        
        query = urllib.quote(text)
        url = "https://www.youtube.com/results?sp=EgIQAVAU&q=" + query
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html,"html.parser")
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            return 'https://www.youtube.com' + vid['href']
    
    def convert(self,yt_link):
        import json
        import urllib2
        
        url = "http://www.youtubeinmp3.com/fetch/?format=JSON&video=" + yt_link
        data = json.load(urllib2.urlopen(url))
        return data["link"]


conv_bot = BotHandler("426392520:AAFN1FZWTOm8-iz_KYEd7Uzcjs98c68p0YQ")

def main():
    
    import re
    
    new_offset = None
    
    while True:
        
        last_update = conv_bot.get_last_update(new_offset)
        
        if last_update != []:
            last_update_id = last_update['update_id']
            try:
                last_chat_text = re.sub('[^A-z ]', '', last_update['message']['text'].lower())
                last_chat_id = last_update['message']['chat']['id']
                reply_id = last_update["message"]["message_id"]
            except KeyError:
                last_chat_text = ""

            yt_link = conv_bot.getURL(last_chat_text)
            dl_link = conv_bot.convert(yt_link)
            conv_bot.send_mp3(last_chat_id,dl_link,reply_id)

            new_offset = last_update_id + 1
            
    return
        
if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
