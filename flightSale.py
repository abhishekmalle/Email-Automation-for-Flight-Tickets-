from amadeus import Flights
import smtplib

key = 'uc3P6EbsIUyjwIfT9eQLyNdUp4CbWbem'
flights = Flights(key)
resp = flights.extensive_search(
    origin='ATL',
    destination='DEN',
    departure_date='2018-02--2018-03')

a = resp['results'][0]['airline']
b = resp['results'][0]['price']
c = resp['results'][1]['airline']
d = resp['results'][1]['price']
e = resp['results'][2]['airline']
f = resp['results'][2]['price']
flight1 = f'{a} flight: {b}\n'
flight2 = f'{c} flight: {d}\n'
flight3 = f'{e} flight: {f}\n'

#SENDING EMAIL
smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.ehlo()
smtp_server.starttls()
email = 'flightsaleresponse@gmail.com'
apppwd = 'kxgrfartdbtkdubf'
smtp_server.login(email, apppwd)
toaddr = 'izaankml@gmail.com' #CHANGE TO ACTUAL SENDER
msg = "\r\n".join([
   "From: flightsaleresponse@gmail.com",
   "To: izaankml@gmail.com",
   "Subject: Your flight offers for the week",
   f"Your top 3 flights from {resp['origin']} to {resp['results'][3]['destination']}\n",
   flight1,
   flight2,
   flight3,
   "Thank You, and have a great day!"
   ])
smtp_server.sendmail(email, toaddr, msg)

# import boto3

# dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")


# table = dynamodb.create_table(
#     TableName='Movies',
#     KeySchema=[
#         {
#             'AttributeName': 'year',
#             'KeyType': 'HASH'  #Partition key
#         },
#         {
#             'AttributeName': 'title',
#             'KeyType': 'RANGE'  #Sort key
#         }
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'year',
#             'AttributeType': 'N'
#         },
#         {
#             'AttributeName': 'title',
#             'AttributeType': 'S'
#         },

#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 10,
#         'WriteCapacityUnits': 10
#     }
# )

# print("Table status:", table.table_status)
