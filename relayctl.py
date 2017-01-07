#!/usr/bin/env python3
from bottle import route, request, run, get, template
from systemd.journal import JournalHandler
import time
import RPi.GPIO as GPIO
import logging

GPIO.setwarnings(False)
#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

rel = (1,2,3,4,5,6,7,8)
ports = (17,18,27,22,23,24,25,12)

log = logging.getLogger('relayctl')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)
log.info('Starting. Log ping #1')

@route('/')
def home():
	log.info('')
	#w_checked = ' checked' #if GPIO.input(22) else ''
	#r_checked = ' checked' #if GPIO.input(15) else ''
	#rel = (1,2,3,4,5,6,7,8)
	ports = (17,18,27,22,23,24,25,12)
	names = ('','','','','','','','')
	html = """<!DOCTYPE html>
<html><head><title>Relay Controller</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css">
<script src="http://code.jquery.com/jquery-1.10.2.min.js"></script>
<script src="http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js"></script>
<script>
$(document).ready(function() {
	$(".relay").change(function() {
		var onoff = $(this).is(":checked") ? 'on' : 'off';
		var id = $(this).prop("name");
		$.ajax({ url: onoff + '/'+ id });
	});
});
</script>
<style>
.ui-field-contain{margin: 0;}
</style>
</head>
<body>

<div data-role="page" id="page">
<div data-role="main" class="ui-content ">
<form>

	% for n in (0,1,2,3,4,5,6,7):

	<div class="ui-field-contain">
	{{n+1}}: <input type="checkbox" data-role="flipswitch" name="flip-{{n}}" id="flip-{{n}}" class="relay" checked=""/>
	<label for="flip-{{n}}">Flip toggle switch:</label>
	</div>
	% end
</form> 
</div>
</div> 
</body></html>"""
	
	return template(html,title='aerg')


@route('/on/<relay:int>')
def turnon(relay):
	port = ports[relay]
	log.info('on:' + str(port) )
	GPIO.setup(port, GPIO.OUT)
	GPIO.output(port,GPIO.LOW)
	log.info(GPIO.input(port))

@route('/off/<relay:int>')
def turnoff(relay):
	port = ports[relay]
	log.info('off:' + str(port) )
	GPIO.setup(port, GPIO.IN)
	GPIO.output(port,GPIO.HIGH)
	log.info(GPIO.input(port))

@route('/state/<relay:int>')
def getstate(relay):
	port = ports[relay]
	state = GPIO.input(port)
	log.info(state)

run(host = '0.0.0.0', port = '80', reloader=True)
#run(host = '0.0.0.0', port = '80')
