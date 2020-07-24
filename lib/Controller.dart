import 'dart:convert';
import 'dart:core';
import 'package:http/http.dart' as http;





class Controller {
  static String ip="";

  static Future<void> get_ip() async {
    var data = await http.get(
        'https://raw.githubusercontent.com/yousefmasry4/Ai-market-assistant-/master/ip');
    Controller.ip=data.body;
    print(Controller.ip);
  }

  Future<data> request(String msg) async {
    print(msg);
    print("ip is "+"${Controller.ip.split("%")[0]}/get");
    var req = await http.post(
      "https://c58c7879f366.ngrok.io/get",
      body:{
        'msg': msg,
      }
    );
    print(req.body);
    print(req.statusCode);

    return data("", req.body, []);
  }
}

class Item {
  final String id, name, price, img;
  Item(this.id, this.img, this.name, this.price);
}

class data {
  final String ref;
  final String answer;
  final List<Item> items;

  data(this.ref, this.answer, this.items);
}
class Ip{
  get() async{
    await Controller.get_ip();
  }
}
Controller bot = Controller();
