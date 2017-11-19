import cv2
import numpy as np
import sys
import os
import matplotlib
import matplotlib.pyplot as plt
import copy
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.

        self.res = 0.0
        self.score = ''
        self.i = 0
        self.mem = ''
        self.consecutive = 0
        self.sequence = ''
        
        self.video = cv2.VideoCapture(0)
        self.label_lines = [line.rstrip() for line in tf.gfile.GFile("logs/trained_labels.txt")]
        
        with tf.gfile.FastGFile("logs/trained_graph.pb", 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

# If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    def get_tf(self):
        return tf

    def __del__(self):
        self.video.release()
    
    def predict(self,image_data,sess,softmax_tensor):
        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        max_score = 0.0
        res = ''
        for node_id in top_k:
            human_string = self.label_lines[node_id]
            self.score = predictions[0][node_id]
            if self.score > max_score:
                max_score = self.score
                res = human_string
        return res, max_score    
    
    def get_frame(self,sess):
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        ret, img = self.video.read()
        if ret:
            x1, y1, x2, y2 = 100, 100, 300, 300
            img_cropped = img[y1:y2, x1:x2]

            # c += 1
            image_data = cv2.imencode('.jpg', img_cropped)[1].tostring()
            a = cv2.waitKey(33)
            if a == 27:
                return
            if self.i == 4:
                res_tmp, self.score = self.predict(image_data,sess,softmax_tensor)
                self.res = res_tmp
                self.i = 0
                if self.mem == self.res:
                    self.consecutive += 1
                else:
                    self.consecutive = 0
                if self.consecutive == 2 and self.res not in ['nothing']:
                    if self.res == 'space':
                        self.sequence += ' '
                    elif self.res == 'del':
                        self.sequence = self.sequence[:-1]
                    else:
                        self.sequence += self.res
                    self.consecutive = 0
            self.i += 1
            # cv2.putText(img, '%s' % (res.upper()), (100,400), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4)
            # cv2.putText(img, '(score = %.5f)' % (float(score)), (100,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
            # mem = res
            cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
            # cv2.imshow("img", img)
            # img_sequence = np.zeros((200,1200,3), np.uint8)
            # cv2.putText(img_sequence, '%s' % (sequence.upper()), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            # cv2.imshow('sequence', img_sequence)
        else:
            return       
        # return "yes"
        # print(self.score)
        
        ret, jpeg = cv2.imencode('.jpg', img)
        if self.score != '':
            if float(self.score) > 0.70 :
                return jpeg.tobytes() , self.res
            else:
                return jpeg.tobytes() , 'no'
        else:
            return jpeg.tobytes() , 'no'