class Controller {
  Future<data> request(String) async{
    return data("", "No",[]);
  }
}

class Item {
  final String id, name, price, img;
  Item(this.id, this.img, this.name, this.price);
}

class data {
  final String ref;
  final String answer;
  final List<Item> items ;

  data(this.ref, this.answer , this.items);
}

Controller bot = Controller();
