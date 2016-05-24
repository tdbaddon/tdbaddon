# -*- coding: utf-8 -*-

""" 
This plugin is 3rd party and not part of p2p-streams addon

Arenavision.in

"""


def clean(text):
	text = text.replace(u'\xda','U').replace(u'\xc9','E').replace(u'\xd3','O').replace(u'\xd1','N').replace(u'\xcd','I').replace(u'\xc1','A')
	return text
