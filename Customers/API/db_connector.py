import csv
import datetime
import logging
import time
from abc import ABC, abstractmethod

from django.conf import settings
from pymongo import MongoClient

logger = logging.getLogger(__name__)

def calculate_speed(func, message, *args):
    """
    Calculate the time spend by a function call
    :param func:  Function to call
    :param message: Message to print when time speed is available
    :param args:  Arguments to pass to functions
    """
    start = time.time()
    func(*args)
    end = time.time()
    print("Complete %s in" % message, end - start, "s")

class MongoDB_Connector():
    """
    Class for Mongo database operations
    """

    def __init__(self):
        client = MongoClient(settings.MONGO_CONNECTION_STRING)
        self.db = client['Customer']

    def clean_tables(self):
        """
        Delete all data on database if exists.
        """
        self.db['Customers'].drop()

    def fetch(self, path) -> None:
        """
        The template method (design pattern).
        """
        self.clean_tables()
        calculate_speed(self.save_customers, "fetching and processing customers data", path)

    def read(self, data, chunk_size=10000):
        #Complete fetching customer data in 296.4673912525177s = 4min 56s
        #3526301 people created.

        customers = []
        counter = 0
        total = 0

        for customer in data:

            customer = customer.rstrip('\n').split(',')
            if len(customer) >= 23:
                email_valid = customer[5]
                if email_valid == 'Y':

                    row = {
                        "LEGAL_IDENTIFIER": customer[1],
                        "SCV_EMAIL_ADDRESS": customer[4],
                        "VALID_EMAIL_ADDRESS_FLAG": email_valid,
                        "SCV_PHONE1": customer[6],
                        "VALID_PHONE1_FLAG": customer[7],
                        "SCV_PHONE2": customer[8],
                        "VALID_PHONE2_FLAG": customer[9],
                        "SCV_PHONE3": customer[10],
                        "VALID_PHONE3_FLAG": customer[11],
                        "CUSTOMER_GENDER": customer[12],
                        "CUSTOMER_TITLE": customer[13],
                        "CUSTOMER_FORENAME": customer[14],
                        "CUSTOMER_SURNAME": customer[15],
                        "BIRTH_DATE": customer[16],
                        "ROAD_TYPE": customer[17],
                        "STREET": customer[18],
                        "NUM": customer[19],
                        "FLOOR": customer[20],
                        "CITY": customer[21],
                        "PROVINCE": customer[22],
                        "POSTAL_CODE": customer[23],
                    }
                    customers.append(row)

                    counter += 1
                    if counter == chunk_size:
                        yield customers
                        total += counter
                        counter = 0
                        customers.clear() # del personas | Raises local variable referenced before assignment

        if customers:
            total += len(customers)
            print(f"{total} people read.")
            yield customers

    def save_customers(self, path):
        with open(path, encoding='latin-1') as data:
            data.seek(0)
            for block in self.read(data):
                self.db.Customers.insert_many(block)
