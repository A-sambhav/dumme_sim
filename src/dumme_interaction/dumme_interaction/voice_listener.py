#!/usr/bin/env python3
"""Offline keyword listener: hears Dumm-E's voice commands on the microphone.

Audio comes from `arecord` (ALSA, so no PortAudio needed) and is recognised by
Vosk with a tiny grammar, so it only ever matches these words (anything else
becomes [unk]) and runs fine on a laptop CPU.

Publishes /voice/command (std_msgs/String), one command per utterance:
  "release"  <- "release" / "stop recording"
  "record"   <- "(hey dummy) start recording" / "record"
  "hi"       <- "hi" / "hello" / "hey"           } both can come from one utterance,
  "dumme"    <- "dummy"                            } e.g. "hey dummy"
Recording commands win over greetings, so "hey dummy start recording" only
records instead of also waving and tracking.

Test without a mic:
  ros2 topic pub --once /voice/command std_msgs/msg/String "{data: dumme}"
"""
import json
import subprocess
import threading
import time

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String
import vosk

RATE = 16000
CHUNK = 4000  # bytes = 125 ms of 16-bit mono

# spoken word -> command. "Dumm-E" isn't an English word; Vosk hears it as "dummy".
WORDS = {
    "hi": "hi",
    "hello": "hi",
    "hey": "hi",
    "dummy": "dumme",
    "dumb": "dumme",
    "record": "record",
    "recording": "record",
    "release": "release",
    "start": None,  # recognised so "start recording" isn't [unk] noise
    "stop": None,   # "stop recording" -> release
}


class VoiceListener(Node):
    def __init__(self):
        super().__init__("voice_listener")
        self.declare_parameter("model_path", "")
        self.declare_parameter("device", "default")  # arecord -D device
        self.declare_parameter("min_conf", 0.9)  # real keywords score ~1.0; chatter ~0.8
        self.declare_parameter("cooldown", 2.0)  # s between repeats of the same command

        p = lambda n: self.get_parameter(n).value  # noqa: E731
        if not p("model_path"):
            raise RuntimeError("parameter 'model_path' is required")
        self.min_conf = float(p("min_conf"))
        self.cooldown = float(p("cooldown"))
        self.last = {}

        vosk.SetLogLevel(-1)
        grammar = json.dumps(sorted(WORDS) + ["[unk]"])
        self.rec = vosk.KaldiRecognizer(vosk.Model(p("model_path")), RATE, grammar)
        self.rec.SetWords(True)

        self.pub = self.create_publisher(String, "/voice/command", 10)
        self.proc = subprocess.Popen(
            ["arecord", "-q", "-D", p("device"), "-f", "S16_LE", "-r", str(RATE),
             "-c", "1", "-t", "raw"],
            stdout=subprocess.PIPE,
        )
        self.running = True
        self.thread = threading.Thread(target=self.listen, daemon=True)
        self.thread.start()
        self.get_logger().info(f"Listening on '{p('device')}' for: {', '.join(sorted(WORDS))}")

    def listen(self):
        while self.running:
            data = self.proc.stdout.read(CHUNK)
            if not data:
                self.get_logger().error("microphone stream ended (is arecord working?)")
                return
            if self.rec.AcceptWaveform(data):
                self.on_result(json.loads(self.rec.Result()))

    @staticmethod
    def commands(words):
        """Confident words of one utterance -> commands, in order."""
        cmds = {WORDS[w] for w in words if WORDS.get(w)}
        if "release" in cmds or ("stop" in words and "record" in cmds):
            return ["release"]
        if "record" in cmds:
            return ["record"]
        return [c for c in ("hi", "dumme") if c in cmds]

    def on_result(self, result):
        words = [w["word"] for w in result.get("result", []) if w["conf"] >= self.min_conf]
        now = time.monotonic()
        for cmd in self.commands(words):
            if now - self.last.get(cmd, -1e9) < self.cooldown:
                continue
            self.last[cmd] = now
            self.get_logger().info(f'heard "{" ".join(words)}" -> {cmd}')
            self.pub.publish(String(data=cmd))

    def destroy_node(self):
        self.running = False
        self.proc.terminate()
        super().destroy_node()


def main():
    rclpy.init()
    node = VoiceListener()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
