tables = {}

room_schema = """
CREATE TABLE IF NOT EXISTS `room`(
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL
) ENGINE=INNODB;
"""

student_schema = """
    CREATE TABLE IF NOT EXISTS `student`(
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `birthday` DATE NOT NULL,
    `room` INT,
    `sex` VARCHAR(1) NOT NULL,
    FOREIGN KEY (`room`)
        REFERENCES `room`(`id`)
) ENGINE=INNODB;
"""

tables["room"] = room_schema
tables["student"] = student_schema

