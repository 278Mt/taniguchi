# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Fri Nov 22 17:28:07 2019

URL: https://github.com/wakame-tech/vendredi-noir/tree/master/src/gesture
@author: n_toba
@id: 4617054
"""
import tensorflow.compat.v1 as tf
import cv2
import pyautogui
import numpy as np



class Gesture(object):


    def __init__(self, builtin: bool=True):

        self.builtin = builtin

        tf.flags.DEFINE_integer('width', 640, 'Screen width')
        tf.flags.DEFINE_integer('height', 480, 'Screen height')
        tf.flags.DEFINE_float  ('threshold', 0.6, 'Threshold for score')
        tf.flags.DEFINE_float  ('alpha', 0.3, 'Transparent level')
        self.FLAGS = tf.flags.FLAGS

        model_path = '../gesture/model.pb'
        self.load_graph(model_path)
        self.capture()


    def load_graph(self, path: str) -> None:

        detection_graph = tf.Graph()

        with detection_graph.as_default():
            graph_def = tf.GraphDef()

            with tf.gfile.GFile(path, 'rb') as fid:
                graph_def.ParseFromString(fid.read())
                tf.import_graph_def(graph_def, name='')

            self.sess = tf.Session(graph=detection_graph)

        self.graph = detection_graph

        return


    def capture(self) -> None:

        FLAGS = self.FLAGS

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FLAGS.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FLAGS.height)
        self.cap = cap

        return


    def detect_hands(self, image: np.ndarray) -> None:

        graph, sess = self.graph, self.sess

        input_image = graph.get_tensor_by_name('image_tensor:0')
        detection_boxes = graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = graph.get_tensor_by_name('detection_scores:0')
        detection_classes = graph.get_tensor_by_name('detection_classes:0')
        image = image[None]
        boxes, scores, classes = sess.run([detection_boxes, detection_scores, detection_classes], feed_dict={input_image: image})

        return np.squeeze(boxes), np.squeeze(scores), np.squeeze(classes)


    def predict(self, boxes: np.ndarray, scores: np.ndarray, classes: np.ndarray, num_hands: int=2) -> list:

        FLAGS = self.FLAGS
        result_li = []

        for box, score, class_ in zip(boxes[:num_hands], scores[:num_hands], classes[:num_hands]):
            if score > FLAGS.threshold:
                y = int(np.mean(box[0::2] * FLAGS.height))
                x = int(np.mean(box[1::2] * FLAGS.width))
                category = int(class_)
                result_li.append([x, y, category])

        return result_li


    def display(self, frame: np.ndarray, x: int, y: int, text: str) -> None:

        GREEN  = (0x00, 0xff, 0x00)
        RED    = (0x00, 0x00, 0xff)
        YELLOW = (0x00, 0xff, 0xff)

        FLAGS = self.FLAGS

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.circle(frame, (x, y), 5, RED, -1)
        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, GREEN, 2)

        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (FLAGS.width, FLAGS.height // 2), YELLOW, -1)
        cv2.addWeighted(overlay, FLAGS.alpha, frame, 1 - FLAGS.alpha, 0, frame)
        cv2.imshow('Detection', frame)

        return


    def main(self, display_mode: bool=False) -> None:

        _x = _y = 0
        eps      = 8
        eps_down = 5
        down_thres = 300

        while cv2.waitKey(10) != ord('q'):

            frame = self.cap.read()[1]
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes, scores, classes = self.detect_hands(frame)
            results = self.predict(boxes, scores, classes)

            if len(results) == 1:
                x, y, category = results[0]
                # category 2 is Closed hand
                if category == 2:
                    text = 'f'
                # elif abs(x-_x) < eps and abs(y-_y) < eps_down:
                #     text = ''
                elif x - _x > eps:
                    text = 'l'
                elif _x - x > eps:
                    text = 'h'
                elif y > down_thres:
                    text = 'k'
                else:
                    continue

                _x, _y = x, y

            else:
                x, y = _x, _y
                continue

            pyautogui.press(text)
            if display_mode:
                self.display(frame, x, y, text)

        return


    def __del__(self):

        if not self.builtin:
            self.cap.release()
            cv2.destroyAllWindows()



if __name__ == '__main__':

    g = Gesture(builtin=False)
    g.main()

