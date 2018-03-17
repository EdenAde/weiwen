from openerp import models
import HTMLParser

class mail_mail_utilities(models.Model):
    _inherit = ['mail.mail']
   
    def unescapeHTML(self, text):
        return HTMLParser.HTMLParser().unescape(text)