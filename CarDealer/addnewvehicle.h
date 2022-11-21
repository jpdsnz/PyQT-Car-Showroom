#ifndef ADDNEWVEHICLE_H
#define ADDNEWVEHICLE_H

#include <QMainWindow>

namespace Ui {
class AddnewVehicle;
}

class AddnewVehicle : public QMainWindow
{
    Q_OBJECT

public:
    explicit AddnewVehicle(QWidget *parent = nullptr);
    ~AddnewVehicle();

private:
    Ui::AddnewVehicle *ui;
};

#endif // ADDNEWVEHICLE_H
