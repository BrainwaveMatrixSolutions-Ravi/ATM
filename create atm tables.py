#create Users table
Create table users (
    account_number varchar(10) not null Primary key,
    name varchar(50) not null,
    pin VARCHAR(4) not null,
    Balance Decimal(10,2) DEFAULT 0.00
);


#create Transactions table
Create table transactions (
    id int not null Auto_increment Primary key,
    account_number varchar(10),
    transaction_type enum('deposit', 'withdraw', 'transfer') not null,
    amount Decimal(10,2) not null,
    transaction_date Timestamp Default Current_Timestamp
);

#create Bank table
Create table bank (
    id int not null Auto_increment Primary key,
    username Varchar(40) not null unique,
    password varchar(40) not null,
    Balance Decimal(10,2) Default 0.00
);





