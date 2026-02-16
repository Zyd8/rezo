import 'package:flutter/material.dart';
import 'package:record/record.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as path; 
import 'package:audioplayers/audioplayers.dart';


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Rezo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.red),
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  bool _isRecording = false;

  final AudioRecorder _record = AudioRecorder();
  final AudioPlayer _player = AudioPlayer();
  String _filePath = '';

  Future<void> _toggleRecording() async {
    if (_isRecording) {
      final path = await _record.stop();
      if (mounted) setState(() => _isRecording = false);
      _filePath = path ?? '';
      return;
    }

    final hasPermission = await _record.hasPermission();
    if (!hasPermission) {
      return;
    }

    final dir = await getTemporaryDirectory();
    final filePath = '${dir.path}/recording_${DateTime.now().millisecondsSinceEpoch}.m4a';

    await _record.start(const RecordConfig(), path: filePath);

    if (mounted) setState(() => _isRecording = true);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Rezo'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Hello'),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _toggleRecording,
              child: Text(_isRecording ? 'Stop Recording' : 'Record'),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => _player.play(DeviceFileSource(_filePath)),
              child: Text('Play Recording'),
            ),
          ],
        ),
      ),
    );
  }
}
