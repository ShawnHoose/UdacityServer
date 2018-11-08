#!/usr/bin/env python3

### Imports ###
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from itemdb import Base, Categories, Items, User

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#clear database
session.query(User).delete()
session.query(Categories).delete()
session.query(Items).delete()
session.commit()

soccer = Categories(name="Soccer", owner_id="1")
session.add(soccer)
session.commit()

BJJ = Categories(name="Brazilian Jiu Jitsu", owner_id="1")
session.add(BJJ)
session.commit()

Karate = Categories(name="Karate", owner_id="1")
session.add(Karate)
session.commit()

Hockey = Categories(name="Hockey", owner_id="1")
session.add(Hockey)
session.commit()

cleats = Items(name="Soccer Cleats",description="Firm ground cleats",cat_id=1,time_added=datetime.now(), owner_id="1")

session.add(cleats)
session.commit()

gloves = Items(name="Keeper Gloves",description="Keeper gloves with extra grip and finger saves",cat_id=1,time_added=datetime.now(), owner_id="1")
session.add(gloves)
session.commit()

bjjgi = Items(name="BJJ Gi",description="Heavy Weight Gi built with resilience for BJJ",cat_id=2,time_added=datetime.now(), owner_id="1")
session.add(bjjgi)
session.commit()

mouthguard = Items(name="Mouthguard",description="Moldable Mouthguard for those hard contacts to keep you in the fight",cat_id=2,time_added=datetime.now(), owner_id="1")
session.add(mouthguard)
session.commit()

karategi = Items(name="Karate Gi",description="Light Weight Gi built to flow and snap for Karate",cat_id=3,time_added=datetime.now(), owner_id="1")
session.add(karategi)
session.commit()

stick = Items(name="Hockey Stick",description="Perfect for those slapshots!",cat_id=4,time_added=datetime.now(), owner_id="1")
session.add(stick)
session.commit()
