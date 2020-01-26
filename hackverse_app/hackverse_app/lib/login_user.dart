import 'dart:async';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:hackverse_app/chatbot_impl.dart';

import 'class_info.dart';

void main() => runApp(LoginUserStateless());

class LoginUserStateless extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: new LoginUserStateful(),
    );
  }
}

class LoginUserStateful extends StatefulWidget {
  @override
  State<LoginUserStateful> createState() => new LoginUsersState();
}

class LoginUsersState extends State<LoginUserStateful> {

  String showLoadingAuth = "";

  TextEditingController emailController = new TextEditingController();
  TextEditingController passwordController = new TextEditingController();


  final GoogleSignIn _googleSignIn = GoogleSignIn();
  final FirebaseAuth _auth = FirebaseAuth.instance;


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      resizeToAvoidBottomPadding: false,
      appBar: AppBar(
        centerTitle: true,
        title: Text("Login / Signup"),
      ),
      body: Column(
        children: <Widget>[

          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              Center(
                child:
                Padding(
                  padding: EdgeInsets.all(16.0),
                  child: Text("Login",
                    style: TextStyle(
                      fontSize: 24.0,
                    ),
                  ),
                ),
              ),
            ],
          ),

          Center(
            child: Padding(
              padding: EdgeInsets.all(8.0),
              child:
              MaterialButton(
                color: Colors.yellow,
                onPressed: () {
                  _handleSignIn().then((firebaseUser) {
                    Navigator.of(context).push(MaterialPageRoute(builder: (context) => ClassData(firebaseUser: firebaseUser,)));

                  }).catchError((e) {
                    print(e);
                  });
                },
                child: Text("Login (or) Signup with Google"),
              ),
            ),
          ),


          Padding(
            padding: EdgeInsets.all(16.0),
            child: Text("or"),
          ),


          Padding(
            padding: EdgeInsets.all(16.0),
            child:
            Card(
              child: Column(
                children: <Widget>[
                  Padding(
                    padding: EdgeInsets.all(16.0),
                    child:
                    Text("Email ID", style: TextStyle( fontSize: 16),),
                  ),


                  Padding(
                    padding: EdgeInsets.all(16.0),
                    child:
                    TextField(
                      controller: emailController,
                    ),
                  ),

                  Padding(
                    padding: EdgeInsets.all(16.0),
                    child:
                    Text("Password", style: TextStyle( fontSize: 16),),
                  ),


                  Padding(
                    padding: EdgeInsets.all(16.0),
                    child:
                    TextField(
                      controller: passwordController,
                      obscureText: true,
                    ),
                  ),


                  RaisedButton(
                    child: Text("Sign in / Sign up"),
                    onPressed: () {
                      createAccount().then((firebaseUser) {
                        Navigator.of(context).push(MaterialPageRoute(builder: (context) => ClassData(firebaseUser: firebaseUser,)));
                      }).catchError((e) {print(e);});
                    },
                  )

                ],
              ),
            ),
          ),

        ],
      ),
    );
  }


  Future<FirebaseUser> createAccount() async {

    final AuthResult userLoggingIn = await _auth.signInWithEmailAndPassword(email: emailController.text, password: passwordController.text);
    if(userLoggingIn.user == null) {

      final FirebaseUser user = (await _auth.createUserWithEmailAndPassword(
        email: emailController.text,
        password: passwordController.text,
      )).user;
      return user;
    } else {
      return userLoggingIn.user;
    }
  }

  Future<FirebaseUser> _handleSignIn() async {
    final GoogleSignInAccount googleUser = await _googleSignIn.signIn();
    final GoogleSignInAuthentication googleAuth = await googleUser.authentication;

    final AuthCredential credential = GoogleAuthProvider.getCredential(
      accessToken: googleAuth.accessToken,
      idToken: googleAuth.idToken,
    );

    final FirebaseUser user = (await _auth.signInWithCredential(credential)).user;
    print("signed in " + user.displayName);
    return user;
  }

}