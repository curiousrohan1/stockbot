# stockbot

## Schema
```
CREATE TABLE `Quotes` ( 
    `date` TEXT NOT NULL, 
    `time` TEXT NOT NULL,
    `symbol` TEXT NOT NULL, 
    `price` REAL NOT NULL, 
    PRIMARY KEY(`date`,`time`,`symbol`) )

CREATE INDEX `i_symbol` ON `Quotes` ( `symbol` ASC, `date` ASC )
```

## Configuration
Copy the stockbot.properties.template to stockbot.properties and edit the properties to fit your environment.
