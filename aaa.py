from escpos import *
""" Seiko Epson Corp. Receipt Printer M129 Definitions (EPSON TM-T88IV) """
Epson = printer.Usb(0x04b8,0x0202)
# Print text
Epson.text("Hello World\n")
# Print image
Epson.image("logo.gif")
# Print QR Code
Epson.qr("You can readme from your smartphone")
# Print barcode
Epson.barcode('1324354657687','EAN13',64,2,'','')
# Cut paper
Epson.cut()