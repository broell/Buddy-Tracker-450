import tensorflow as tf, sys
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib

# change this as you see fit
image_path = "/home/ubuntu/tf_files/pics/current.jpg"

# Read in the image_data
image_data = tf.gfile.FastGFile(image_path, "rb").read()

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line in tf.gfile.GFile("tf_files/retrained_labels.txt")]


def send_email():

    # Prepare actual message
    msg = MIMEMultipart()
    recipients = "brandon.m.roell@gmail.com"
    user = "ChelsEat3r@gmail.com"
    #recipients = ['rcpt1@example.com', 'rcpt2@example.com', 'group1@example.com']
    #emaillist = [elem.strip().split(',') for elem in recipients]
    msg["Subject"] = "Buddy is Waiting Patiently"
    msg["From"] = user

    msg.preamble = "Multipart message.\n"

    part = MIMEText("Butterscotch is ready to come in.")
    msg.attach(part)

    part = MIMEApplication(open(image_path, "rb").read())
    part.add_header("Content-Disposition", "attachment", filename=image_path)
    msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(user, "[]oq*Y<d3c}$S=+6_{,b#'q?&")

        server.sendmail(msg["From"], recipients, msg.as_string())

    except:
        print "failed to send mail"


def evaluate_image():

    # Unpersists graph from file
    with tf.gfile.FastGFile("tf_files/retrained_graph.pb", "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name("final_result:0")

        predictions = sess.run(softmax_tensor, {"DecodeJpeg/contents:0": image_data})

        # Sort to show labels of first prediction in order of confidence
        #top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        #for node_id in top_k:
            #human_string = label_lines[node_id]
            #score = predictions[0][node_id]
        human_string = label_lines[0]
        score = predictions[0][0]
        print("%s (score = %.5f)" % (human_string, score))

            #if human_string == "buddy" and score >= .95:
                #send_email()
