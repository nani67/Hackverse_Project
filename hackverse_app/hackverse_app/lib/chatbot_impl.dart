import 'dart:async';
import 'dart:convert';
import 'dart:math' as Math;
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';

import 'schema.dart';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(ChatbotPage());

class ChatbotPage extends StatelessWidget {
  final FirebaseUser firebaseUser;
  ChatbotPage({Key key, this.firebaseUser}) : super(key: key);

  Widget build(context) {
    return MaterialApp(
      title: "Chatbot Implementation",
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.amber,
      ),
      home: ChatBotStateful(firebaseUser: firebaseUser,),
    );
  }
}

class ChatBotStateful extends StatefulWidget {
  final FirebaseUser firebaseUser;
  ChatBotStateful({Key key, this.firebaseUser}) : super(key: key);
  State<ChatBotStateful> createState() => new ChatbotState();
}

class ChatbotState extends State<ChatBotStateful> {


  TextEditingController userText = new TextEditingController();
  List<Widget> getAllTypedInfo = new List<Widget>();

  Widget getPositionOfObject;

  void initState() {
    getPositionOfObject = Center(
      child: Text("Select the options below"),
    );

    super.initState();


    getDocsCaps().then((onValue) { print("Done with getting"); print(collegeName); });
  }
  
  String collegeName;
  String section;
  String depart;
  
  Future<void> getDocsCaps() async{
    await Firestore.instance.collection("UsersInfo").document(widget.firebaseUser.uid).collection("personalInfo").document("SampleDoesTheThing").get().then((value) {
      collegeName = value.data["collegeName"];
      depart = value.data["department"];
      section = value.data["section"];
    });
  }

  Widget build(context) {



    return Scaffold(
    resizeToAvoidBottomPadding: false,
      resizeToAvoidBottomInset: false,
      bottomNavigationBar: BottomAppBar(
        color: Colors.white,
        child: new Row(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: <Widget>[
            IconButton(icon: Icon(Icons.menu), onPressed: () {
              getPositionOfObject = menuPage(context);
              setState(() {

              });

            },),
            IconButton(icon: Icon(Icons.chat), onPressed: () {
              getPositionOfObject = getTheChatbotOnes(context);
              setState(() {

              });
            },),
            IconButton(icon: Icon(Icons.home), onPressed: () {

              getPositionOfObject = getHomePage(context);
              setState(() {

              });

            },),
            IconButton(icon: Icon(Icons.history), onPressed: () {
              getPositionOfObject = historyOfPreviousCounsellings(context);
              setState(() {

              });
            },),
            IconButton(icon: Icon(Icons.notifications), onPressed: () {
              getPositionOfObject = remindersForStudents(context);
              setState(() {

              });
            },),
          ],
        ),
      ),

      appBar: AppBar(
        title: Text("Blue Flags"),
        centerTitle: true,
      ),
      body: getPositionOfObject,
    );
  }

  String reminderOne = "";

  Widget getTheChatbotOnes(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.max,
      mainAxisAlignment: MainAxisAlignment.end,
      children: <Widget>[

        Container(
          width: MediaQuery
              .of(context)
              .size
              .width,
          height: MediaQuery
              .of(context)
              .size
              .height - 200,
          child:
          SingleChildScrollView(
            reverse: true,
            child:
            Column(
              verticalDirection: VerticalDirection.down,
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: getAllTypedInfo,
            ),
          ),
        ),

        Row(
          children: <Widget>[
            Container(
              width: MediaQuery
                  .of(context)
                  .size
                  .width - 60,
              child: TextField(
                controller: userText,
              ),
            ),

            FloatingActionButton(
              onPressed: () {



                getAllTypedInfo.add(
                    Container(
                      alignment: FractionalOffset.bottomRight,
                      padding: EdgeInsets.all(4.0),
                      child:
                      Card(
                        elevation: 4.0,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.all(Radius.circular(32.0))),
                        child: Padding(
                          padding: EdgeInsets.all(16.0),
                          child: Text(userText.text),
                        ),
                      ),
                    )
                );

                setState(() {

                });


                sendTextToDialogflow(userText.text).whenComplete(() {
                    userText.text = "";

                    setState(() {
                      getPositionOfObject = getTheChatbotOnes(context);
                    });
                });


              },
              child: Icon(Icons.send),
            )
          ],
        )


      ],
    );
  }

  int _rating = 0;
  String userName = "";

  Widget getHomePage(BuildContext context) {

    userName = widget.firebaseUser.displayName;

    return new Container(
      width: MediaQuery.of(context).size.width,
      height: MediaQuery.of(context).size.height,
      child: SingleChildScrollView(
        child: Column(
          children: <Widget>[

            Padding(
              padding: EdgeInsets.all(16.0),
              child:
              Text(
                "Hi "+userName,
                style: TextStyle(
                  fontSize: 24,
                ),
              ),
            ),



            Container(
              width: MediaQuery.of(context).size.width,
              child: Padding(
                padding: EdgeInsets.all(16.0),
                child: Card(
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.all(Radius.circular(16.0))),
                  child: Column(
                    children: <Widget>[
                      Padding(
                        padding: EdgeInsets.all(16.0),
                        child:
                        Text(
                          "What's my reminders?",
                          style: TextStyle(
                            fontSize: 24,
                          ),
                        ),
                      ),
                      Padding(
                        padding: EdgeInsets.all(16.0),
                        child:
                        Text(
                          reminderOne,
                        ),
                      ),


                      Padding(
                        padding: EdgeInsets.all(16.0),
                        child: RaisedButton(
                          child: Text("Show me more!"),
                          onPressed: () {
                            getPositionOfObject = remindersForStudents(context);
                            setState(() {

                            });
                          },
                        ),
                      ),

                    ],
                  ),
                ),
              ),
            ),


            Container(
              width: MediaQuery.of(context).size.width,
              child: Padding(
                padding: EdgeInsets.all(16.0),
                child: Card(
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.all(Radius.circular(16.0))),
                  child: Column(
                    children: <Widget>[

                      Padding(
                        padding: EdgeInsets.all(16.0),
                        child: Text("How's your mood?", style: TextStyle(fontSize: 24),),
                      ),

                      Padding(
                        padding: EdgeInsets.all(16.0),
                        child:
                        Column(
                          children: <Widget>[

                            Center(
                                child:
                                Row(
                                  mainAxisSize: MainAxisSize.max,
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: getStarButtons(),
                                ),
                            ),

                          ],
                        ),
                      ),

                    ],
                  ),
                ),
              ),
            ),



            Container(
              width: MediaQuery.of(context).size.width,
              child: Padding(
                padding: EdgeInsets.all(16.0),
                child: Card(
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.all(Radius.circular(16.0))),
                  child: Column(
                    children: <Widget>[

                      Padding(
                        padding: EdgeInsets.all(16.0),
                        child: Text("Today's Quote", style: TextStyle(
                          fontSize: 24,
                        ),),
                      ),


                      Padding(
                        padding: EdgeInsets.all(16.0),
                        child: Text(
                          "Do something than nothing. Sleeping is also a work.",
                          style: TextStyle(
                              fontStyle: FontStyle.italic,
                              fontSize: 16,

                          ),
                          textAlign: TextAlign.center,
                        ),
                      )





                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );

  }

  List<Widget> getStarButtons() {
    List<Widget> stars = [];

    for(int i=1; i<=5; i++) {
      Widget star = IconButton(
        icon: Icon(
          _rating >= i ? Icons.star : Icons.star_border,
          size: 35,
          color: Colors.blue,
        ),
        onPressed: () {
          _rating = i;
          setState(() {
              getPositionOfObject = getHomePage(context);
          });
        },
      );
      stars.add(star);
    }
    return stars;
  }

  Widget historyOfPreviousCounsellings(BuildContext context) {


    return StreamBuilder<QuerySnapshot>(
      stream: Firestore.instance.collection('UsersInfo').document('9zm0xm3mCyMAeGXTyEos0akWMhC2').collection('counsellingHistory').snapshots(),
      builder: (BuildContext context, AsyncSnapshot<QuerySnapshot> snapshot) {
        if (snapshot.hasError)
          return new Text('Error: ${snapshot.error}');
        switch (snapshot.connectionState) {
          case ConnectionState.waiting: return new Text('Loading...');
          default:
            return new ListView(

              children: snapshot.data.documents.map((DocumentSnapshot document) {
                return new ListTile(
                  title: new Text(document['dateOfCounselling']),
                  subtitle: new Text(document['counsellorName']),
                );
              }).toList(),
            );
        }
      },
    );


  }

  Widget remindersForStudents(BuildContext context) {


    return StreamBuilder<QuerySnapshot>(
      stream: Firestore.instance.collection('TeachersAssignmentsList').where("UniversityName",isEqualTo: collegeName).where("UniversityClass", isEqualTo: depart).where("section", isEqualTo: section).snapshots(),
      builder: (BuildContext context, AsyncSnapshot<QuerySnapshot> snapshot) {
        if (snapshot.hasError)
          return new Text('Error: ${snapshot.error}');
        switch (snapshot.connectionState) {
          case ConnectionState.waiting: return new Text('Loading...');
          default:
            return new ListView(
              children: snapshot.data.documents.map((DocumentSnapshot document) {
                reminderOne = document['reminder'];
                return new ListTile(
                  title: new Text(document['reminder']),
                );
              }).toList(),
            );
        }
      },
    );


  }

  Future<void> sendTextToDialogflow(String requestString) async {



    Map<String, String> headers = {
      "Content-Type": "application/json",
      "Authorization": "Bearer ff014da917154815b27d4680180576b2",
    };

    var message = jsonEncode({
        "lang": "en",
        "query": requestString,
        "sessionId": "12345",
    });

    var url = 'https://api.dialogflow.com/v1/query?v=20150910';
    await http.post(url,
        headers: headers,
        body: message,
      ).then((value) {
        var decodedJson = json.decode(value.body);
        var responseParsed = Schema.fromMap(decodedJson);

        getAllTypedInfo.add(
            Container(
              padding: EdgeInsets.all(4.0),
              alignment: FractionalOffset.bottomLeft,
              child:
              Card(
                color: Colors.amber,
                elevation: 4.0,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.all(Radius.circular(32.0))),
                child: Padding(
                  padding: EdgeInsets.all(16.0),
                  child: Text(responseParsed.result.fulfillment.speech),
                ),
              ),
            )
        );

    });


  }

  var instagramUserName = new TextEditingController();
  var instagramPassword = new TextEditingController();

  Widget menuPage(BuildContext context) {
    return new AlertDialog(
      title: Text("Instagram Credentials (Secured)"),
      content:SingleChildScrollView(
        child:  Column(
          children: <Widget>[

            Padding(
              padding: EdgeInsets.all(4.0),
              child: TextField(
                controller: instagramUserName,
                decoration: InputDecoration(
                    labelText: "Username (or) Email ID"
                ),
              ),
            ),

            Padding(
              padding: EdgeInsets.all(4.0),
              child:
              TextField(
                controller: instagramPassword,
                decoration: InputDecoration(
                  labelText: "Password",
                ),
                obscureText: true,
              ),
            ),


            RaisedButton(
              child: Text("Update"),
              onPressed: () {
                updateValues();
              },
            ),

            RaisedButton(
              child: Text("Cancel"),
              onPressed: () {
                setState(() {
                  getPositionOfObject = getHomePage(context);
                });
              },
            ),

            RaisedButton(
              child: Text("Privacy Policy"),
              onPressed: () {},
            ),


          ],
        ),
      ),
    );
  }

  updateValues() async {
    Map<String, dynamic> data = {"instagramUserId": instagramUserName.text, "instagramPassword": instagramPassword.text};
    Firestore.instance.collection("UsersInfo").document(widget.firebaseUser.uid).collection("instagramCred").add(data);
  }
}