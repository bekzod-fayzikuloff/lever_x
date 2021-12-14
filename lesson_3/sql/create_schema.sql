CREATE TABLE IF NOT EXISTS student(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    room_id INT,
    sex VARCHAR(1) NOT NULL,
    FOREIGN KEY (room_id)
        REFERENCES room(id)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS room(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
) ENGINE=INNODB;