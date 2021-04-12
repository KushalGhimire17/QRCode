from django.shortcuts import render
import pyzbar.pyzbar as pyzbar
import cv2
import numpy

# Create your views here.


def scanner_view(request):
    i = 0
    cap = cv2.VideoCapture(0)

    while i < 1:
        _, frame = cap.read()
        decoded = pyzbar.decode(frame)

        for obj in decoded:
            print(decoded)
            i += 1
        cv2.startWindowThread()
        cv2.imshow("QrCode", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            cv2.destroyAllWindows()
            cap.release()
    context = {'scan': 'QR Successfully Scanned',
               'phone_number': decoded}
    return render(request, 'scanner/scanner.html', context)
