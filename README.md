# Item catalog
## Udacity Full Stack Web Development ND Project 2

___________________________________________

## About

This project created a item database website with login capabilities which allowed for further administrative access of the database including creating, editing, and deleting items and categories.

## Prerequisites

* Python3 -- Download at https://www.python.org/downloads/

* VirtualBox -- A linux virtualization environment (virtual machine) that we run our server on. Download at https://www.virtualbox.org/

* Vagrant -- Allows us to manage and access our virtual machine. Download at https://www.vagrantup.com/downloads.html

* SQLAlchemy -- A Python SQL toolkit and Object Relational Mapper [ORM] that allows us to interact with our database in our Python code. Installed through the terminal via `pip install sqlalchemy`

* Flask -- A web framework that allows for an easy way to bind functions to URL's to create a RESTFUL API. Installed through the terminal via `pip install flask`

* Flask Login -- An extension of Flask that allows for easy Login / Logout functionality. Installed through the terminal via `pip install flask-login`

* Flask Dance -- An extension of Flask that allows for easy OAuth2 implementation. Installed through the terminal via `pip install flask-dance[sqla]` (Since we have used SQLAlchemy).

* Requests -- Allows for the sending of HTTP requests through Python. Installed through the terminal via `pip install requests`

* WTForms -- Allows for the creation of and access to login forms and fields to gather user data, such as Username and Password. Installed through the terminal via `pip install wtforms`

* ItsDangerous -- Allows for protecting data via signing before sending the data. Used to protect user information in the database. Installed through the terminal via `pip install itsdangerous`

___________________________________________


## The Database

The database contains three tables:

* Users
  ```python3
  __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))
    authenticated = Column(Boolean, default=False)
    oauth = Column(Boolean, default=False)
  ```
  * Includes hash_password, verify_password, is_active, is_authenticated, is_anonymous, get_id methods

* Categories
  ```
  __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(64),  nullable=False)
    owner_id = Column(Integer, ForeignKey('user.id'))
  ```
  * Includes a JSON Serialize method

* Items
  ```
  __tablename__ = 'items'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(64))
    description = Column(String(256))
    cat_id = Column(Integer, ForeignKey('categories.id'))
    owner_id = Column(Integer, ForeignKey('user.id'))
    time_added = Column(DateTime)
    categories = relationship(Categories)
  ```
  * Includes a JSON Serialize method

## Connecting to the virtual machine

After VirtualBox and Vagrant are installed, follow the below steps to initialize and access the database on your virtual machine.

* Open a new terminal/shell window
* Navigate to the `/vagrant` directory that was created when you installed Vagrant using the `cd` command
* Initialize your vagrant environment with `vagrant init`
* Enter the command `vagrant up` to initialize the virtual machine
* Enter the command `vagrant ssh` to log into the virtual machine
* Once in the virtual machine, navigate to the `/vagrant` folder using the same method as before

## Running the website

In your virtual machine, navigate to the folder containing all the python files. This should be `/vagrant/itemCatalog`. We can initialize the database by running `python3 itemdb.py`.

Next, so our website is interesting and pretty when we first load it in, and so we don't have to go through the hassle of adding in a lot of items and categories initially, we can populate the database by running `python3 populateCatalog.py`. This will populate the database with 4 categories and 6 items.

Simply run `python3 itemCatalog.py` now, and we're in business! Open your favorite browser and navigate to http://localhost:8000 and begin to explore!

___________________________________________


## The website

All pages of the website will present the same header containing a title link and a login/logout button. They will also all have the same footer with a link to the homepage.

The homepage of the website contains a list of all categories on the left hand side as well as the 6 most recently created items on the right. Within each category will be a list of the items as well as the total count of items. Within each item it will list the item name and description as well as a link returning you to the items parent category.

If a user has logged in with either a local account or their Google account, they will have access to create or edit categories and create, edit, or delete items.
