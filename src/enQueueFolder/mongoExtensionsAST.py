from mongoengine import *
import datetime
import mongoExtensionsAST as mongo

# DB_HOST = os.environ.get("DB_HOST", "localhost")
# DB_PORT = int(os.environ.get("DB_PORT", "37017"))
# connect("extensionsASTnpantel", username="npantel", host=DB_HOST, port=DB_PORT)
connect("analyzer", host="localhost", port=27017)

class AstDiffFiles(Document):
	hid = StringField(required=True)
	nameBoth = StringField()
	fileAst = FileField()


class AstDiffFilesUnobfuscated(Document):
	hid = StringField(required=True)
	nameBoth = StringField()
	fileAst = FileField()
	
class AstDiffFilesUnobfuscatedNew(Document):
	hid = StringField(required=True)
	nameBoth = StringField()
	fileAst = FileField()
	length = IntField()

class diffStore(Document):
	hid1 = StringField(required=True)
	hid2 = StringField(required=True)
	nameBoth1 = StringField()
	nameBoth2 = StringField()
	commonLength = IntField()
	commonAPI = FileField()
	similarityRatio = FloatField()


class diffStoreUnobfuscated(Document):
	hid1 = StringField(required=True)
	hid2 = StringField(required=True)
	nameBoth1 = StringField()
	nameBoth2 = StringField()
	commonLengthTotal = IntField()
	commonAPITotal = FileField()
	commonLengthConseq = IntField()
	commonAPIConseq = FileField()
	commonLengthTotalWithoutA = IntField()
	commonAPITotalWithoutA = FileField()
	commonLengthConseqWithoutA = IntField()
	commonAPIConseqWithoutA = FileField()
	percATotal = FloatField()
	percAConseq = FloatField()
	similarityRatio = FloatField()          
	similarityRatioWithoutA = FloatField()

class diffStoreUnobfuscatedNew(Document):
	hid1 = StringField(required=True)
	hid2 = StringField(required=True)
	nameBoth1 = StringField()
	nameBoth2 = StringField()
	commonLengthTotal = IntField()
	commonAPITotal = FileField()
	commonLengthConseq = IntField()
	commonAPIConseq = FileField()
	commonLengthTotalWithoutA = IntField()
	commonAPITotalWithoutA = FileField()
	commonLengthConseqWithoutA = IntField()
	commonAPIConseqWithoutA = FileField()
	percATotal = FloatField()
	percAConseq = FloatField()
	similarityRatio = FloatField()          
	similarityRatioWithoutA = FloatField()	

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

class allapia(Document):
	hid = StringField(required=True)
	name = StringField(required=True)
	apiFreqsAll = ListField(IntField())
	sumAll = IntField()

class allapib(Document):
	hid = StringField(required=True)
	name = StringField(required=True)
	apiFreqsAll = ListField(IntField())
	sumExt = IntField()
	sumOther = IntField()
	sumAll = IntField()

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
