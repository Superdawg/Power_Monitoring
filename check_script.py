#!/usr/bin/python3
#
# Synopsis:
# ./power_check.py  --email-recipients --email-relay

from apcaccess import status as apc
from email.message import EmailMessage
import argparse
import logging
import os
import pprint
import smtplib
import socket
import sys
import time

class Logger(object):
    def __init__(self, name, filename=None):
        self.loggerName = name

        if filename:
            self.filename = filename
        else:
            self.filename = None

    def getLogger(self):
        logger = logging.getLogger(self.loggerName)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s-%(name)s-[%(process)d] %(message)s')
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        if self.filename:
            fhandler = logging.FileHandler(self.filename)
            fhandler.setFormatter(formatter)
            logger.addHandler(fhandler)
        return logger

class PowerMonitor(object):
    def __init__(self):
        self.log = Logger(name = "PowerMonitor").getLogger()
        self.parseArgs()
        try:
            self.hostname = socket.getfqdn()
        except Exception as error:
            self.log.error("Unable to detect proper hostname")
            sys.exit(1)

    def parseArgs(self):
        parser = argparse.ArgumentParser(
                description=("Check the power status of the UPS and notify if "
                             "it is unacceptable"))
        parser.add_argument('--email-recipients',
                            action='store',
                            dest='emails',
                            type=str,
                            nargs='+',
                            default=None,
                            help=("The list of email addresses to notify when "
                                  "there is a confirmed failure"))
        parser.add_argument('--email-relay',
                            action='store',
                            dest='email_relay',
                            type=str,
                            default='localhost',
                            help=("The SMTP/MTA to use for sending the email"))
        args = parser.parse_args()

        self.emails = args.emails
        self.relay = args.email_relay

    def notifyEmails(self):
        """
        Send email notice if specified that we have acted on a failure
        """
        message = EmailMessage()
        message.set_content(("The Power Monitoring Script has noticed that the "
                             "status is not ONLINE.  Please investigate for "
                             "possible power outage"
                             "\n\n"
                             "APC Stats follow:"
                             "%s" % pprint.pformat(self.state)))

        # Keeping a timestamp in the subject is important since this message
        # may be getting delivered significantly later than the actual action.
        # If this event triggers, that means internet is considered to be down.
        # This message won't be delivered until internet connectivity has been
        # restored.
        #XXX: If the connection is down for a long time, then there could be a
        #     large number of these messages queued up.  This should probably
        #     be taken into account somehow.
        message['Subject'] = ("[POWER FAILURE] %s - %s" %
            (time.strftime("%Y%m%d-%H%M%S"), self.hostname))
        message['From'] = ("power_check@%s" % self.hostname)
        message['To'] = ', '.join(self.emails)

        # Now that we're finished assembilng the message, let's send it along.
        smtp = smtplib.SMTP(self.relay)
        smtp.send_message(message)
        smtp.quit()

    def run(self):
        self.state = apc.parse(apc.get(), strip_units=True)

        if self.state['STATUS'] != "ONLINE":
            print("Power status is %s.  This is bad" % self.state['STATUS'])
            self.notifyEmails()
        print("All is well, nothing to see here.")

if __name__ == "__main__":
    PM = PowerMonitor()
    PM.run()
    sys.exit(0)
