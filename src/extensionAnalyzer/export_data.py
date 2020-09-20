import analyzer.db.mongo as mongo
import os

def tostring(detection_array):
    s = ""
    for d in detection_array:
        s += "[[%s-%s] %s]" % (d.c, d.did, d.d)
    return s


try:
    os.makedirs("/tank/data")
except:
    pass

feed_label=mongo.Label.objects(name="feed").first()
count = 0
md5s = {}

for anal in mongo.Analysis.objects(labels__contains=feed_label).order_by("-ts"):
    # no extension duplicates
    if anal.extension is None or anal.extension.md5 in md5s:
        continue
    crx = anal.extension.crx.read()
    if crx is None:
        continue
    md5s[anal.extension.md5] = True

    print "%s\t%s" % (anal.h, tostring(anal.detections))
    with open("/tank/data/%s.crx" % (anal.h), "wb") as f:
        f.write(crx)
    count += 1
    #if count > 10000:
    #    break
