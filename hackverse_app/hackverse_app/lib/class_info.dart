import 'dart:async';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import 'chatbot_impl.dart';

void main() => runApp(ClassData());

class ClassData extends StatelessWidget {
  final FirebaseUser firebaseUser;
  ClassData({Key key, this.firebaseUser}): super(key: key);
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Hackverse Project',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: ClassInfo(title: 'Blue Flags', firebaseUser: firebaseUser,),
    );
  }
}

class ClassInfo extends StatefulWidget {
  ClassInfo({Key key, this.title, this.firebaseUser}) : super(key: key);
  final String title;
  final FirebaseUser firebaseUser;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<ClassInfo> {


  void initState() {
    super.initState();

  }

  var classSectionController = new TextEditingController();
  var mentorNameController = new TextEditingController();
  var collegeNameController = new TextEditingController();
  var sectionController = new TextEditingController();
  var studentNameController = new TextEditingController();
  var idNoController = new TextEditingController();


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      resizeToAvoidBottomPadding: false,
      appBar: AppBar(
        title: Text(widget.title),
        centerTitle: true,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[

            TextField(
              controller: studentNameController,
              decoration: InputDecoration(
                  labelText: "Your name"
              ),
            ),




            TextField(
              controller: idNoController,
              decoration: InputDecoration(
                  labelText: "Your ID"
              ),
            ),






            TextField(
              controller: collegeNameController,
              decoration: InputDecoration(
                  labelText: "College Name"
              ),
            ),


            TextField(
              controller: classSectionController,
              decoration: InputDecoration(
                  labelText: "Department"
              ),
            ),




            TextField(
              controller: sectionController,
              decoration: InputDecoration(
                  labelText: "Section"
              ),
            ),



            TextField(
              controller: mentorNameController,
              decoration: InputDecoration(
                  labelText: "Email of Coordinator"
              ),
            ),


            RaisedButton(
              onPressed: () {
                Map<String, dynamic> data = { "collegeName": collegeNameController.text,
                  "idNumber": idNoController.text,
                  "personName": studentNameController.text,
                  "department": classSectionController.text,
                  "section": sectionController.text,
                  "mentor": mentorNameController.text};
                Firestore.instance.collection('UsersInfo').document(widget.firebaseUser.uid).collection('personalInfo').document('SampleDoesTheThing').setData(data).whenComplete(() {

                  Navigator.of(context).push(MaterialPageRoute(builder: (context) => ChatbotPage(firebaseUser: widget.firebaseUser,)));
                });


              },
              child: Text("Let's go!"),
            )



          ],
        ),
      ),
    );
  }
}
