# coding: utf-8
import requests

API_SERVER="https://www.google.com/recaptcha/api.js"
VERIFY_SERVER="https://www.google.com/recaptcha/api/siteverify"


def displayhtml(public_key, noscript=True):
    """
    Gets the HTML to display for reCAPTCHA

    public_key -- The public api key
    """

    html = """
    <script src="{recaptcha_server}" async defer></script>
    <div class="g-recaptcha" data-sitekey="{recaptcha_site_key}"></div>
    """.format(recaptcha_server=API_SERVER, recaptcha_site_key=public_key)

    if noscript:
        html += """
        <noscript>
          <div>
            <div style="width: 302px; height: 422px; position: relative;">
              <div style="width: 302px; height: 422px; position: absolute;">
                <iframe src="https://www.google.com/recaptcha/api/fallback?k={recaptcha_site_key}"
                        frameborder="0" scrolling="no"
                        style="width: 302px; height:422px; border-style: none;">
                </iframe>
              </div>
            </div>
            <div style="width: 300px; height: 60px; border-style: none;
                           bottom: 12px; left: 25px; margin: 0px; padding: 0px; right: 25px;
                           background: #f9f9f9; border: 1px solid #c1c1c1; border-radius: 3px;">
              <textarea id="g-recaptcha-response" name="g-recaptcha-response"
                           class="g-recaptcha-response"
                           style="width: 250px; height: 40px; border: 1px solid #c1c1c1;
                                  margin: 10px 25px; padding: 0px; resize: none;" >
              </textarea>
            </div>
          </div>
        </noscript>
        """.format(recaptcha_site_key=public_key)
    return html


def submit(request, secret_ket):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    recaptcha_challenge_field -- The value of recaptcha_challenge_field from the form
    recaptcha_response_field -- The value of recaptcha_response_field from the form
    private_key -- your reCAPTCHA private key
    remoteip -- the user's ip address
    """

    if request.method == 'POST':
        data = request.POST
        captcha_rs = data.get('g-recaptcha-response')

        if captcha_rs is None:
            status = 204
            message = "No captcha info provided"
        else:
            params = {
                'secret': secret_ket,
                'response': captcha_rs,
                'remoteip': get_client_ip(request)
            }

            verify_rs = requests.get(VERIFY_SERVER, params=params, verify=True)
            verify_rs = verify_rs.json()
            status = 200 if verify_rs.get("success", False) else 500
            message = verify_rs.get('error-codes', None) or ""
    else:
        status = 400
        message = "Should be a POST request"
    return {'message': message, 'status': status}


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
