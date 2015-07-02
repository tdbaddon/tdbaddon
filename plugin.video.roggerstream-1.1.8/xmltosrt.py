#!/usr/bin/python
# -*- encoding:utf-8 -*-


import re, sys

def cleanHtml(dirty):
    clean = re.sub('&quot;', '\"', dirty)
    clean = re.sub('&#039;', '\'', clean)
    clean = re.sub('&#215;', 'x', clean)
    clean = re.sub('&#038;', '&', clean)
    clean = re.sub('&#8216;', '\'', clean)
    clean = re.sub('&#8217;', '\'', clean)
    clean = re.sub('&#8211;', '-', clean)
    clean = re.sub('&#8220;', '\"', clean)
    clean = re.sub('&#8221;', '\"', clean)
    clean = re.sub('&#8212;', '-', clean)
    clean = re.sub('&amp;', '&', clean)
    clean = re.sub("`", '', clean)
    clean = re.sub('<em>', '[I]', clean)
    clean = re.sub('</em>', '[/I]', clean)
    return clean

# Pattern to identify a subtitle and grab start, duration and text.
pat = re.compile(r'<?text start="(\d+\.\d+)" dur="(\d+\.\d+)">(.*)</text>?')

def parseLine(text):
	"""Parse a subtitle."""
	m = re.match(pat, text)
	if m:
		return (m.group(1), m.group(2), m.group(3))
	else:
		return None

def formatSrtTime(secTime):
	"""Convert a time in seconds (google's transcript) to srt time format."""
	sec, micro = str(secTime).split('.')
	m, s = divmod(int(sec), 60)
	h, m = divmod(m, 60)
	#return "{:02}:{:02}:{:02},{}".format(h,m,s,micro)
	return "%.0f:%.0f:%.0f,%.0f" % (h,m,s,float(micro))

def convertHtml(text):
	"""A few HTML encodings replacements.
	&amp;#39; to '
	&amp;quot; to "
	"""
	return cleanHtml(text.replace('&amp;#39;', "'").replace('&amp;quot;', '"'))

def printSrtLine(i, elms):
	"""Print a subtitle in srt format."""
	return "%s\n%s --> %s\n%s\n\n" % (i, formatSrtTime(elms[0]), formatSrtTime(float(elms[0])+float(elms[1])), convertHtml(elms[2]))

fileName = sys.argv[1]

def main(fileName):
	"""Parse google's transcript and write the converted data in srt format."""
	with open(fileName, 'rb') as infile:
		buf = []
		for line in infile:
			buf.append(line.rstrip('\n'))
	# Split the buffer to get one string per tag.
	buf = "".join(buf).split('><')
	i = 0
	srtfileName = fileName.replace('.xml', '.srt')
	with open(srtfileName, 'w') as outfile:
		for text in buf:
			parsed = parseLine(text)
			if parsed:
				i += 1
				outfile.write(printSrtLine(i, parsed))
	print('DONE (%s)' % (srtfileName))

if __name__ == "__main__":
	main(fileName)
