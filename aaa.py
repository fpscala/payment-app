from escpos import *

# Xprinter = printer.Usb(0x1046, 0x20497)
Xprinter = printer.Network("192.162.1.101", 9100)
for copies in range(0, 2):
    Xprinter.set(bold=True, align='center')
    Xprinter.image("img/data_logo_250.png")
    Xprinter.text("\"DATA UNION\" MCHJ")
    Xprinter.set(align='center')
    Xprinter.text(" ga qarashli\n")
    Xprinter.set(bold=True, align='center')
    Xprinter.text("\"DATA\"")
    Xprinter.set(align='center')
    Xprinter.textln(" o'quv markazi\n Kirim order No:")
    Xprinter.ln()
    Xprinter.set(align='left', font='a')
    Xprinter.control("HT", tab_size=30)
    Xprinter.text("     To'lovchi:\t")
    Xprinter.textln("John Dao")

    Xprinter.text("     To'lov summasi:\t")
    Xprinter.textln("John Dao")

    Xprinter.text("     To'lov summasi:\t")
    Xprinter.textln("John Dao")

    Xprinter.text("     To'lov turi:\t")
    Xprinter.textln("John Dao")

    Xprinter.text("     Sana:\t")
    Xprinter.textln("John Dao")

    Xprinter.text("     Guruh:\t")
    Xprinter.textln("John Dao")

    Xprinter.text("     Kurs oyi uchun:\t")
    Xprinter.textln("John Dao")

    Xprinter.text("     Qarz qoldig'i:\t")
    Xprinter.textln("John Dao\n")

    Xprinter.set(align='center', font='b')
    if copies == 1:
        Xprinter.textln('@data_learning_centre\n')
        Xprinter.set(align='left', bold=True)
        Xprinter.text('     Imzo:     _______________________________')
    else:
        Xprinter.text('@data_learning_centre\n'
                      '+99899 757 88 86 \n'
                      '+99899 758 88 86 \n'
                      '+99899 759 88 86')

    Xprinter.cut()
