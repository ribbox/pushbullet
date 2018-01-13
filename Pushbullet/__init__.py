from pushbullet import Pushbullet

from modules import app, cbpi
from thread import start_new_thread
import logging
import time
import requests

pushbullet_token = None


def pushBulletToken():
	global pushbullet_token
	pushbullet_token = cbpi.get_config_parameter("pushbullet_token", None)
	cbpi.app.logger.info("check parameter")
	if pushbullet_token is None:
		print "INIT pushbullet Token"
		try:
			cbpi.add_config_parameter("pushbullet_token", "", "text", "pushbullet API Token")
		except:
			cbpi.notify("pushbullet Error", "Unable to update database. Update CraftBeerPi and reboot.", type="danger", timeout=None)


@cbpi.initalizer(order=9000)
def init(cbpi):
	global pushbullet
	cbpi.app.logger.info("INITIALIZE pushbullet PLUGIN")
	pushBulletToken()
	if pushbullet_token is None or not pushbullet_token:
		cbpi.notify("pushbullet Error", "Check pushbullet API Token is set", type="danger", timeout=None)
	else:
		pushbullet = "OK"

@cbpi.event("MESSAGE", async=True)
def messageEvent(message):
	pb = Pushbullet(pushbullet_token)
	push = pb.push_note(message["headline"],message["message"])

