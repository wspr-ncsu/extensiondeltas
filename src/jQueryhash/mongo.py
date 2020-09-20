from mongoengine import *
from hashlib import sha1
import uuid
import datetime

# connect('analyzer', host="hulk.csc.ncsu.edu", port=27077, connect=False)
connect('analyzer', host="localhost", port=37017, connect=False)

#
# Hulk stuff.
#

class Manifest(DynamicEmbeddedDocument):
    pass


class Metadata(Document):
    hid = StringField(required=True)
    # scrapped time
    ts = DateTimeField(default=datetime.datetime.now)

    author = StringField()
    author_url = StringField()
    rating = FloatField()
    votes = IntField()
    num_votes = IntField()
    users = IntField()
    description = StringField()
    t = StringField()
    category = StringField()
    reviews = ListField(DictField())
    num_reviews = IntField()
    error = StringField()


class Extension(Document):
    hid = StringField(required=True)
    crx = FileField(unique=True)
    md5 = StringField()
    manifest = EmbeddedDocumentField(Manifest)
    files = ListField(FileField())
    metadata = ReferenceField(Metadata, reverse_delete_rule=CASCADE)


class Label(Document):
    name = StringField()
    # type of label
    t = StringField(default="user")

    def __repr__(self):
        return self.name


class Analysis(Document):
    extension = ReferenceField(Extension, reverse_delete_rule=CASCADE)
    hid = StringField(required=True)
    ts = DateTimeField(default=datetime.datetime.now)
    h = StringField()
    duration = FloatField()
    report = URLField()
    urls = ListField(StringField())
    result = StringField()
    netdump = FileField()
    netlogs = ListField()
    jslogs = ListField()
    nxdomainslogs = ListField()
    domainlogs = ListField()
    detections = ListField()
    labels = ListField(ReferenceField(Label), default=list)
    label = StringField()
    vm = IntField()
    users = IntField()
    avg_rating = FloatField()
    votes  = IntField()

    def clean(self):
        if self.h is None:
            self.h = sha1(str(uuid.uuid4())).hexdigest()


class ActivityLog(Document):
    analysis = ReferenceField(Analysis, reverse_delete_rule=CASCADE)
    hid = StringField()
    ts = LongField()
    action_type = IntField()
    api_name = StringField()
    args = StringField()
    page_url = StringField()
    arg_url = StringField()
    other = StringField()

    meta = {'allow_inheritance': True}


class ActivityLogFile(ActivityLog):
    args = FileField()


class NetworkLog(Document):
    analysis = ReferenceField(Analysis, reverse_delete_rule=CASCADE)
    ts = DateTimeField(default=datetime.datetime.now)
    domain = StringField()
    url = StringField()
    url_sha1 = StringField()
    status = IntField()
    content_type = StringField()
    content_hash = StringField()
    isjs = BooleanField()
    headers = ListField()


class HTTPHeader(Document):
    netlog = ReferenceField(NetworkLog, reverse_delete_rule=CASCADE)
    name = StringField()
    value = StringField()

class DomainLog(Document):
    analysis = ReferenceField(Analysis, reverse_delete_rule=CASCADE)
    ts = DateTimeField(default=datetime.datetime.now)
    domain = StringField()


class JsLog(Document):
    analysis = ReferenceField(Analysis, reverse_delete_rule=CASCADE)
    ts = DateTimeField(default=datetime.datetime.now)
    msg = StringField()
    origin = StringField()


class NXDomainLog(Document):
    analysis = ReferenceField(Analysis, reverse_delete_rule=CASCADE)
    ts = DateTimeField(default=datetime.datetime.now)
    domain = StringField()


class Detection(Document):
    # Analysis hash id
    h = StringField()
    # detection id
    did = IntField()
    # Description
    d = StringField()
    # Classification
    c = IntField()


class Queue(Document):
    ts = DateTimeField(default=datetime.datetime.now)
    priority = IntField(default=0)
    processed = IntField(default=0)
    crx = FileField()
    md5 = StringField()
    hid = StringField()
    # IP address of the submitter
    submitter = StringField()
    # feed? public submission?
    label = StringField()
    version = StringField(default="")
    sha256sum = StringField(default="")


class Feed(Document):
    hid = StringField()
    lastmod = StringField()

#
# Mystique stuff.
#

class MystiqueQueue(Document):
    name = StringField(default="")
    md5 = StringField()
    hid = StringField(default="")
    crx = FileField()
    processed = BooleanField(default=False)
    ts = DateTimeField(default=datetime.datetime.now)
    submitter = StringField()
    retries = IntField()
    version = StringField(default="")
    sha256sum = StringField(default="")

class MystiqueActivityLog(Document):
    md5 = StringField()
    time = LongField()
    action_type = IntField()
    api_name = StringField(default="")
    args = StringField(default="")
    page_url = StringField(default="")
    page_title = StringField(default="")
    arg_url = StringField(default="")
    other = StringField(default="")

class MystiqueNetworkLog(Document):
    md5 = StringField()
    ts = DateTimeField()
    req_url = StringField()
    req_header = StringField()
    status = IntField()
    is_js = BooleanField()

class MystiqueContentScripts(Document):
    md5 = StringField()
    content_script = FileField()

class Mystique(Document):
    md5 = StringField()
    result = StringField()
    taint_sources = FileField()
    taint_sinks = FileField()
    hulk_logs = FileField()
    analysis_start = DateTimeField()
    analysis_duration = FloatField()
    stdout = FileField()
    stderr = FileField()

class MystiqueWebstoreStats(Document):
    hid = StringField()
    users = IntField(default=-1)  # Only on failure to get user count.
    offered_by = StringField(default="")
    category = StringField(default="")
    description = StringField(default="")
    details = StringField(default="")
    additional_info = StringField(default="")
    ts = DateTimeField(default=datetime.datetime.now)

class ExtensionNames(Document):
    browser = StringField()
    hid = StringField()
    md5 = StringField()
    name = StringField()

#
# Third-party cookies stuff.
#

class CookiesAnalysisLog(Document):
    run_id = StringField()
    time = DateTimeField(default=datetime.datetime.now)
    url = StringField()
    success = BooleanField()
    taint_sources = FileField()
    has_tainted_cookies = BooleanField(default=False)
    tainted_cookies = FileField()
    taint_sinks_triggered = BooleanField(default=False)
    taint_sinks = FileField()
    net_dump = FileField()

#
# Publications.
#
class Publications(Document):
    name = StringField()
    pdf = FileField()
    bibtex = StringField()

#
# Access control.
#
class User(Document):
    email = StringField()
    password = StringField()
    firstname = StringField()
    lastname = StringField()
    affiliation = StringField()
    homepage = StringField()
    active = BooleanField()
    roles = ListField(ObjectIdField())
    confirmed_at = DateTimeField()
    last_login_at = DateTimeField()
    login_count = IntField()
    current_login_at = DateTimeField()
    current_login_ip = StringField()
    last_login_ip = StringField()

class Role(Document):
    name = StringField()

class apiFreqStorage(Document):
	name = StringField(required=True)
	apiFreqs = ListField(IntField())

class apiFreqStorageUpd(Document):
	hid = StringField(required=True)
	name = StringField(required=True)
	apiFreqs = ListField(IntField())
	sum0 = IntField()
	failed = ListField(StringField())

class apiFreqStorageUpdOrder(Document):
	hid = StringField(required=True)
	name = StringField(required=True)
	apiFreqs = ListField(IntField())
	sum0 = IntField()
	failed = ListField(StringField())

class apiFreqStorageUpdOrderA(Document):
	hid = StringField(required=True)
	name = StringField(required=True)
	apiFreqs = ListField(IntField())
	sum0 = IntField()
	failed = ListField(StringField())


class apiFreqStorageUpdOrderB(Document):
	hid = StringField(required=True)
	name = StringField(required=True)
	apiFreqsUpdated = ListField(IntField())
	apiFreqsNew = ListField(IntField())
	sum0 = IntField()
	failed = ListField(StringField())    


class allapib(Document):
	hid = StringField(required=True)
	name = StringField(required=True)
	apiFreqsAll = ListField(IntField())
	sumExt = IntField()
	sumOther = IntField()
	sumAll = IntField()    