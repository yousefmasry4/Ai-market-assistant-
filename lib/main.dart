
import 'dart:math';

import 'dart:async';
import 'package:speech_to_text/speech_recognition_error.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:flutter/material.dart';
import 'package:flutter/animation.dart';
void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.pink,
      ),
      home: MyHomePage(title: 'Animate'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}
enum TtsState { playing, stopped, paused, continued }
class _MyHomePageState extends State<MyHomePage> with TickerProviderStateMixin{
  bool _hasSpeech = false;
  FlutterTts flutterTts;
  dynamic languages;
  String language;
  double volume = 2;
  double pitch = 1.3;
  double rate = 1.0;

  String _newVoiceText;

  TtsState ttsState = TtsState.stopped;

  get isPlaying => ttsState == TtsState.playing;

  get isStopped => ttsState == TtsState.stopped;

  get isPaused => ttsState == TtsState.paused;

  get isContinued => ttsState == TtsState.continued;
  String lastWords = "";
  String lastError = "";
  String lastStatus = "";
  final SpeechToText speech = SpeechToText();

  @override
  void initState() {
    super.initState();
    initSpeechState();
    _backgroundController = AnimationController(
      duration: const Duration(seconds: 10),
      vsync: this,
    )..repeat();
    bubbleController = AnimationController(
      duration: const Duration(seconds:20),
      vsync: this,
    );
    backgroundAnimation = CurvedAnimation(parent: _backgroundController, curve: Curves.easeInOut)
      ..addStatusListener((status){
        if(status == AnimationStatus.completed){
          setState(() {

            _backgroundController.forward(from: 0);
          });
        }
        if(status == AnimationStatus.dismissed){
          setState(() {
            _backgroundController.forward(from: 0);
          });
        }
      });

    bubbleController.forward();

    flutterTts = FlutterTts();

    _getLanguages();
    _getEngines();


    flutterTts.setStartHandler(() {
      setState(() {
        print("Playing");
        ttsState = TtsState.playing;
      });
    });

    flutterTts.setCompletionHandler(() {
      setState(() {
        print("Complete");
        ttsState = TtsState.stopped;
      });
    });

    flutterTts.setCancelHandler(() {
      setState(() {
        print("Cancel");
        ttsState = TtsState.stopped;
      });
    });



    flutterTts.setErrorHandler((msg) {
      setState(() {
        print("error: $msg");
        ttsState = TtsState.stopped;
      });
    });

  }

  Future<void> initSpeechState() async {
    bool hasSpeech = await speech.initialize(onError: errorListener, onStatus: statusListener );

    if (!mounted) return;
    setState(() {
      _hasSpeech = hasSpeech;
    });
  }

  //Animation
  Animation<double> backgroundAnimation;
  Animation<double> bubbleAnimation;

  //Animation Controller
  AnimationController bubbleController;
  AnimationController _backgroundController;

  // list of bubble widgets shown on screen
  final bubbleWidgets = List<Widget>();

  // flag to check if the bubbles are already present or not.
  bool areBubblesAdded = false;


  Animatable<Color> backgroundDark = TweenSequence<Color>([
    TweenSequenceItem(
      weight: 0.2,
      tween: ColorTween(
        begin: Colors.black,

      ),
    ),
    TweenSequenceItem(
      weight: 0.2,
      tween: ColorTween(

        end: Colors.black,
      ),
    ),

  ]);
  Animatable<Color> backgroundNormal = TweenSequence<Color>([
    TweenSequenceItem(
      weight:  0.5,
      tween: ColorTween(
        begin: Colors.blue[800],
        end: Colors.black,
      ),
    ),
    TweenSequenceItem(
      weight:  0.5,
      tween: ColorTween(
        begin: Colors.black,
        end: Colors.blue[800],
      ),
    ),
  ]);
  Animatable<Color> backgroundLight = TweenSequence<Color>([
    TweenSequenceItem(
      weight: 0.5,
      tween: ColorTween(
        begin: Colors.blue[800],
        end: Colors.black,
      ),
    ),
    TweenSequenceItem(
      weight: 0.5,
      tween: ColorTween(
        begin: Colors.black,
        end: Colors.blue[800],
      ),
    ),
  ]);

  AlignmentTween alignmentTop = AlignmentTween(begin: Alignment.bottomCenter,end: Alignment.bottomCenter);
  AlignmentTween alignmentBottom = AlignmentTween(begin: Alignment.bottomLeft,end: Alignment.center);

  bool mic =false;


  @override
  Widget build(BuildContext context) {

    // Add below to add bubbles intially.

    return AnimatedBuilder(
      animation: backgroundAnimation,
      builder: (context, child){
        return Scaffold(
          backgroundColor: Colors.black,
          body:  Stack(
            children: <Widget>[
              Container(
                width: MediaQuery.of(context).size.width,
                height: MediaQuery.of(context).size.height/1.2,
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: alignmentTop.evaluate(backgroundAnimation),
                    end: Alignment.topCenter,
                    colors: [
                      backgroundDark.evaluate(backgroundAnimation),
                      backgroundNormal.evaluate(backgroundAnimation),

                    ],
                  ),
                ),
              ),


            ]
                +bubbleWidgets
                +[Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Expanded(
                  child: SizedBox(),
                ),
              Center(
                child: Text(lastWords,style: TextStyle(color: Colors.white,fontSize: 48,fontWeight: FontWeight.w800),),
              ),
              Expanded(
                child: SizedBox(),
              ),
                Center(
                  child:speech.isListening ? Text("I'm listening...",style: TextStyle(color: Colors.white,fontSize: 18,fontWeight: FontWeight.w800)) :
                  Text( 'Not listening' ,style: TextStyle(color: Colors.white,fontSize: 18,fontWeight: FontWeight.w800)),
                ),

                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    InkWell(
                      child: mic && speech.isListening?Image.asset("assets/mic_read.gif",height: 170,width: 170,):
                      Image.asset("assets/mic_on.gif",height: 170,width: 170,),
                      onTap: (){
                        setState(() {
                          mic=!mic;
                          mic?startListening():stopListening();

                        });
                      },
                      focusColor: Colors.black,
                      highlightColor: Colors.black,
                      splashColor: Colors.black,
                    )

                  ],
                )
              ],
            ),],
          ),


        );
      },
    );
  }
  @override

  void dispose() {
    super.dispose();
    bubbleController.dispose();
    _backgroundController.dispose();
    flutterTts.stop();

  }


  void startListening() {
    lastWords = "";
    lastError = "";
    speech.listen(onResult: resultListener );
    setState(() {

    });
  }
  void stopListening() {
    speech.stop( );
    setState(() {
      _speak();
    });
  }
  void cancelListening() {
    speech.cancel( );
    setState(() {

    });
  }
  void resultListener(SpeechRecognitionResult result) {
    setState(() {
      lastWords = "${result.recognizedWords}";
    });
  }
  void errorListener(SpeechRecognitionError error ) {
    setState(() {
      lastError = "${error.errorMsg} - ${error.permanent}";
    });
  }
  void statusListener(String status ) {
    setState(() {
      lastStatus = "$status";
    });
  }

  Future _getLanguages() async {
    languages = await flutterTts.getLanguages;
    if (languages != null) setState(() => languages);
  }
  Future _getEngines() async {
    var engines = await flutterTts.getEngines;
    if (engines != null) {
      for (dynamic engine in engines) {
        print(engine);
      }
    }
  }
  Future _speak() async {
    await flutterTts.setVolume(volume);
    await flutterTts.setSpeechRate(rate);
    await flutterTts.setPitch(pitch);

    if (lastWords != null) {
      if (lastWords.isNotEmpty) {
        var result = await flutterTts.speak(lastWords);
        if (result == 1) setState(() => ttsState = TtsState.playing);
      }
    }
  }
  Future _stop() async {
    var result = await flutterTts.stop();
    if (result == 1) setState(() => ttsState = TtsState.stopped);
  }
  Future _pause() async {
    var result = await flutterTts.pause();
    if (result == 1) setState(() => ttsState = TtsState.paused);
  }
  List<DropdownMenuItem<String>> getLanguageDropDownMenuItems() {
    var items = List<DropdownMenuItem<String>>();
    for (dynamic type in languages) {
      items.add(
          DropdownMenuItem(value: type as String, child: Text(type as String)));
    }
    return items;
  }
  void changedLanguageDropDownItem(String selectedType) {
    setState(() {
      language = selectedType;
      flutterTts.setLanguage(language);
    });
  }
  void _onChange(String text) {
    setState(() {
      _newVoiceText = text;
    });
  }

}





