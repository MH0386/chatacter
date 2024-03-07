import 'dart:convert';

import 'package:animated_text_kit/animated_text_kit.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class Chat extends StatefulWidget {
  const Chat({super.key});
  @override
  State<Chat> createState() => _ChatState();
}

Future<Map<String, dynamic>> getResponse(String query) async {
  final response = await http.post(Uri.parse("https://8000-01hqrk1qr2p3w6cc5np0wk0ys5.cloudspaces.litng.ai/predict?query='$query'"));
  if (response.statusCode == 200) {
    Map<String, dynamic> data = jsonDecode(jsonDecode(response.body));
    return data;
  } else {
    throw Exception('Failed to load data');
  }
}

class _ChatState extends State<Chat> {
  late String _message;
  late String _response = '';
  updateMessage(String value) {
    print('The value is: $value');
    setState(() {
      _message = value;
    });
  }

  submitValue(String value) {
    print('submit: $value');
    getResponse(value).then((response) {
      print(response);
      setState(() {
        _response = response['response'];
        _message = '';
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        elevation: 50,
        leading: IconButton(
          onPressed: () {
            print('Back to home');
            Navigator.pop(context);
          },
          icon: Icon(Icons.arrow_back, color: Theme.of(context).colorScheme.primary),
        ),
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: const Text('Chatting'),
      ),
      body: Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            AnimatedTextKit(
              animatedTexts: [
                TypewriterAnimatedText(
                  'Chatacter Alpha Version\nYou are now chatting with Napoleon\nType your message below and\npress send to get a response\nIt may take time due to server starting\n',
                  textStyle: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 30,
                  ),
                ),
              ],
              isRepeatingAnimation: false,
            ),
            Text(
              _response,
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                fontFamily: 'JetBrainsMono',
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: Padding(
        padding: EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom),
        child: Container(
          margin: const EdgeInsets.all(10),
          child: Row(
            children: [
              Expanded(
                child: TextField(
                  decoration: const InputDecoration(
                    hintText: 'Message...',
                    border: OutlineInputBorder(),
                  ),
                  onChanged: updateMessage,
                ),
              ),
              TextButton(
                onPressed: () => submitValue(_message),
                onHover: (value) {
                  print('Hovering over the button');
                },
                child: const Icon(
                  Icons.send,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
