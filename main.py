import os
import sys
from qtpy import QtWidgets
from PyQt5.QtWidgets import *
from PIL import Image
from PyQt5.QtGui import *
import sqlite3
import matplotlib.pyplot as plt
from CarDealer.mainwindow import Ui_MainWindow
from CarDealer.addnewvehicle import Ui_AddnewVehicle
from CarDealer.dispyvehicletable import Ui_DispyVehicleTable

# ------ Global Variables ------ #
con = sqlite3.connect("car dealer.db")  # need the .db here at the end!
cur = con.cursor()
replacementPicture = "pictures/question.jpg"  # Need global variable for picture


# ------ Main Window Widget ------ #
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("icons/deal.png"))

        # Icons - Icons for menu when creating exe data
        self.ui.actionadd_new_vehiclemenuToolbar.setIcon(QIcon("icons/label.png"))
        self.ui.actionadd_new_vehicleMenu.setIcon(QIcon("icons/label.png"))
        self.ui.label_PictureMainWindow.setPixmap(QPixmap("pictures/lamborghini.Yellow.png"))

        # Connections - What happens when clicking on buttons
        self.ui.actionadd_new_vehicleMenu.triggered.connect(self.showAddNewVehicleWindowMenu)
        self.ui.actionadd_new_vehiclemenuToolbar.triggered.connect(self.showAddNewVehicleWindowMenuToolbar)
        self.ui.actionShow_existing_vehiclesMenu.triggered.connect(self.showVehicleTable)

    # ------ Button Functions ------ #
    def showAddNewVehicleWindowMenu(self):
        self.ui.showaddnewvehiclewidow = AddnewVehicle()
        self.ui.showaddnewvehiclewidow.show()
        self.close()  # close main window

    def showAddNewVehicleWindowMenuToolbar(self):
        self.ui.showaddnewvehiclewidow = AddnewVehicle()
        self.ui.showaddnewvehiclewidow.show()
        self.close()  # close main window

    def showVehicleTable(self):
        self.ui.showvehicletable = DispyVehicleTable()
        self.ui.showvehicletable.show()
        self.close()


# ------ Classes ------ #
class AddnewVehicle(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AddnewVehicle()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("icons/deal.png"))
        self.ui.label_pictureAddNewVehicle.setPixmap(QPixmap("pictures/label.png"))

        # Connect buttons for add vehicle - Method name inside parentheses for action
        self.ui.pushButton_UploadVehiclePictureAddNewVehicle.clicked.connect(self.UploadVehiclePicture)
        self.ui.pushButton_SubmitAddNewVehicle.clicked.connect(self.addNewVehicle)

    def UploadVehiclePicture(self):
        global replacementPicture
        size = (700, 250)

        file, imageFile = QFileDialog.getOpenFileName(self, "Upload pictures", "C:\\", "Pictures Files(*.jpg *.png)")
        print(file, "file")  # url to file
        print(imageFile, 'imageFile')
        if imageFile:
            replacementPicture = os.path.basename(file)  #
            print(replacementPicture, "replacementPicture")
            picture = Image.open(file)
            print(picture, "picture")
            picture = picture.resize(size)  # Resize the selected picture to size variable
            print(picture, "picture")
            picture.save("pictures/{}".format(replacementPicture))  # Save in database

    def addNewVehicle(self):
        global replacementPicture

        vehicleName = self.ui.lineEditVehicleNameAddNewVehicle.text()
        manufacturer = self.ui.lineEditManufacturerAddNewVehicle.text()
        constructionYear = self.ui.lineEditConstructionYearAddNewVehicle.text()
        kmStood = self.ui.lineEditKmStoodAddNewVehicle.text()
        vehicleCondition = self.ui.comboBox_VehicleConditionAddNewVehicle.currentText()  # Combo box uses currentText()
        numberOfPieces = self.ui.lineEditNumberOfPiecesAddNewVehicle.text()
        price = self.ui.lineEditPriceAddNewVehicle.text()
        currency = self.ui.comboBoxCurrencyAddNewVehicle.currentText()

        if (
                vehicleName and manufacturer and constructionYear and kmStood and vehicleCondition and numberOfPieces and price != ""):
            try:
                query = "INSERT INTO vehicle(vehicle_name, manufacturer, construction_year, km_stood, vehicle_condition, pieces, price, currency, picture) VALUES(?,?,?,?,?,?,?,?,?)"
                result = cur.execute(query, (
                    vehicleName, manufacturer, constructionYear, kmStood, vehicleCondition, numberOfPieces, price,
                    currency,
                    replacementPicture))
                print(result, "result")
                con.commit()  # Use this to change something in db!
                QMessageBox.information(self, "Info", "vehicle has been added")
                self.close()
                self.ui.mainWindow = MainWindow()
                self.ui.mainWindow.close()
                self.ui.displytable = DispyVehicleTable()
                self.ui.displytable.show()  # Show table after entering a new vehicle!
            except:
                QMessageBox.information(self, "Warning", "vehicle has not been added")
        else:
            QMessageBox.critical(self, "Warning", "Fields cannot be empty!")  # Can use QMessageBox. "critical, warning, question" for types

    def closeEvent(self, event):
        self.ui.mainWindow = MainWindow()
        self.ui.mainWindow.show()


class DispyVehicleTable(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DispyVehicleTable()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("icons/deal.png"))
        self.displyVehicleTable()

        # Fix Column Width for Table (index, width)
        self.ui.tableWidgetShowVehicles.setColumnWidth(0, 35)
        self.ui.tableWidgetShowVehicles.setColumnWidth(1, 340)
        self.ui.tableWidgetShowVehicles.setColumnWidth(2, 200)
        self.ui.tableWidgetShowVehicles.setColumnWidth(3, 230)
        self.ui.tableWidgetShowVehicles.setColumnWidth(4, 150)
        self.ui.tableWidgetShowVehicles.setColumnWidth(5, 120)
        self.ui.tableWidgetShowVehicles.setColumnWidth(6, 100)
        self.ui.tableWidgetShowVehicles.setColumnWidth(7, 140)
        self.ui.tableWidgetShowVehicles.setColumnWidth(8, 130)
        self.ui.tableWidgetShowVehicles.setColumnWidth(9, 155)

        # Search Button
        self.ui.pushButton_SearchForVehicle.clicked.connect(self.searchForVehicle)

    def displyVehicleTable(self):
        query = "SELECT vehicle_id, vehicle_name, manufacturer, construction_year, km_stood, vehicle_condition, pieces, price, currency, availability FROM vehicle"
        result = cur.execute(query,)  # Execute query, (single query needs comma!)
        print(result, 'result')  # Check query in cmd line!

        for row in result:
            print(row, "row")
            rowNumber = self.ui.tableWidgetShowVehicles.rowCount()
            print(rowNumber, 'rowNumber')
            self.ui.tableWidgetShowVehicles.insertRow(rowNumber)
            for columnNumber, data in enumerate(row):  # Enumerate makes number for every single col in row
                print(columnNumber, 'columnNumber')
                print(data, 'data')
                self.ui.tableWidgetShowVehicles.setItem(rowNumber, columnNumber, QTableWidgetItem(str(data)))

    def searchForVehicle(self):
        value = self.ui.lineEditLookingForVehicle.text()
        if value == "":
            QMessageBox.warning(self, "Warning", "search fields cannot be empty!")
            self.ui.lineEditLookingForVehicle.setText("")
        else:
            query = "SELECT vehicle_id, vehicle_name, manufacturer, construction_year, km_stood, vehicle_condition, pieces, price, currency, availability FROM vehicle WHERE vehicle_name LIKE? or manufacturer LIKE?"
            result = cur.execute(query,('%' + value + '%', '%' + value + '%')).fetchall()  # Execute query, compare 2 string values
            print(result, "result")
            if result == []:
                QMessageBox.warning(self, "Warning", "Vehicle name or manufactuter not found!")
                self.ui.lineEditLookingForVehicle.setText("")
                return
            else:
                self.ui.tableWidgetShowVehicles.setRowCount(0)  # Clear the table if a record is found!
                for row in result:
                    print(row, "row")
                    rowNumber = self.ui.tableWidgetShowVehicles.rowCount()
                    print(rowNumber, "rowNumber")
                    self.ui.tableWidgetShowVehicles.insertRow(rowNumber)
                    for columnNumber, data in enumerate(row):
                        print(columnNumber, "columnNumber")
                        print(data, 'data')
                        self.ui.tableWidgetShowVehicles.setItem(rowNumber, columnNumber, QTableWidgetItem(str(data)))


    def closeEvent(self, event):
        self.ui.mainWindow = MainWindow()
        self.ui.mainWindow.show()


# -------- Main App Execution -------- #
app = QApplication(sys.argv)
print(app, "app")
window = MainWindow()
window.show()
sys.exit(app.exec_())
