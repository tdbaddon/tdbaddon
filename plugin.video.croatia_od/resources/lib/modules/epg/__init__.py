


def get_current_epg(id):
	if id.isdigit() or id.endswith('.xml'):
		import mojtv
		return mojtv.get_current_epg(id)

	elif id.startswith('bleb'):
		import bleb
		return bleb.get_current_epg(id.split('-')[1])

	elif id.startswith('siol'):
		import siol
		return siol.get_current_epg(id.split('-')[1])

	elif id.startswith('mts'):
		import mts
		return mts.get_current_epg(id.replace('mts-',''))

	else:
		return 'Nema informacija'