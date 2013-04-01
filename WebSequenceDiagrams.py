import sublime, sublime_plugin, urllib, re, tempfile, os, desktop

def getTempPreviewPath(view):
    	tmp_filename = '%s.png' % view.file_name()
    	tmp_fullpath = os.path.join(tempfile.gettempdir(), tmp_filename)
    	return tmp_fullpath

def getSequenceDiagram(text, outputFile, style = 'default'):
	request = {}
	request["message"] = text
	request["style"] = style
	request["apiVersion"] = "1"

	url = urllib.urlencode(request)

	f = urllib.urlopen("http://www.websequencediagrams.com/", url)
	line = f.readline()
	f.close()

	expr = re.compile("(\?(img|pdf|png|svg)=[a-zA-Z0-9]+)")
	m = expr.search(line)

	if m == None:
	    print "Invalid response from server."
	    return False

	urllib.urlretrieve("http://www.websequencediagrams.com/" + m.group(0),
	        outputFile )

	return True

class WebsequencediagramsListener(sublime_plugin.EventListener):
    def on_post_save(self, view):
        if view.file_name().endswith(('.wsd')):
            temp_file = getTempPreviewPath(view)
            if os.path.isfile(temp_file):
                view.run_command('websequencediagrams')

class WebsequencediagramsCommand(sublime_plugin.TextCommand):
	def run(self, edit, target = 'browser'):
		region = self.view.visible_region()
		contents = self.view.substr(region)
		if not "participant" in contents:
			region = self.view.find('(participant .*\n)+', 0)
			participants = self.view.substr(region)
			contents = participants + contents
		style = "qsd"
		pngFile = getTempPreviewPath(self.view)
		if getSequenceDiagram(contents, pngFile, style):
			desktop.open(pngFile)


