import rpa as r

r.init()
r.url("https://duckduckgo.com")
r.type('//*[@name="q"]', "decentralisation[enter]")
r.wait()  # ensure results are fully loaded
r.snap("page", "results.png")
r.close()
