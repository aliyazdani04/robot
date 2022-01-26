from requests import get
from re import findall
from rubika.client import Bot
from rubika.tools import Tools
from rubika.encryption import encryption
import time

print ("♡ WELCOME ♡")
print ("<Created By Ali Hl>")

bot = Bot(input("Please enter your Auth:"))
target=input("group guid: ")

print ("The robot was successfully activated.")

def hasInsult(msg):
	swData = [False,None]
	for i in open("dontReadMe.txt").read().split("\n"):
		if i in msg:
			swData = [True, i]
			break
		else: continue
	return swData

def hasAds(msg):
	links = list(map(lambda ID: ID.strip()[1:],findall("@[\w|_|\d]+", msg))) + list(map(lambda link:link.split("/")[-1],findall("rubika\.ir/\w+",msg)))
	joincORjoing = "joing" in msg or "joinc" in msg

	if joincORjoing: return joincORjoing
	else:
		for link in links:
			try:
				Type = bot.getInfoByUsername(link)["data"]["chat"]["abs_object"]["type"]
				if Type == "Channel":
					return True
			except KeyError: return False
			
answered = [bot.getGroupAdmins]
retries = {}
sleeped = False
# Creator = shayan Heydari (snipe4Kill)
plus= True

while True:
	try:
		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]
		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue
		
		open("id.db","w").write(str(messages[-1].get("message_id")))

		for msg in messages:
			if msg["type"]=="Text" and not msg.get("message_id") in answered:
				if not sleeped:
					if msg.get("text") == "آنلاینی" and msg.get("author_object_guid") in admins :
						bot.sendMessage(target, "آره عشقم فعالم😉❤", message_id=msg.get("message_id"))
						
					elif hasAds(msg.get("text")) and not msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [str(msg.get("message_id"))])

					elif msg.get("text").startswith("add") :
						bot.invite(target, [bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"]])
						bot.sendMessage(target, "کاربر مورد نظر افزوده شد!", message_id=msg.get("message_id"))

					elif msg.get("text") == "دستورات":
						bot.sendMessage(target, "لیسـت دستـــورات ربـات 🤖:\n\n⚜🤖 (ربات آنلاینی؟) : فعال یا غیر فعال بودن بات\n\n⚜❎ (پایان) : غیر فعال سازی بات\n\n⚜✅ (شروع) : فعال سازی بات\n\n⚜🕘 (ساعت) : ساعت\n\n⚜📅 (تاریخ میلادی) : تاریخ\n\n⚜🗑 (پاک) : حذف پیام با ریپ بر روی آن\n\⚜🔒 (بستن گروه) : بستن چت در گروه\n\n⚜🔓 (باز کردن گروه) : باز کردن چت در گروه\n\n🔱❌ (بن) : حذف کاربر با ریپ زدن\n\n⚜✉ send : ارسال پیام با استفاده از ایدی\n\n🔱☣ add : افزودن کاربر به گپ با ایدی\n\n⚜📜 (دستورات) : لیست دستورات ربات\n\n⚜📟(cal):ماشین حساب(مثال: cal 3 * 4 )\n\n⚜🤣 (جوک) : ارسال جوک\n\n⚜🪄(فونت): ارسال فونت (مثال: فونت ali)\n\n⚜💻(پینگ):گرفتن پینگ سایت با آدرس سایت\n\n⚜📚(معنی):معنی کلماته فارسی\n\n⛈⚡️ (!weather) : آب و هوا\n\n⚜⏳ (زمان) : تاریخ و ساعت\n\n⚜🎎 (بیوگرافی) : بیوگرافی\n\n⚜😂 (پ ن پ) : جوک پ ن پ\n\n⚜😂 (الکی مثلا) : جوک الکی مثلا\n\n⚜🧔🏻‍♂ (حدیث) : سخن بزرگان\n\n⚜📖 (داستان) : داستان های کوتاه\n\n⚜🧠 (دانستنی) : دانستنی ها\n\n⚜🕴🏼 (دیالوگ) : دیالوگ های ماندگار\n\n⚜🤲🏽 (ذکر) : ذکر روز ها\n\n⚜🌞(اوقات): ساعت طلوع و غروب و اذان\n\n⚜💵(ارز): طلا و ارز (مثال:ارز tala)\n\n⚜🕯(فال):فال حافظ (مثال:فال 54)\n\n⚜🕯(غزل):غزل سعدی\n\n⚜🎼(آهنگ):جستجو آهنگ\n\n⚜✏️(font):فونت فارسی\n\n⚜🎉(عید):زمان باقی مانده تا عید نوروز\n\n⚜💰(بورس): وضعیت بورس\n\nسازنده @Ali_yazdani04")
					elif msg.get("text").startswith("cal"):
						msd = msg.get("text")
						if plus == True:
							try:
								call = [msd.split(" ")[1], msd.split(" ")[2], msd.split(" ")[3]]
								if call[1] == "+":
									am = float(call[0]) + float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
									plus = False
							
								elif call[1] == "-":
									am = float(call[0]) - float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
							
								elif call[1] == "*":
									am = float(call[0]) * float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
							
								elif call[1] == "/":
									am = float(call[0]) / float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
							except IndexError:
								bot.sendMessage(target, "دستور رو اشتباه وارد کردی😂🤦‍♂️" ,message_id=msg.get("message_id"))
						plus= True
					elif msg.get("text").startswith("send") :
						bot.sendMessage(bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"], "شما یک پیام ناشناس دارید:\n"+" ".join(msg.get("text").split(" ")[2:]))
						bot.sendMessage(target, "پیام ناشناستو ارسال کردم😉👌", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("سلام"):
						bot.sendMessage(target, "ثلام برتو😍🌹", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("صلم"):
						bot.sendMessage(target, "ثلم😑😐", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اخطار":
						bot.sendMessage(target, "دیگه تکرار نشه🤨😡", message_id=msg.get("message_id"))
					
					
					elif msg.get("text").startswith("صلام"):
						bot.sendMessage(target, "سلام😐🌹", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("سلم"):
						bot.sendMessage(target, "ثلم😍🌹", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("سیلام"):
						bot.sendMessage(target, "سلاااامم😍😍", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("صیلام"):
						bot.sendMessage(target, "ثلام😍🌹", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("های"):
						bot.sendMessage(target, "hi my friend🤝🏼😍", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("هلو"):
						bot.sendMessage(target, "hi my friend🤝🏼😍", message_id=msg.get("message_id"))
					
					elif msg.get("text").startswith("خوبی"):
						bot.sendMessage(target, "تو چطوری؟🤪", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("چه خبر"):
						bot.sendMessage(target, "ســلامـتیت😍♥", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "چخبر":
						bot.sendMessage(target, "ســلامـتیت😍♥", message_id=msg.get("message_id"))
					
					elif msg.get("text") == "قربونت":
						bot.sendMessage(target, "فدات😘", message_id=msg.get("message_id"))
					
					elif msg.get("text") == "نوکرتم":
						bot.sendMessage(target, "میخامتو خرجت میکنم🤝🏼🤝🏼", message_id=msg.get("message_id"))
					
					elif msg.get("text") == "جون":
						bot.sendMessage(target, "بگم علی بیاد🤔🤨", message_id=msg.get("message_id"))
					
					elif msg.get("text") == "علی کیه":
						bot.sendMessage(target, " عشقه منه علی همه کسمه😍❤", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "سوکنیه":
						bot.sendMessage(target, "بدبختو نگا کارش به سوکینه گیره😂😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "کوکب":
						bot.sendMessage(target, "کوکب چیه بیتربیت کوکب خانم🤨🤨", message_id=msg.get("message_id"))
					
					elif msg.get("text") == "حوصلم":
						bot.sendMessage(target, "موزو بیشتر دوس داری یا خیارو؟🤔🥒🍌", message_id=msg.get("message_id"))
					
					elif msg.get("text") == "کص":
						bot.sendMessage(target, "بیتربیت حرفه زشت نزن😡😠", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "رل":
						bot.sendMessage(target, "بپر پیوی سوکینه بدرد هم میخورید😂😉", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "خاموش":
						bot.sendMessage(target, "کرم نریز🤨🤨", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🤣":
						bot.sendMessage(target, "جر نخوری حالا😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اره بگو":
						bot.sendMessage(target, "باش برو پیویش  @ali_yazdani04", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "چخبر":
						bot.sendMessage(target, "ســلامـتیت😍♥", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "علی":
						bot.sendMessage(target, "با عشقه من کار داری؟🤔", message_id=msg.get("message_id"))
					
					elif msg.get("text") == "خبی":
						bot.sendMessage(target, "من انقده اصفونیا را دوست دارم که نگو😍❤", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "رباط":
						bot.sendMessage(target, "😑 رباتو اینجوری مینویسن اگه بلد نیستی", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "گوه":
						bot.sendMessage(target, "خب تو بخور💩😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "که که ":
						bot.sendMessage(target, "از دهنت میچکه😂💩", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "ککه":
						bot.sendMessage(target, "از دهنت میچکه😂💩", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اصلمو بده":
						bot.sendMessage(target, "علیم اچ ال/ اچ الم علی", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اصل":
						bot.sendMessage(target, "باتم اچ ال/اچ الم ربات😂   بقیش هم توکانال بخون @robotHL", message_id=msg.get("message_id"))
					
					elif msg.get("text") == "ریده":
						bot.sendMessage(target, "خودت ریدی بیتربیت🤨🤨", message_id=msg.get("message_id"))
					
					elif msg.get("text") == "صیک":
						bot.sendMessage(target, "تو اونجات😂👌🏼", message_id=msg.get("message_id"))
					
					elif msg.get("text") == "سیک":
						bot.sendMessage(target, "تو اونجات😂👌🏼", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "کصکش":
						bot.sendMessage(target, "به من نگو کصکش زن دارم🤦‍♂", message_id=msg.get("message_id"))	
					
					elif msg.get("text") == "کسکش":
						bot.sendMessage(target, "به من نگو کسکش زن دارم🤦‍♂", message_id=msg.get("message_id"))
					
					elif msg.get("text") == "جنده":
						bot.sendMessage(target, "خاک ب سرم🤦‍♂️🤦‍♂️😶", message_id=msg.get("message_id"))
					
					elif msg.get("text") == "شیوا":
						bot.sendMessage(target, "سگ شیوا را آخه صدا میکنه که تو صداش میکنی😐😂😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "لینک":
						bot.sendMessage(target, "بپر تو بیو😘😘😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "خفه شو":
						bot.sendMessage(target, "💩🦓تو کونه خر چپه شو", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "محمد":
						bot.sendMessage(target, "پتوعو بنداز رو عمت😂😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "جان":
						bot.sendMessage(target, "اگه خوشت اومد که بگم شیوا بیاد😋😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "منم":
						bot.sendMessage(target, "خب به عنم😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "مرگ":
						bot.sendMessage(target, "سرش بتمرگ😂💖", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "ماشین":
						bot.sendMessage(target, "باکون برین جاشین😂🌹", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "کیر":
						bot.sendMessage(target, "به دندون بگیر😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "باشه":
						bot.sendMessage(target, "بچوس تا لاش وا شه😂😂🌹🌹", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "گوه نخور":
						bot.sendMessage(target, "شاشیدم سر نخور😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "ککه":
						bot.sendMessage(target, "از دهنت میچکه😂💩", message_id=msg.get("message_id"))	
								
					elif msg.get("text") == "قوانین":
						name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
						bot.sendMessage(target, "🌀 قوانین گروه {name} :\n\n⛔️ ارسال لینک ممنوع!\n⛔️ ارسال فحش ممنوع!\n⛔️ توهین به کسی ممنوع!\n⛔️ارسال از کانال (فروارد) ممنوع!", message_id=msg.get("message_id"))
							
					elif msg.get("text").startswith("ربات"):
						bot.sendMessage(target, "جــونـم😁💋", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "استغفرالله":
						bot.sendMessage(target, "توبه توبه", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "سبحان الله":
						bot.sendMessage(target, "😱😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "😂":
						bot.sendMessage(target, "😂😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "سجاد":
						bot.sendMessage(target, "سرش به صد جات😂🤝🏼💖", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "زر نزن":
						bot.sendMessage(target, "خب تو زر بزن😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "معصومه":
						bot.sendMessage(target, "کونت برام کپسوله😂🌹", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "مانی":
						bot.sendMessage(target, "تو کونت قوطی رانی😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "امین":
						bot.sendMessage(target, "کون بده بعد برین- سوراخ کونت به این💖😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "هدایت":
						bot.sendMessage(target, "یه کون بده فدایت😂💖", message_id=msg.get("message_id"))
					
					elif msg.get("text") == "علی":
						bot.sendMessage(target, "وقتی دیدش در نری.اینو بخوری اولی💖😂😋", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "هانی":
						bot.sendMessage(target, "تو الکسیس من جانی😋😈", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "صابر":
						bot.sendMessage(target, "Fuck Your Mother😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "جواد":
						bot.sendMessage(target, "کیرم کنجه لبات😂😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "نگار":
						bot.sendMessage(target, "کردمت شدی رستگار😂😂💖", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "هادی":
						bot.sendMessage(target, "توکونت تفنگ بادی😂😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "ندا":
						bot.sendMessage(target, "ساک بزن بی سر و صدا😂😂❤", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "فاطی":
						bot.sendMessage(target, "عمت کرده قاطی.کونت شده خاکی.خوراکه انگشته فاکی😂🥒❤", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "وحید":
						bot.sendMessage(target, "ریدم تو اسمت شدید😂💩", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "آریا":
						bot.sendMessage(target, "سرشو بگیر را بیا😂😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "پژو":
						bot.sendMessage(target, "اینو بگیر بجو😂🥒", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "کوفت":
						bot.sendMessage(target, "گایدنت مفت😂💖", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "کوفته":
						bot.sendMessage(target, "گایدنت موفته😂😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "ایمان":
						bot.sendMessage(target, "تو کونت پاکت سیمان😂💖", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "مرضیه":
						bot.sendMessage(target, "نوار بهداشتیت قرضیه😂😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "امیر":
						bot.sendMessage(target, "بیا زیرش بمیر😂😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "عمیر":
						bot.sendMessage(target, "بیا زیرش بمیر😂💖", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "غلط کردی":
						bot.sendMessage(target, "سرشو لقت کردی😂😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "ماعده":
						bot.sendMessage(target, "کیرمو توکونت جا بده😂❤", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "عشقم":
						bot.sendMessage(target, "بکش پایین تنشم😂💧", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "مهناز":
						bot.sendMessage(target, "بخور کیرمو با ناز😂❤", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "دیوس":
						bot.sendMessage(target, "دولاشو سرشو ببوس نخاستی کونمو ببوس❤💖😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "دیوص":
						bot.sendMessage(target, "دولاشو سرشو ببوس نخاستی کونمو ببوس❤💖😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "دیوث":
						bot.sendMessage(target, "دولاشو سرشو ببوس نخاستی کونمو ببوس❤💖😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "نازنین":
						bot.sendMessage(target, "لخت شو بخواب رو زمین🤝🏼💧💖😈", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "احسان":
						bot.sendMessage(target, "کردمت پشت نیسان🤝🏼😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "میلاد":
						bot.sendMessage(target, "از مامانت بپرس دیشب به کی داد😂😂💖", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "امید":
						bot.sendMessage(target, "بابام پرده ننتو درید😂😂💖", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "لیلا":
						bot.sendMessage(target, "بشو دولا. بخور یالا😂😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "حامد":
						bot.sendMessage(target, "کردمت با روغن جامد😂💖", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "عجب":
						bot.sendMessage(target, "کیره مش رجب. دست زدی بش بود چند وجب؟😂🤔", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "عباس":
						bot.sendMessage(target, "عنم برات مرباس😂💖", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "نازی":
						bot.sendMessage(target, "چقد شبیه غازی😂😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "کثافت":
						bot.sendMessage(target, "ریدم تو اون قیافت با نرمی و لطافت😂😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "کثافط":
						bot.sendMessage(target, "ریدم تو اون قیافت با نرمی و لطافت😂😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "مبینا":
						bot.sendMessage(target, "بخور ازینا😈🥒", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "تو":
						bot.sendMessage(target, "سرت تو گوه😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "سحر":
						bot.sendMessage(target, "خاستی بدی بده یه خبر😂😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "فرشته":
						bot.sendMessage(target, "ممه بدی جات بهشته.ندی کارت خیلی زشته😂😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "ستاره":
						bot.sendMessage(target, "کس ننت میخاره😂🥒", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "اکبر":
						bot.sendMessage(target, "لاپات شیشتا کفتر😂😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "پری":
						bot.sendMessage(target, "رو کونت بسته رو سری😂😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "پریا":
						bot.sendMessage(target, "اونجا ها نریا😂😂❤", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "هستی":
						bot.sendMessage(target, "تو کونت ترمز دستی😂❤", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "امیرعلی":
						bot.sendMessage(target, "به من میدی یا بغلی؟😂🤝🏼", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "متین":
						bot.sendMessage(target, "بشین روش برین😂", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "زهرا":
						bot.sendMessage(target, "مامانت رفت به صحرا😂💖", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "حسن":
						bot.sendMessage(target, "تخمام برات دل واپسن😂💖", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "آفرین":
						bot.sendMessage(target, "میخامت💖", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "😘":
						bot.sendMessage(target, "چه خوب بوس میکنی😍😍", message_id=msg.get("message_id"))		
						
					elif msg.get("text").startswith("گاییدم"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("نگاییدم"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("kir"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("کیر"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("کص"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("کون"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("مادرت"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("مادرتو"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("کیرم"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("کوص"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("کوس"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("کبص"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("کوبص"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("کسکش"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("بی ناموس"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("بیناموس"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("بی ناموص"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("بیناموص"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text") == "سنجاق" and msg.get("author_object_guid") in admins :
						    bot.pin(target, msg["reply_to_message_id"])
						    bot.sendMessage(target, "پیام مورد نظر با موفقیت سنجاق شد!", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "برداشتن سنجاق" and msg.get("author_object_guid") in admins :
						    bot.unpin(target, msg["reply_to_message_id"])
						    bot.sendMessage(target, "پیام مورد نظر از سنجاق برداشته شد!", message_id=msg.get("message_id"))

					elif msg.get("text") == "پایان" and msg.get("author_object_guid") in admins :
						sleeped = True
						bot.sendMessage(target, "ربات با موفقیت خاموش شد!", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("پینگ"):
						
						try:
							responser = get(f"https://api.codebazan.ir/ping/?url={msg.get('text').split()[1]}").text
							bot.sendMessage(target, responser,message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
						
					elif msg.get("text").startswith("ارز"):
						
						try:
							responser = get(f"http://api.codebazan.ir/arz/?type={msg.get('text').split()[1]}").text
							bot.sendMessage(target, responser,message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("معنی"):
						
						try:
							responser = get(f"https://api.codebazan.ir/vajehyab/?text={msg.get('text').split()[1]}").text
							bot.sendMessage(target, responser,message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("قیمت موبایل"):
						
						try:
							responser = get(f"https://api.codebazan.ir/mobile-price/?type={msg.get('text').split()[1]}").text
							bot.sendMessage(target, responser,message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
					
					elif msg.get("text").startswith("ویکی"):
						
						try:
							responser = get(f"https://api.codebazan.ir/wiki/?search={msg.get('text').split()[1]}").text
							bot.sendMessage(target, responser,message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
					
					elif msg.get("text").startswith("خواب"):
						
						try:
							responser = get(f"https://api.codebazan.ir/tabir/?text={msg.get('text').split()[1]}").text
							bot.sendMessage(target, responser,message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("اوقات"):
						
						try:
							responser = get(f"https://api.codebazan.ir/owghat/?city={msg.get('text').split()[1]}").text
							bot.sendMessage(target, responser,message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("فال"):
						
						try:
							responser = get(f"https://api.codebazan.ir//ghazaliyathafez/?type=ghazal&num={msg.get('text').split()[1]}").text
							bot.sendMessage(target, responser,message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])	
					
					elif msg.get("text").startswith("font"):
						
						try:
							responser = get(f"https://api.codebazan.ir/font/?type=fa&text={msg.get('text').split()[1]}").text
							bot.sendMessage(target, responser,message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])		

		
					elif msg.get("text").startswith("!trans"):
						
						try:
							responser = get(f"https://api.codebazan.ir/translate/?type=json&from=en&to=fa&text={msg.get('text').split()[1:]}").json()
							al = [responser["result"]]
							bot.sendMessage(msg.get("author_object_guid"), "پاسخ به ترجمه:\n"+"".join(al)).text
							bot.sendMessage(target, "نتیجه رو برات ارسال کردم😘", message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])

					elif msg.get("text").startswith("فونت"):
						#print("\n".join(list(response["result"].values())))
						try:
							response = get(f"https://api.codebazan.ir/font/?text={msg.get('text').split()[1]}").json()
							bot.sendMessage(msg.get("author_object_guid"), "\n".join(list(response["result"].values())[:110])).text
							bot.sendMessage(target, "نتیجه رو برات ارسال کردم😘", message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])



					elif msg.get("text").startswith("جوک"):
						
						try:
							response = get("https://api.codebazan.ir/jok/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
									
					elif msg.get("text").startswith("بورس"):
						
						try:
							response = get("https://api.codebazan.ir/bours/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])				
							
					elif msg.get("text").startswith("غزل"):
						
						try:
							response = get("https://api.codebazan.ir/ghazalsaadi/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("چیستان"):
						
						try:
							response = get("https://api.codebazan.ir/chistan/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])		
							
					elif msg.get("text").startswith("اخبار"):
						
						try:
							response = get("https://api.codebazan.ir/khabar/?kind=iran").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("ذکر"):
						
						try:
							response = get("http://api.codebazan.ir/zekr/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("حدیث"):
						
						try:
							response = get("http://api.codebazan.ir/hadis/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("بیوگرافی"):
						
						try:
							response = get("https://api.codebazan.ir/bio/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg["text"].startswith("!weather"):
						response = get(f"https://api.codebazan.ir/weather/?city={msg['text'].split()[1]}").json()
						#print("\n".join(list(response["result"].values())))
						try:
							bot.sendMessage(msg["author_object_guid"], "\n".join(list(response["result"].values())[:20])).text
							bot.sendMessage(target, "نتیجه بزودی برای شما ارسال خواهد شد...", message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "متاسفانه نتیجه‌ای موجود نبود!", message_id=msg["message_id"])
						
							
					elif msg.get("text").startswith("دیالوگ"):
						
						try:
							response = get("http://api.codebazan.ir/dialog/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("دانستنی"):
						
						try:
							response = get("http://api.codebazan.ir/danestani/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("همسر"):
						
						try:
							response = get("https://api.codebazan.ir/name/?type=json").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])				
					elif msg.get("text").startswith("داستان"):
						
						try:
							response = get("http://api.codebazan.ir/dastan/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("پ ن پ"):
						
						try:
							response = get("http://api.codebazan.ir/jok/pa-na-pa/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("الکی مثلا"):
						
						try:
							response = get("http://api.codebazan.ir/jok/alaki-masalan/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("زمان"):
						
						try:
							response = get("https://api.codebazan.ir/time-date/?td=all").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])

					elif msg.get("text") == "ساعت":
						bot.sendMessage(target, f"Time : {time.localtime().tm_hour} : {time.localtime().tm_min} : {time.localtime().tm_sec}", message_id=msg.get("message_id"))

					elif msg.get("text") == "تاریخ میلادی":
						bot.sendMessage(target, f"Date: {time.localtime().tm_year} / {time.localtime().tm_mon} / {time.localtime().tm_mday}", message_id=msg.get("message_id"))

					elif msg.get("text") == "پاک" and msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [msg.get("reply_to_message_id")])
						bot.sendMessage(target, "پیام مورد نظر پاک شد...", message_id=msg.get("message_id"))


					elif msg.get("text") == "بستن گروه" and msg.get("author_object_guid") in admins :
						print(bot.setMembersAccess(target, ["ViewMembers","ViewAdmins","AddMember"]).text)
						bot.sendMessage(target, "گروه بسته شد!", message_id=msg.get("message_id"))

					elif msg.get("text") == "باز کردن گروه" and msg.get("author_object_guid") in admins :
						bot.setMembersAccess(target, ["ViewMembers","ViewAdmins","SendMessages","AddMember"])
						bot.sendMessage(target, "گروه باز شد!", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("بن") and msg.get("author_object_guid") in admins :
						try:
							guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["abs_object"]["object_guid"]
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							if not guid in admins :
								bot.banGroupMember(target, guid)
								bot.sendMessage(target, f"کاربر مورد نظر بن شد !", message_id=msg.get("message_id"))
							else :
								bot.sendMessage(target, f"خطا", message_id=msg.get("message_id"))
								
						except IndexError:
							a = bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"]
							if a in admins:
								bot.sendMessage(target, f"خطا", message_id=msg.get("message_id"))
							else:
								bot.banGroupMember(target, bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"])
								bot.sendMessage(target, f"کاربر مورد نظر بن شد !", message_id=msg.get("message_id"))

				else:
					if msg.get("text") == "شروع" and msg.get("author_object_guid") in admins :
						sleeped = False
						bot.sendMessage(target, "ربات شروع به فعالیت کرد!", message_id=msg.get("message_id"))

			elif msg["type"]=="Event" and not msg.get("message_id") in answered and not sleeped:
				name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
				data = msg['event_data']
				if data["type"]=="RemoveGroupMembers":
					user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"سعی کن همیشه تو زندگیت ادم باشی🙃از اینجا ریمت زدیم شاید بفهمی اشتباهت کجا بوده^_^", message_id=msg["message_id"])
				
				elif data["type"]=="AddedGroupMembers":
					user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"های {user} به گروه {name} خوش اومدی😍❤️\nلطفا قوانین رو رعایت کن👌🙁\n\nمتعلق به : @ali_yazdani04", message_id=msg["message_id"])
				
				elif data["type"]=="LeaveGroup":
					user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"مراقبت کن😈😘", message_id=msg["message_id"])
					
				elif data["type"]=="JoinedGroupByLink":
					user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"hello {user} به گروه {name} خوش اومدی😍❤️\nلطفا قوانین رو رعایت کن👌🙁\n\nمتعلق به : @ali_yazdani04", message_id=msg["message_id"])

			answered.append(msg.get("message_id"))

	except KeyboardInterrupt:
		exit()

	except Exception as e:
		if type(e) in list(retries.keys()):
			if retries[type(e)] < 3:
				retries[type(e)] += 1
				continue
			else:
				retries.pop(type(e))
		else:
			retries[type(e)] = 1
			continue
