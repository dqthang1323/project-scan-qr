
# from imutils.video import VideoStream
# from pyzbar import pyzbar
# import argparse
# import datetime
# import imutils
# import time
# import cv2
# import webbrowser
# ap = argparse.ArgumentParser()

# # 
# def decode():
#       #Uncomment this if you are using Webcam
# #vs = VideoStream(usePiCamera=True).start() # For Pi Camera
#     encoding = 'utf-8'
#     vs = VideoStream(src=0).start()
#     frame = vs.read()
#     # frame = imutils.resize(frame)
#     barcodes = pyzbar.decode(frame)
#     for barcode in barcodes:
#         (x, y, w, h) = barcode.rect
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
#         barcodeData = barcode.data.decode("utf-8")
#         url = str(barcodes[0].data, encoding=encoding)
#         barcodeType = barcode.type
#         text = "{} ({})".format(barcodeData, barcodeType)
#         print (text)
#         cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
#         if barcodeType == 'EAN13':

#             webbrowser.open("https://www.barcodelookup.com/"+barcodeData)
#             # time.sleep(2)
#         elif barcodeType == "QRCODE":
#             webbrowser.open(url)
#             # time.sleep(2)
#     cv2.imshow("Barcode Reader", frame)
#     key = cv2.waitKey(1) & 0xFF

#     if key == ord("s"):
#         pass
#     print("[INFO] cleaning up...")

#     cv2.destroyAllWindows()
#     vs.stop()





from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import webbrowser
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())
def decode(vs):
    # vs = VideoStream(src=0).start()  #Uncomment this if you are using Webcam
#vs = VideoStream(usePiCamera=True).start() # For Pi Camera

    encoding = 'utf-8'
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            url = str(barcodes[0].data, encoding=encoding)
            barcodeType = barcode.type
            text = "{} ({})".format(barcodeData, barcodeType)
            print (text)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            if barcodeType == 'EAN13':

                webbrowser.open("https://www.barcodelookup.com/"+barcodeData)
                time.sleep(2)
            elif barcodeType == "QRCODE":
                webbrowser.open(url)
                time.sleep(2)
        cv2.imshow("Barcode Reader", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            break
    print("[INFO] cleaning up...")

    cv2.destroyAllWindows()
    vs.stop()
