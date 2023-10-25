import rpa as r

r.init(visual_automation=True, chrome_browser=False)
r.run("notepad.exe")

r.keyboard("[ctrl]s")

# r.keyboard('[enter]')
