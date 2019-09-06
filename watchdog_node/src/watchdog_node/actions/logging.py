from . import ActionType
import smtplib
import rospy

class SendEmail(ActionType):
    name = "SendEmail"
    description = "Sends an email using simple unsecure SMTP."
    config_keys = [("to_addresses", "A list of email addresses to send to."),
                   ("from_address", "The email address to be sent from."),
                   ("message", "The message body of the email."),
                   ("server", "The SMTP server."),
                   ("port", "The port the SMTP server uses.")]

    def execute(self):
        try:
            msg = ("From: %s\r\nTo: %s\r\nSubject: %s\n\n%s"
                   % (self.from_address, ", ".join(self.to_addresses), self.subject,
                      self.message))

            with open(rospy.get_param("~pw_file"), "r") as f:
                self.pw = f.readline()

            server = smtplib.SMTP(self.server, self.port)
            server.starttls()
            server.login(self.from_address , self.pw)
            server.set_debuglevel(True)
            server.sendmail(self.from_address, self.to_addresses, msg)
            server.quit()
            rospy.loginfo("Sent email to {}".format(', '.join(self.to_addresses)))
        except Exception, e:
            rospy.logerr("Could not send email: {}".format(e))

