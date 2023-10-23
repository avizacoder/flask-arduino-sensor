CREATE DATABASE app_weather;

use app_weather;

CREATE TABLE sensor(
    id INT UNIQUE NOT NULL AUTO_INCREMENT,
    name_sensor VARCHAR(250) UNIQUE NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE historial(
    id INT UNIQUE NOT NULL AUTO_INCREMENT,
    dato_sensor FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sensor_id INT,
    FOREIGN KEY (sensor_id) REFERENCES sensor(id) 
);


INSERT INTO sensor(name_sensor)
VALUES ('temperatura');
INSERT INTO sensor(name_sensor)
VALUES ('presion');
INSERT INTO sensor(name_sensor)
VALUES ('altitud');


SELECT sensor.name_sensor, historial.id, historial.dato_sensor, historial.created_at 
FROM sensor
RIGHT JOIN historial
ON sensor.id = historial.sensor_id;