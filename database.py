import uuid
import psycopg2
from datetime import date

host_name = "localhost"
database_name = "adbms"
user_name = "adbms"
password = "adbms"
port = 5432
con = None
cur = None


try:
    con = psycopg2.connect(
        host=host_name,
        dbname=database_name,
        user=user_name,
        password=password,
        port=port,
    )
    print("connected to database")
except:
    print("connection is cant be created")


delete = '''
            drop table if exists feedback;
            drop table if exists bill_product;
            drop table if exists bill;
            drop table if exists product;
            drop table if exists category;
            drop table if exists address;
            drop table if exists account;
            '''
account = '''create table account(
            id integer primary key,
            name varchar(15),
            l_name varchar(15),
            username varchar(20) not null unique,
            password varchar(20) not null,
            email_address varchar(40) unique,
            last_login varchar(25),
            is_user boolean not null,
            is_staff boolean not null ,
            is_admin boolean not null ,
            varified_email boolean not null 
        );'''


address = '''create table address (
                address_id integer primary key,
                usr integer not null,
                line_1 varchar(50),
                line_2 varchar(50),
                line_3 varchar(50),
                city varchar(20),
                state varchar(20),
                pincode integer,
                is_varified boolean,
                document varchar(60),
                constraint account_user_fk foreign key(usr) references account(id) on delete cascade
            );'''

category = '''create table category(
                    category_id integer primary key,
                    category_name varchar(25)
                    );'''
product = '''create table product (
                product_id integer primary key,
                product_name varchar(50),
                description varchar(250),
                base_price integer,
                current_bid integer,
                current_bidder integer,
                category integer,
                creation_date varchar(10),
                last_bid_date varchar(10),
                image1 varchar(35),
                image2 varchar(35),
                image3 varchar(35),
                image4 varchar(35),
                image5 varchar(35),
                is_upcoming boolean,
                is_ongoing boolean,
                is_completed boolean,
                constraint product_user_fk foreign key(current_bidder) references account(id) on delete cascade,
                constraint product_category_fk foreign key(category) references category(category_id) on delete cascade
            );'''
feedback = '''create table feedback(
                feedback_id integer primary key,
                usr integer,
                feedback varchar(500),
                constraint feedback_user_fk foreign key(usr) references account(id) on delete cascade
                );'''

bill = '''create table bill (
            bill_id integer primary key,
            usr integer,
            total integer,
            generation_date varchar,
            constraint bill_user_fk foreign key(usr) references account(id) on delete cascade
            );'''

bill_product = '''create table bill_product(
    bill_product_id integer primary key,
    bill_no integer,
    product_id integer,
    constraint billproduct_billno foreign key(bill_no) references bill(bill_id) on delete cascade,
    constraint billproduct_productid foreign key(product_id) references product(product_id) on delete cascade
)'''
cur = con.cursor()
cur.execute(delete)
cur.execute(account)
cur.execute(address)
cur.execute(category)
cur.execute(product)
cur.execute(feedback)
cur.execute(bill)
cur.execute(bill_product)

acc = [
    [1,'avinash','kumar','avinash','passwd','mail1@gmail.com',date.today(),'t','t','t','t'],
    [2,'anshul','nathe','anshul','passwd','mail2@gmail.com',date.today(),'t','f','f','t'],
    [3,'Sakshi','Rothe','Sakshi','passwd','mail3@gmail.com',date.today(),'t','t','f','t'],
    [4,'Bhanu','Thapa','Bhanu','passwd','mail4@gmail.com',date.today(),'t','f','f','t'],
    [5,'Akshatha','Niar','akshatha','passwd','mail5@gmail.com',date.today(),'t','f','f','t']
]

for x in acc:
    account_insert = "insert into account values( " + str(x[0]) + " , '" + x[1] + "' , '" + x[2] + "' , '" + x[3] + "' , '" + x[4] + "' , '" + x[5] + "' , '" + str(x[6]) + "' , '" + x[7] + "' , '" + x[8] + "' , '" + x[9] +  "' , '" + x[10] +  "' );"
    cur.execute(account_insert)

cat = [
    [1,'Art'],
    [2,'Painting'],
    [3,'Collactable'],
    [4,'Sulptures'],
    [5,'Modern Art'],
]

for x in cat:
    category_insert = "insert into category values ( " + str(x[0]) + " , '" + x[1] + "');"
    cur.execute(category_insert)

addr = [
    ['1','5','addp1l1','addp1l2','addp1l3','city','state','123456','t','document_name1.pdf'],
    ['2','4','addp2l1','addp2l2','addp2l3','city','state','223456','t','document_name2.pdf'],
    ['3','3','addp3l1','addp3l2','addp3l3','city','state','323456','t','document_name3.pdf'],
    ['4','2','addp4l1','addp4l2','addp4l3','city','state','423456','t','document_name4.pdf'],
    ['5','1','addp5l1','addp5l2','addp5l3','city','state','523456','t','document_name5.pdf'],
] 

def file_name():
    filename = str(uuid.uuid4()) + ".pdf"
    return filename

for x in addr:
    addr_insert = "insert into address values ( "+ x[0] + "," + x[1] + ",'" + x[2] + "','" + x[3] + "','" + x[4] + "','" + x[5] + "','" + x[6] + "'," + x[7] + ",'" + x[8] + "','" + file_name() + "');"       
    cur.execute(addr_insert)

prod  = [
    ['1','Mona Lisa','Very Famus Painting','89000','1245670','1','1','2022-11-10','2022-11-11','image1','image2','image3','','','f','t','f'],
    ['2','DaVichi','Very Famus art','89000','1234560','2','2','2022-11-10','2022-11-12','image1','image2','image3','','','f','t','f'],
    ['3','Specture','Very Famus sculpture','89000','1234570','3','1','2022-11-10','2022-11-13','image1','image2','image3','','','f','t','f'],
    ['4','Charltor','Very Famus device','89000','1234670','4','2','2022-11-10','2022-11-14','image1','image2','image3','','','f','t','f'],
    ['5','Nuke','Very Famus book','89000','1235670','5','3','2022-11-10','2022-11-15','image1','image2','image3','','','f','t','f'],
]

for x in prod:
    prod_insert = "insert into product values (" + x[0] + ",'" + x[1] + "','" + x[2] + "','" + x[3] + "'," + x[4] + "," + x[5] + "," + x[6] + ",'" + x[7] + "','" + x[8] + "','" + x[9] + "','" + x[10] + "','" + x[11] + "','" + x[12]  + "','" + x[13] + "','" + x[14]  + "','" + x[15] + "','" + x[16] + "');"
    cur.execute(prod_insert)

fedbak = [
    ['1','1','This is a very nice feedback that is given by the user in their calmful mind.'],
    ['3','2','This is a very nice feedback that is given by the user in their calmful mind.'],
    ['4','5','Such a hidious site, never seen such one before.'],
    ['2','3','This is a very nice feedback that is given by the user in their calmful mind.'], ]
for x in fedbak:
    fed = "insert into feedback values ( " + x[0] + "," + x[1] + ",'" + x[2] + "');"
    cur.execute(fed)
            # bill_id integer primary key,
            # usr integer,
            # total integer,
            # generation_date varchar
bill_no = [
    ['1','1','127980','2022-11-22'],
    ['2','2','127980','2022-11-22'],
    ['3','3','127980','2022-11-22'],
    ['4','4','127980','2022-11-22'],
    ['5','5','127980','2022-11-22'],
]
for x in bill_no:
    bil = "insert into bill values(" + x[0] + "," + x[1] + "," + x[2] + ",'" + x[3] + "');"
    cur.execute(bil)
bill_prod = [
    ['1','2','3'],
    ['2','3','4'],
    ['3','4','5'],
    ['4','5','1'],
    ['5','1','2'],
]
for x in bill_prod:
    bil = "insert into bill_product values(" + x[0] + "," + x[1] + "," + x[2] + ");"
    cur.execute(bil)
con.commit()