from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime
engine = create_engine('sqlite:///ddd.db', echo = True)
meta = MetaData()

data_digital = Table(
   'data_digital', meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String), 
   Column('email', String),
   Column('telephone', String), 
   Column('location', String),
   Column('sub_total', String), 
   Column('tax_rate', String),
   Column('tax', String),
   Column('total', String), 
   Column('description', Text),
   Column('isp_bill', Text),
   Column('date_add', DateTime)

)
meta.create_all(engine)