from flask import Flask, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import en_core_web_sm
import json
from sqlalchemy.ext.indexable import index_property

nlp = en_core_web_sm.load()
app = Flask(__name__)

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
prod = ["AA", "bb", "cc"]

# TODO: LOAD ALL categ NAME
categ = ["A", "b", "c"]


@app.route("/get", methods=['POST'])
def get_bot_response():
    userText = request.form.get('msg')
    prev = json.loads(request.form.get('prev'))
    print(request.form.get('msg'))
    answer1 = str(english_bot.get_response(userText))
    if "ORDER" in str(userText).upper() and prev["with"] == "start":
        return '''{
                    "prev":{
                            "id":"",
                            "with":"get_id"
                            },
                    "msg":"What is your number"
                    }'''
    elif prev["with"] == "get_id" and prev["id"] == "-1":
        for i in str(userText).split():
            if i[:3] == "015" or i[:3] == "010" or i[:3] == "011":
                # TODO:  nshof el rakm dah mawgod walla la w n return in the next var : NONE LW MFESH
                data = None
                if (None == data):
                    # TODO: n3ml save lel id ka new user mn 8er esm kda kda 7ns2lo 3lyh
                    return '''{
                        "prev":{
                            "id":%s,
                            "with":"get_name_into_id"
                        },
                        "msg":"what is Your name"
                    }''' % (i)
                else:
                    return '''{
                        "prev":{
                            "id":%s,
                            "with":"ready"
                        },
                        "msg":"what is Your order , %s"
                    }''' % (i, data["name"].split(" ")[0])
    elif prev["with"] == "get_name_into_id" and prev["id"] != "-1":
        id = prev["id"]
        print(str(userText))
        name = (str(userText).upper()).replace("MY NAME IS", "")
        if name[0] == " ":
            name = name[1:]
        print(name)
        # TODO: save name into id
        return '''{
            "prev":{
                "id":%s,
                "with":"get_address"
            },
            "msg":"what is Your address , %s"
        }''' % (id, name.split(" ")[0])
    elif prev["with"] == "get_address" and prev["id"] != "-1":
        id = prev["id"]
        address = (str(userText).upper()).replace("MY ADDRESS IS", "")
        # TODO: save address into id
        # TODO : get user name
        user_name = "Yousseff"
        return '''{
                        "prev":{
                            "id":%s,
                            "with":"ready"
                        },
                        "msg":"what is Your order , %s"
                    }''' % (id, user_name.split(" ")[0])
    elif prev["with"] == "number" or prev["with"] == "not_number":
        p = prev["cash"]
        id = prev["id"]
        if "CANCEL" in str(userText).upper().split():
            return '''{
                                "prev":{
                                    "id":%s,
                                    "with":"ready"
                                },
                                "msg":"ok no problem"

                            }''' % id
        # TODO: get number of items of it
        x = 6
        number = [int(i) for i in userText.split() if i.isdigit()][0]
        if number is None:
            return '''{
                                "prev":{
                                    "id":%s,
                                    "with":"not_number"
                                },
                                "msg":"give me number or say cancel"

                            }''' % id
        elif int(number) > x:
            return '''{
                                "prev":{
                                    "id":%s,
                                    "with":"not_number"
                                },
                                "msg":"i have only %s,So give me another number or say cancel"
                            }''' % (id, str(x))
        else:
            # TODO: deflo p*number fel list bta3to w shel el bda3a ely 5dha
            return '''{
                                "prev":{
                                    "id":%s,
                                    "with":"ready"
                                },
                                "msg":"ok, I added it successfully"
                            }''' % id
    elif prev["with"] == "ready_to_add" and prev["id"] != "-1":
        # TODO : add x to list
        x = prev["cash"]
        id = prev["id"]
        if "NO" in str(userText).upper():
            return '''{
                                "prev":{
                                    "id":%s,
                                    "with":"ready"
                                },
                                "msg":"ok"
                            }''' % id
        return '''{
                 "prev":{
                       "id":%s,
                       "with":"number",
                       "cash":%s
                        },
                 "msg":"Ok, how many %s do you need"
                }''' % (id, x, x)
    elif prev["with"] == "ready" and prev["id"] != "-1":
        id = prev["id"]
        # TODO : get user name
        user_name = "Yousseff"
        if "NEED" in str(userText).upper() or "ADD" in str(userText).upper():
            x = None
            for i in categ:
                if i in str(userText).upper().split(" "):
                    x = i
                    break
            if x is not None:
                # TODO return all items of category
                itesms = ["a1", "a2", "a3"]
                return '''{
                                "prev":{
                                    "id":%s,
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
                    return '''{
                             "prev":{
                                   "id":%s,
                                   "with":"number",
                                   "cash":%s
                                    },
                             "msg":"Ok %s , how many %s do you need"
                            }''' % (id, x, user_name.split(" ")[0], x[0])
                else:
                    return '''{
                        "prev":{
                            "id":%s,
                            "with":"ready"
                        },
                        "msg":"sorry %s , We don't have it"
                    }''' % (id, user_name.split(" ")[0])
        elif "REMOVE" in str(userText).upper() or "DELETE" in str(userText).upper():
            x = None
            for i in prod:
                if i in str(userText).upper().split(" "):
                    x = i
                    break
            if x is not None:
                # TODO : remove x from list
                return '''{
                         "prev":{
                               "id":%s,
                               "with":"ready"
                                },
                         "msg":"Ok"
                        }''' % id
            else:
                return '''{
                    "prev":{
                        "id":%s,
                        "with":"ready"
                    },
                    "msg":"sorry %s , You don't select it"
                }''' % (id, user_name.split(" ")[0])
        elif "PRICE" in str(userText).upper() or "HOW MUCH" in str(userText).upper():
            x = None
            for i in categ:
                if i in str(userText).upper().split(" "):
                    x = i
                    break
            if x is not None:
                # TODO return all items of category
                itesms = ["a1", "a2", "a3"]
                return '''{
                                "prev":{
                                    "id":%s,
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
                price = 500
                return '''{
                         "prev":{
                               "id":%s,
                               "with":"ready_to_add",
                               "cash":%s
                                },
                         "msg":"%s $,Do you wanna add it"
                        }''' % (id, x, price)
            else:
                return '''{
                    "prev":{
                        "id":%s,
                        "with":"ready"
                    },
                    "msg":"sorry %s ,We don't have it"
                }''' % (id, user_name.split(" ")[0])
        elif "LIST" in str(userText).upper():
            # TODO:get ist of id
            l = []
            return '''{
                            "prev":{
                                "id":%s,
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
                location=""
                return '''{
                                "prev":{
                                    "id":%s,
                                    "with":"ready"
                                },
                                "msg":"you can find it in %s"
                            }''' % (id, location)
            else:
                for i in prod:
                    if i in str(userText).upper().split(" "):
                        x = i
                        break
                if x is not None:
                    #TODO :get location of item x
                    location = ""
                    return '''{
                                    "prev":{
                                        "id":%s,
                                        "with":"ready"
                                    },
                                    "msg":"you can find it in %s"
                                }''' % (id, location)
                else:
                    return '''{
                        "prev":{
                            "id":%s,
                            "with":"ready"
                        },
                        "msg":"sorry %s , We don't have it"
                    }''' % (id, user_name.split(" ")[0])
        elif "FINISH" in str(userText).upper():
            # TODO: get ist of id
            l = []
            # TODO get courier name and number
            courier = ""
            number = ""
            return '''{ "prev":{ "id":%s, "with":"ready" }, "msg":"I Am happy to speak to you %s,your courier will be 
            %s and his number is %s and he'll reach you in 45", "list":%s, "t_list":"v" }''' % (id, user_name.split(" ")[0], courier, number, json.dumps(l))

    return answer1


if __name__ == "__main__":
    app.debug = True
    app.run(ip="192.168.1.4", port=80)
