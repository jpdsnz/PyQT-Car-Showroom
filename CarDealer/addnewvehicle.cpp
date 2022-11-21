#include "addnewvehicle.h"
#include "ui_addnewvehicle.h"

AddnewVehicle::AddnewVehicle(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::AddnewVehicle)
{
    ui->setupUi(this);
}

AddnewVehicle::~AddnewVehicle()
{
    delete ui;
}
