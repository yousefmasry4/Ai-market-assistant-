import 'dart:convert';
import 'dart:core';
import 'package:http/http.dart' as http;





class Controller {
  static String ip="";
  var prev=null;
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
      "https://68a5a708ed82.ngrok.io/get",
      body:{
        'msg': msg,
        "prev":prev == null?'{"id":"","with":""}':jsonEncode(prev)
      }
    );
    print(req.body);
    print(req.statusCode);
    Map<String, dynamic> body =await jsonDecode(req.body);
    prev =await body["prev"];
    print(body);
    return data(prev, body["msg"], body["list"],body["t_list"]);
  }
}


class data {
  final Map<String, dynamic>  ref;
  String answer="";
  final List items;
  final String t_list;

  data(this.ref, this.answer, this.items, this.t_list);
}
class Ip{
  get() async{
    await Controller.get_ip();
  }
}
Controller bot = Controller();
