#ifndef DISPYVEHICLETABLE_H
#define DISPYVEHICLETABLE_H

#include <QMainWindow>

namespace Ui {
class DispyVehicleTable;
}

class DispyVehicleTable : public QMainWindow
{
    Q_OBJECT

public:
    explicit DispyVehicleTable(QWidget *parent = nullptr);
    ~DispyVehicleTable();

private:
    Ui::DispyVehicleTable *ui;
};

#endif // DISPYVEHICLETABLE_H
