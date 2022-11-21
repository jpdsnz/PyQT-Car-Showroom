#include "dispyvehicletable.h"
#include "ui_dispyvehicletable.h"

DispyVehicleTable::DispyVehicleTable(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::DispyVehicleTable)
{
    ui->setupUi(this);
}

DispyVehicleTable::~DispyVehicleTable()
{
    delete ui;
}
