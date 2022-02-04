from requests import get
from re import findall
import os
import glob
from rubika.client import Bot
import requests
from rubika.tools import Tools
from rubika.encryption import encryption
from gtts import gTTS
from mutagen.mp3 import MP3
import time
import random
import urllib
import io

print ("welcome, Created By Ali HL \n")

print ("Please subscribe to the channel to receive updates! : for Rubika : @robotHL\n")

bot = Bot(input("Please enter your Auth:"))
target=input("Please Enter Your Guid (Group): ")

print ("\nThe robot was successfully activated.")

def hasAds(msg):
	links = ["http://","https://",".ir",".com",".org",".net",".me"]
	for i in links:
		if i in msg:
			return True
			
def hasInsult(msg):
	swData = [False,None]
	for i in open("dontReadMe.txt").read().split("\n"):
		if i in msg:
			swData = [True, i]
			break
		else: continue
	return swData
	
# static variable
answered, sleeped, retries = [], False, {}

alerts, blacklist = [] , []

def alert(guid,user,link=False):
	alerts.append(guid)
	coun = int(alerts.count(guid))

	haslink = ""
	if link : haslink = "گزاشتن لینک در گروه ممنوع میباشد .\n\n"

	if coun == 1:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (1/3) اخطار دریافت کرده اید .\n\nپس از دریافت 3 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")
	elif coun == 2:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (2/3) اخطار دریافت کرده اید .\n\nپس از دریافت 3 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")

	elif coun == 3:
		blacklist.append(guid)
		bot.sendMessage(target, "🚫 کاربر [ @"+user+" ] \n (3/3) اخطار دریافت کرد ، بنابراین اکنون اخراج میشود .")
		bot.banGroupMember(target, guid)


while True:
	# time.sleep(15)
	try:
		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]

		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue

		for msg in messages:
			try:
				if msg["type"]=="Text" and not msg.get("message_id") in answered:
					if not sleeped:
						if hasAds(msg.get("text")) and not msg.get("author_object_guid") in admins :
							guid = msg.get("author_object_guid")
							user = bot.getUserInfo(guid)["data"]["user"]["username"]
							bot.deleteMessages(target, [msg.get("message_id")])
							alert(guid,user,True)

						elif msg.get("text") == "!stop" or msg.get("text") == "/stop" and msg.get("author_object_guid") in admins :
							try:
								sleeped = True
								bot.sendMessage(target, "✅ ربات اکنون خاموش است", message_id=msg.get("message_id"))
							except:
								print("err off bot")
								
						elif msg.get("text") == "!restart" or msg.get("text") == "/restart" and msg.get("author_object_guid") in admins :
							try:
								sleeped = True
								bot.sendMessage(target, "در حال راه اندازی مجدد...", message_id=msg.get("message_id"))
								sleeped = False
								bot.sendMessage(target, "ربا‌ت با موفقیت مجددا راه اندازی شد!", message_id=msg.get("message_id"))
							except:
								print("err Restart bot")
								
						elif msg.get("text").startswith("سازنده") and msg.get("author_object_guid") in creator :
							try:
								bot.sendMessage(target, "سلا‌م با‌با شما سازنده من هستی !", message_id=msg.get("message_id"))
							except:
								print("err admin")
								
						elif msg.get("text").startswith("حذف") and msg.get("author_object_guid") in admins :
							try:
								number = int(msg.get("text").split(" ")[1])
								answered.reverse()
								bot.deleteMessages(target, answered[0:number])

								bot.sendMessage(target, "✅ "+ str(number) +" پیام اخیر با موفقیت حذف شد", message_id=msg.get("message_id"))
								answered.reverse()

							except IndexError:
								bot.deleteMessages(target, [msg.get("reply_to_message_id")])
								bot.sendMessage(target, "✅ پیام با موفقیت حذف شد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("اخراج") and msg.get("author_object_guid") in admins :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									bot.banGroupMember(target, guid)
									# bot.sendMessage(target, "✅ کاربر با موفقیت از گروه اخراج شد", message_id=msg.get("message_id"))
								else :
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", message_id=msg.get("message_id"))
									
							except IndexError:
								bot.banGroupMember(target, bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"])
								# bot.sendMessage(target, "✅ کاربر با موفقیت از گروه اخراج شد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ دستور اشتباه", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("افزودن") or msg.get("text").startswith("!add") :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"]
								if guid in blacklist:
									if msg.get("author_object_guid") in admins:
										alerts.remove(guid)
										alerts.remove(guid)
										alerts.remove(guid)
										blacklist.remove(guid)

										bot.invite(target, [guid])
									else:
										bot.sendMessage(target, "❌ کاربر محدود میباشد", message_id=msg.get("message_id"))
								else:
									bot.invite(target, [guid])
									# bot.sendMessage(target, "✅ کاربر اکنون عضو گروه است", message_id=msg.get("message_id"))

							except IndexError:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
							
							except:
								bot.sendMessage(target, "❌ دستور اشتباه", message_id=msg.get("message_id"))
								
						elif msg.get("text") == "دستورات":
							try:
								rules = open("help.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text").startswith("آپدیت دستورات") and msg.get("author_object_guid") in admins:
							try:
								rules = open("help.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت قوانین")))
								bot.sendMessage(target, "دستو‌رات ربا‌ت به‌روزرسانی شد!", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "مشکلی پیش اومد مجددا تلاش کنید!", message_id=msg.get("message_id"))
								
						elif msg.get("text").startswith("زمان"):
							try:
								response = get("https://api.codebazan.ir/time-date/?td=all").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								print("err answer time")
								
						elif msg.get("text") == "ساعت":
							try:
								bot.sendMessage(target, f"Time : {time.localtime().tm_hour} : {time.localtime().tm_min} : {time.localtime().tm_sec}", message_id=msg.get("message_id"))
							except:
								print("err time answer")
						
						elif msg.get("text") == "!date":
							try:
								bot.sendMessage(target, f"Date: {time.localtime().tm_year} / {time.localtime().tm_mon} / {time.localtime().tm_mday}", message_id=msg.get("message_id"))
							except:
								print("err date")
								
						elif msg.get("text") == "پاک" and msg.get("author_object_guid") in admins :
							try:
								bot.deleteMessages(target, [msg.get("reply_to_message_id")])
								bot.sendMessage(target, "پیام مورد نظر پاک شد...", message_id=msg.get("message_id"))
							except:
								print("err pak")
								
						elif msg.get("text").startswith("!cal") or msg.get("text").startswith("حساب"):
							msd = msg.get("text")
							if plus == True:
								try:
									call = [msd.split(" ")[1], msd.split(" ")[2], msd.split(" ")[3]]
									if call[1] == "+":
										try:
											am = float(call[0]) + float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
											plus = False
										except:
											print("err answer +")
										
									elif call[1] == "-":
										try:
											am = float(call[0]) - float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer -")
										
									elif call[1] == "*":
										try:
											am = float(call[0]) * float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer *")
										
									elif call[1] == "/":
										try:
											am = float(call[0]) / float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer /")
											
								except IndexError:
									bot.sendMessage(target, "متاسفانه دستور شما اشتباه میباشد!" ,message_id=msg.get("message_id"))
									plus= True
						
						elif hasInsult(msg.get("text"))[0] and not msg.get("author_object_guid") in admins :
							try:
								print("yek ahmagh fohsh dad")
								bot.deleteMessages(target, [str(msg.get("message_id"))])
								print("fohsh pak shod")
							except:
								print("err del fohsh Bug")
								
						elif msg.get("text").startswith("سلام") or msg.get("text").startswith("سلم") or msg.get("text").startswith("صلام") or msg.get("text").startswith("صلم") or msg.get("text").startswith("hi") or msg.get("text").startswith("Hi") or msg.get("text").startswith("Hello") or msg.get("text").startswith("hello"):
							try:
								bot.sendMessage(target, "هــای😍🌹", message_id=msg.get("message_id"))
							except:
								print("err answer hello")
								
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
								
					elif msg.get("text").startswith("خوبی") or msg.get("text").startswith("خبی"):
							try:
								bot.sendMessage(target, "تو چطوری؟🤪", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
					elif msg.get("text").startswith("چه خبر") or msg.get("text").startswith("چخبر"):
							try:
								bot.sendMessage(target, "ســلامـتیت😍♥", message_id=msg.get("message_id"))
							except:
								print("err CheKhabar")
								
					elif msg.get("text").startswith("ربات") or msg.get("text").startswith("بات"):
							try:
								bot.sendMessage(target, "جــونـم😁💋", message_id=msg.get("message_id"))
							except:
								print("err bot answer")
								
					elif msg.get("text").startswith("😂") or msg.get("text").startswith("🤣"):
							try:
								bot.sendMessage(target, "جــون تـو فــقط بخـند😍", message_id=msg.get("message_id"))
							except:
								print("err luagh")
								
					elif msg.get("text") == "😐":
							try:
								bot.sendMessage(target, "😑😐", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
					elif msg.get("text").startswith("!trans"):
							try:
								responser = get(f"https://api.codebazan.ir/translate/?type=json&from=en&to=fa&text={msg.get('text').split()[1:]}").json()
								al = [responser["result"]]
								bot.sendMessage(msg.get("author_object_guid"), "پاسخ به ترجمه:\n"+"".join(al)).text
								bot.sendMessage(target, "نتیجه رو برات ارسال کردم😘", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
								
					elif msg.get("text").startswith("!font"):
							try:
								response = get(f"https://api.codebazan.ir/font/?text={msg.get('text').split()[1]}").json()
								bot.sendMessage(msg.get("author_object_guid"), "\n".join(list(response["result"].values())[:110])).text
								bot.sendMessage(target, "نتیجه رو برات ارسال کردم😘", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
						
					elif msg.get("text").startswith("جوک") or msg.get("text").startswith("jok") or msg.get("text").startswith("!jok"):
							try:
								response = get("https://api.codebazan.ir/jok/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("ذکر") or msg.get("text").startswith("zekr") or msg.get("text").startswith("!zekr"):
							try:
								response = get("http://api.codebazan.ir/zekr/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ببخشید، خطایی پیش اومد!", message_id=msg["message_id"])
								
					elif msg.get("text").startswith("حدیث") or msg.get("text").startswith("hadis") or msg.get("text").startswith("!hadis"):
							try:
								response = get("http://api.codebazan.ir/hadis/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ببخشید، خطایی تو ارسال پیش اومد!", message_id=msg["message_id"])
								
					elif msg.get("text").startswith("بیو") or msg.get("text").startswith("bio") or msg.get("text").startswith("!bio"):
							try:
								response = get("https://api.codebazan.ir/bio/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ببخشید، خطایی تو ارسال پیش اومد!", message_id=msg["message_id"])
								
					elif msg["text"].startswith("!weather"):
							try:
								response = get(f"https://api.codebazan.ir/weather/?city={msg['text'].split()[1]}").json()
								bot.sendMessage(msg["author_object_guid"], "\n".join(list(response["result"].values())[:20])).text
								bot.sendMessage(target, "نتیجه بزودی برای شما ارسال خواهد شد...", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "متاسفانه نتیجه‌ای موجود نبود!", message_id=msg["message_id"])
								
					elif msg.get("text").startswith("دیالوگ"):
							try:
								response = get("http://api.codebazan.ir/dialog/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "متاسفانه تو ارسال مشکلی پیش اومد!", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("دانستنی"):
							try:
								response = get("http://api.codebazan.ir/danestani/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
								
					elif msg.get("text").startswith("پ ن پ") or msg.get("text").startswith("!pa-na-pa") or msg.get("text").startswith("په نه په"):
							try:
								response = get("http://api.codebazan.ir/jok/pa-na-pa/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "شرمنده نتونستم بفرستم!", message_id=msg["message_id"])
								
					elif msg.get("text").startswith("الکی مثلا") or msg.get("text").startswith("!alaki-masalan"):
							try:
								response = get("http://api.codebazan.ir/jok/alaki-masalan/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "نشد بفرستم:(", message_id=msg["message_id"])
								
					elif msg.get("text").startswith("داستان") or msg.get("text").startswith("!dastan"):
							try:
								response = get("http://api.codebazan.ir/dastan/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "مشکلی پیش اومد!", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("!ping"):
							try:
								responser = get(f"https://api.codebazan.ir/ping/?url={msg.get('text').split()[1]}").text
								bot.sendMessage(target, responser,message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
								
					elif "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
							try:
								print("Yek ahmagh forwared Zad")
								bot.deleteMessages(target, [str(msg.get("message_id"))])
								print("tabligh forearedi pak shod")
							except:
								print("err delete forwared")
						
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
							
				       elif msg.get("text").startswith("همسر"):
						
						try:
							response = get("https://api.codebazan.ir/name/?type=json").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("فونت"):
						#print("\n".join(list(response["result"].values())))
						try:
							response = get(f"https://api.codebazan.ir/font/?text={msg.get('text').split()[1]}").json()
							bot.sendMessage(msg.get("author_object_guid"), "\n".join(list(response["result"].values())[:110])).text
							bot.sendMessage(target, "نتیجه رو برات ارسال کردم😘", message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])	
						
						elif msg.get("text") == "قوانین":
							try:
								rules = open("rules.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err ghanon")
							
						elif msg.get("text").startswith("آپدیت قوانین") and msg.get("author_object_guid") in admins:
							try:
								rules = open("rules.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت قوانین")))
								bot.sendMessage(target, "✅  قوانین بروزرسانی شد", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))

						elif msg.get("text") == "حالت آرام" and msg.get("author_object_guid") in admins:
							try:
								number = 10
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام برای "+str(number)+"ثانیه فعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
						elif msg.get("text") == "!speak" or msg.get("text") == "speak" or msg.get("text") == "Speak" or msg.get("text") == "بگو":
							try:
								if msg.get('reply_to_message_id') != None:
									msg_reply_info = bot.getMessagesInfo(target, [msg.get('reply_to_message_id')])[0]
									if msg_reply_info['text'] != None:
										text = msg_reply_info['text']
										speech = gTTS(text)
										changed_voice = io.BytesIO()
										speech.write_to_fp(changed_voice)
										b2 = changed_voice.getvalue()
										changed_voice.seek(0)
										audio = MP3(changed_voice)
										dur = audio.info.length
										dur = dur * 1000
										f = open('sound.ogg','wb')
										f.write(b2)
										f.close()
										bot.sendVoice(target , 'sound.ogg', dur,message_id=msg["message_id"])
										os.remove('sound.ogg')
										print('sended voice')
								else:
									bot.sendMessage(target, 'پیام شما متن یا کپشن ندارد',message_id=msg["message_id"])
							except:
								print('server gtts bug')
							
						elif msg.get("text") == "برداشتن حالت آرام" and msg.get("author_object_guid") in admins:
							try:
								number = 0
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام غیرفعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "لطفا دستور رو صحیح وارد کنید!", message_id=msg.get("message_id"))


						elif msg.get("text").startswith("اخطار") and msg.get("author_object_guid") in admins:
							try:
								user = msg.get("text").split(" ")[1][1:]
								guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									alert(guid,user)
									
								else :
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", message_id=msg.get("message_id"))
									
							except IndexError:
								guid = bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"]
								user = bot.getUserInfo(guid)["data"]["user"]["username"]
								if not guid in admins:
									alert(guid,user)
								else:
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))



						elif msg.get("text") == "قفل گروه" and msg.get("author_object_guid") in admins :
							try:
								bot.setMembersAccess(target, ["AddMember"])
								bot.sendMessage(target, "🔒 گروه قفل شد", message_id=msg.get("message_id"))
							except:
								print("err lock GP")

						elif msg.get("text") == "بازکردن گروه" or msg.get("text") == "باز کردن گروه" and msg.get("author_object_guid") in admins :
							try:
								bot.setMembersAccess(target, ["SendMessages","AddMember"])
								bot.sendMessage(target, "🔓 گروه اکنون باز است", message_id=msg.get("message_id"))
							except:
								print("err unlock GP")

					else:
						if msg.get("text") == "!start" or msg.get("text") == "/start" and msg.get("author_object_guid") in admins :
							try:
								sleeped = False
								bot.sendMessage(target, "ربا‌ت با موفقیت روشن شد!", message_id=msg.get("message_id"))
							except:
								print("err on bot")
								
				elif msg["type"]=="Event" and not msg.get("message_id") in answered and not sleeped:
					name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
					data = msg['event_data']
					if data["type"]=="RemoveGroupMembers":
						try:
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"‼️ کاربر {user} با موفقیت از گروه حذف شد .", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err rm member answer")
					
					elif data["type"]=="AddedGroupMembers":
						try:
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"هــای {user} عزیز 😘🌹 \n • به گـروه {name} خیـلی خوش اومدی 😍❤️ \nلطفا قوانین رو رعایت کن .\n 💎 برای مشاهده قوانین کافیه کلمه (قوانین) رو ارسال کنی!\nدوست داری ربات بسازی؟ بیا اینجا😍👇\n@RobotHL", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err add member answer")
					
					elif data["type"]=="LeaveGroup":
						try:
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"مراقبت کن😈😘 {user} 👋 ", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err Leave member Answer")
							
					elif data["type"]=="JoinedGroupByLink":
						try:
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"هــای {user} عزیز 😘🌹 \n • به گـروه {name} خیـلی خوش اومدی 😍❤️ \nلطفا قوانین رو رعایت کن .\n 💎 برای مشاهده قوانین کافیه کلمه (قوانین) رو ارسال کنی!\nدوست داری ربات بسازی؟ بیا اینجا😍👇\n@RobotHL", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err Joined member Answer")
							
				else:
					if "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [msg.get("message_id")])
						guid = msg.get("author_object_guid")
						user = bot.getUserInfo(guid)["data"]["user"]["username"]
						bot.deleteMessages(target, [msg.get("message_id")])
						alert(guid,user,True)
					
					continue
			except:
				continue

			answered.append(msg.get("message_id"))
			print("[" + msg.get("message_id")+ "] >>> " + msg.get("text") + "\n")

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
