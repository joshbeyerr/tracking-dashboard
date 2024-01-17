import requests
import time

def solve_recaptcha():
    apikey= "efebccba07761fb17d5df76532596178"
    # Step 1: Request reCAPTCHA solving
    captcha_data = {
        'key': apikey,
        'method': 'userrecaptcha',
        'googlekey': "6LdQquAaAAAAALeU6cp88M5ByhWDANC1-ei8xfMW",
        'pageurl': "https://www.adidas.ca/api/orders/search?sitePath=en",
        'json': 1,
    }

    response = requests.post('http://2captcha.com/in.php', data=captcha_data)
    request_result = response.json()

    print(request_result)

    if request_result['status'] != 1:
        raise Exception("Failed to submit reCAPTCHA for solving")

    # Step 2: Polling for reCAPTCHA solution
    captcha_id = request_result['request']

    for _ in range(20):  # Adjust the number of polling attempts as needed
        time.sleep(5)  # Wait for 5 seconds between polling attempts

        captcha_result = requests.get(f'http://2captcha.com/res.php?key={apikey}&action=get&id={captcha_id}').text

        if 'OK' in captcha_result:
            return captcha_result.split('|')[1]  # Extract the reCAPTCHA solution

    raise Exception("Failed to get reCAPTCHA solution within timeout")

b = solve_recaptcha()
print(b)


s = requests.session()

data = {"email":"beyertorontoshoes@gmail.com","recaptcha":b,"orderNo":"ACA93514432","returnHub":False}
print(data)
s.headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
)

send = s.post('https://www.adidas.ca/api/orders/search?sitePath=en', data=data)
print(send)
print(send.text)