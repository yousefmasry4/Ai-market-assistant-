from flask import Flask, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import en_core_web_sm
import json
from sqlalchemy.ext.indexable import index_property
from db_helper import db
nlp = en_core_web_sm.load()
app = Flask(__name__)
data=db()
english_bot = ChatBot("s", storage_adapter='chatterbot.storage.SQLStorageAdapter',
                      logic_adapters=[
                          {
                              'import_path': 'chatterbot.logic.BestMatch',
                              'default_response': 'I am sorry, but I do not understand.',
                              'maximum_similarity_threshold': 0.30
                          }
                      ],
                      )
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train(
    "chatterbot.corpus.english",
)

# TODO: LOAD ALL PRODUCTS NAME
prod  = db.readitems()

# TODO: LOAD ALL categ NAME
categ = db.readcateg()


@app.route("/get", methods=['POST'])
def get_bot_response():
    userText = request.form.get('msg')
    prev = json.loads(request.form.get('prev'))
    print(request.form)
    answer1 = str(english_bot.get_response(userText))
    if "ORDER" in str(userText).upper() and prev["with"] == "":
        return '''{
                    "prev":{
                            "id":"",
                            "with":"get_id"
                            },
                    "msg":"What is your number" ,"list":[], "t_list":"v"
                    }'''
    elif prev["with"] == "get_id" and prev["id"] == "":
        for i in str(userText).split():
            if i[:3] == "015" or i[:3] == "010" or i[:3] == "011":
                # TODO:  nshof el rakm dah mawgod walla la w n return in the next var : NONE LW MFESH
                data = db.checkid(getid=db.getid(),z=i)

                if ([] == data):
                    # TODO: n3ml save lel id ka new user mn 8er esm kda kda 7ns2lo 3lyh
                    db.adduserid(i)
                    return '''{
                        "prev":{
                            "id":"%s",
                            "with":"get_name_into_id"
                        },
                        "msg":"what is Your name" ,"list":[], "t_list":"v"
                    }''' % (i)
                else:
                    return '''{
                        "prev":{
                            "id":"%s",
                            "with":"ready"
                        },
                        "msg":"what is Your order , %s" ,"list":[], "t_list":"v"
                    }''' % (i, data["name"].split(" ")[0])
    elif prev["with"] == "get_name_into_id" and prev["id"] != "":
        id = prev["id"]
        print(str(userText))
        name = (str(userText).upper()).replace("MY NAME IS", "")
        if name[0] == " ":
            name = name[1:]
        print(name)
        # TODO: save name into id
        db.addusername(id,name)
        return '''{
            "prev":{
                "id":"%s",
                "with":"get_address"
            },
            "msg":"what is Your address , %s" ,"list":[], "t_list":"v"
        }''' % (id, name.split(" ")[0])
    elif prev["with"] == "get_address" and prev["id"] != "":
        id = prev["id"]
        address = (str(userText).upper()).replace("MY ADDRESS IS", "")
        # TODO: save address into id
        db.addaddress(address,id)
        # TODO : get user name
        user_name = db.getusername(id)[0]
        return '''{
                        "prev":{
                            "id":"%s",
                            "with":"ready"
                        },
                        "msg":"what is Your order , %s" ,"list":[], "t_list":"v"
                    }''' % (id, user_name.split(" ")[0])
    elif prev["with"] == "number" or prev["with"] == "not_number":
        p = prev["cash"]
        id = prev["id"]
        if "CANCEL" in str(userText).upper().split():
            return '''{
                                "prev":{
                                    "id":"%s",
                                    "with":"ready"
                                },
                                "msg":"ok no problem"
 ,"list":[], "t_list":"v"
                            }''' % id
        # TODO: get number of items of it
        db.getquantity(x)
        x = 6
        number = [int(i) for i in userText.split() if i.isdigit()][0]
        if number is None:
            return '''{
                                "prev":{
                                    "id":"%s",
                                    "with":"not_number"
                                },
                                "msg":"give me number or say cancel"
 ,"list":[], "t_list":"v"
                            }''' % id
        elif int(number) > x:
            return '''{
                                "prev":{
                                    "id":"%s",
                                    "with":"not_number"
                                },
                                "msg":"i have only %s,So give me another number or say cancel" ,"list":[], "t_list":"v"
                            }''' % (id, str(x))
        else:
            # TODO: deflo p*number fel list bta3to w shel el bda3a ely 5dha
            db.addtolist(x)
            return '''{
                                "prev":{
                                    "id":"%s",
                                    "with":"ready"
                                },
                                "msg":"ok, I added it successfully" ,"list":[], "t_list":"v"
                            }''' % id
    elif prev["with"] == "ready_to_add" and prev["id"] != "":
        # TODO : add x to list
        db.addtolist(x)
        x = prev["cash"]
        id = prev["id"]
        if "NO" in str(userText).upper():
            return '''{
                                "prev":{
                                    "id":"%s",
                                    "with":"ready"
                                },
                                "msg":"ok" ,"list":[], "t_list":"v"
                            }''' % id
        return '''{
                 "prev":{
                       "id":"%s",
                       "with":"number",
                       "cash":%s
                        },
                 "msg":"Ok, how many %s do you need" ,"list":[], "t_list":"v"
                }''' % (id, x, x)
    elif prev["with"] == "ready" and prev["id"] != "":
        id = prev["id"]
        # TODO : get user name
        db.getusername(id)
        user_name = "Yousseff"
        if "NEED" in str(userText).upper() or "ADD" in str(userText).upper():
            x = None
            for i in categ:
                if i in str(userText).upper().split(" "):
                    x = i
                    break
            if x is not None:
                # TODO return all items of category
                db.getallitemsincat(categ)
                itesms = ["a1", "a2", "a3"]
                return '''{
                                "prev":{
                                    "id":"%s",
                                    "with":"ready"
                                },
                                "msg":"%s select item from %s please",
                                "list":%s
                            }''' % (id, user_name.split(" ")[0], x, json.dumps(itesms))
            else:
                for i in prod:
                    if i in str(userText).upper().split(" "):
                        x = i
                        break
                if x is not None:
                    # TODO : add x to list
                    db.addtolist(x)
                    return '''{
                             "prev":{
                                   "id":"%s",
                                   "with":"number",
                                   "cash":%s
                                    },
                             "msg":"Ok %s , how many %s do you need" ,"list":[], "t_list":"v"
                            }''' % (id, x, user_name.split(" ")[0], x[0])
                else:
                    return '''{
                        "prev":{
                            "id":"%s",
                            "with":"ready"
                        },
                        "msg":"sorry %s , We don't have it" ,"list":[], "t_list":"v"
                    }''' % (id, user_name.split(" ")[0])
        elif "REMOVE" in str(userText).upper() or "DELETE" in str(userText).upper():
            x = None
            for i in prod:
                if i in str(userText).upper().split(" "):
                    x = i
                    break
            if x is not None:
                # TODO : remove x from list
                db.removefromlist(x)
                return '''{
                         "prev":{
                               "id":"%s",
                               "with":"ready"
                                },
                         "msg":"Ok" ,"list":[], "t_list":"v"
                        }''' % id
            else:
                return '''{
                    "prev":{
                        "id":"%s",
                        "with":"ready"
                    },
                    "msg":"sorry %s , You don't select it" ,"list":[], "t_list":"v"
                }''' % (id, user_name.split(" ")[0])
        elif "PRICE" in str(userText).upper() or "HOW MUCH" in str(userText).upper():
            x = None
            for i in categ:
                if i in str(userText).upper().split(" "):
                    x = i
                    break
            if x is not None:
                # TODO return all items of category
                db.getallitemsincat(categ)
                itesms = ["a1", "a2", "a3"]
                return '''{
                                "prev":{
                                    "id":"%s",
                                    "with":"ready"
                                },
                                "msg":"%s select item from %s please",
                                "list":%s,
                                "t_list":"h"
                            }''' % (id, user_name.split(" ")[0], x, json.dumps(itesms))
            for i in prod:
                if i in str(userText).upper().split(" "):
                    x = i
                    break
            if x is not None:
                # TODO : GET PRICE OF X
                db.getprice(x)
                price = 500
                return '''{
                         "prev":{
                               "id":"%s",
                               "with":"ready_to_add",
                               "cash":%s
                                },
                         "msg":"%s $,Do you wanna add it" ,"list":[], "t_list":"v"
                        }''' % (id, x, price)
            else:
                return '''{
                    "prev":{
                        "id":"%s",
                        "with":"ready"
                    },
                    "msg":"sorry %s ,We don't have it" ,"list":[], "t_list":"v"
                }''' % (id, user_name.split(" ")[0])
        elif "LIST" in str(userText).upper():
            # TODO:get ist of id
            db.getlistid()
            l = []
            return '''{
                            "prev":{
                                "id":"%s",
                                "with":"ready"
                            },
                            "msg":"Ok %s,If you wanna finish say finish to me ",
                            "list":%s,
                            "t_list":"v"
                        }''' % (id, user_name.split(" ")[0], json.dumps(l))
        elif "WHERE" in str(userText).upper():
            x = None
            for i in categ:
                if i in str(userText).upper().split(" "):
                    x = i
                    break
            if x is not None:
                # TODO return location of category
                db.getlocationofitem(x)
                location=""
                return '''{
                                "prev":{
                                    "id":"%s",
                                    "with":"ready"
                                },
                                "msg":"you can find it in %s" ,"list":[], "t_list":"v"
                            }''' % (id, location)
            else:
                for i in prod:
                    if i in str(userText).upper().split(" "):
                        x = i
                        break
                if x is not None:
                    #TODO :get location of item x
                    db.getlocationofitem(x)
                    location = ""
                    return '''{
                                    "prev":{
                                        "id":"%s",
                                        "with":"ready"
                                    },
                                    "msg":"you can find it in %s" ,"list":[], "t_list":"v"
                                }''' % (id, location)
                else:
                    return '''{
                        "prev":{
                            "id":"%s",
                            "with":"ready"
                        },
                        "msg":"sorry %s , We don't have it"
                        ,"list":[], "t_list":"v"
                    }''' % (id, user_name.split(" ")[0])
        elif "FINISH" in str(userText).upper():
            # TODO: get ist of id
            l = []
            # TODO get courier name and number
            courier = db.getcourier()
            number =db.getcouriernumber(courier)
            return '''{ "prev":{ "id":"%s", "with":"ready" }, "msg":"I Am happy to speak to you %s,your courier will be 
            %s and his number is %s and he'll reach you in 45", "list":%s, "t_list":"v" }''' % (id, user_name.split(" ")[0], courier, number, json.dumps(l))

    return '''{
                    "prev":{
                        "id":"%s",
                        "with":"%s"
                    },
                    "msg":"%s" ,"list":[], "t_list":"v"
                }''' % (prev["id"],prev["with"],answer1)


if __name__ == "__main__":
    app.debug = True
    app.run(ip="192.168.1.4", port=80)
