"""
/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 43):
 * <neerajkumar@outlook.com> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return. 
 * If you are reading this in the second half the the 21st century, then I am at 
 * an age which won't allow me to metabolize any kind of alcohol, so please
 * treat yourself with a beer on my behalf.
 * -Neeraj Kumar
 * ----------------------------------------------------------------------------
 */
"""

import datetime
import math
import json
import retry
import time
import urllib
import urllib2


SCOPE_URL='http://api.microsofttranslator.com'
OAUTH_URL='https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
AZURE_TRANSLATE_API_URL='http://api.microsofttranslator.com/V2/Ajax.svc/Translate?%s'
GRANT_CLIENT_CREDENTIALS_ONLY='client_credentials'


class MicrosoftTranslatorClient(object):
  """Handles authentication and translation for Microsoft Translator API.
  
  Arguments:
    client_id: The client_id for your azure application (as a string)
    client_secret: The client secret for your azure application (as a string)
  """
  
  def __init__(self, client_id, client_secret):
    self.client_id = client_id
    self.client_secret = client_secret
    self.last_auth_token_refresh=None
    self.auth_token = self.__GetAuthenticationToken()

  @retry.retry(Exception, tries=3, delay=5, backoff=2)
  def __GetAuthenticationToken(self):
    """Gets the authentication token for your app from azure marketplace."""
    auth_args = {
      'client_id': self.client_id,
      'client_secret': self.client_secret,
      'scope': SCOPE_URL,
      'grant_type': GRANT_CLIENT_CREDENTIALS_ONLY
    }
    self.auth_token = json.loads(urllib2.urlopen(OAUTH_URL,data=urllib.urlencode(auth_args)).read())
    if self.auth_token:
      self.last_auth_token_refresh = datetime.datetime.now()
      return self.auth_token
    else:
      return None

  @retry.retry(Exception, tries=3, delay=5, backoff=2)
  def TranslateText(self, unicode_string, from_lang_code, to_lang_code):
    """Translates a given text from given language to target language.
    
    This function tries to translate the text thrice, and if no translations could be done
    returns an empty string.
    
    Arguments:
      unicode_string: The string to transalte in unicode format.
      from_lang_code: The source language code.
      to_lang_code: The destination language code.
    
    Returns:
      Translated string if succesful, ""(empty string) otherwise.
    """
    
    self.translated_text = ""
    # Whenever there is a translate request, check if our token in still valid.
    # if valid, then its all good, continue to next step
    # if not, then get the authentication token again.
    now = datetime.datetime.now()
    if (now - self.last_auth_token_refresh).seconds > 550 :
      if not self.__GetAuthenticationToken():
        return "Text could not be translated due to a recurring authentication error."
    translate_packet = {
      'text': unicode_string,
      'to': to_lang_code,
      'from': from_lang_code
    }
    headers = {
      'Authorization': 'Bearer '+ self.auth_token['access_token']
    }
    translate_req = urllib2.Request(AZURE_TRANSLATE_API_URL % urllib.urlencode(translate_packet),
                                    headers=headers)
    return urllib2.urlopen(translate_req).read()