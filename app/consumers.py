from channels.consumer import AsyncConsumer,SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .models import *


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):  
        print("websocket connected",event)
        print("channel layer.........",self.channel_layer)  #get default channel layer from a project.
        print("channel name.........",self.channel_name) 

        self.user = self.scope['user']  #get a authenticated user 

        # self.group_name=self.scope['url_route']['kwargs']['GroupName']  # get a group name
        # print(self.group_name)

        async_to_sync(self.channel_layer.group_add)(self.group_name,self.channel_name) 

        self.send({                      # this method accepts the connection from server side. 
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):  
        print("Message Received from client.......",event)            #Message Received from client....... {'type': 'websocket.receive', 'text': '{"msg":"hy"}'}
        print("Message Received from client.......",event['text'])    #Message Received from client....... {"msg":"hy"}
        print("Type of Message Received from client.......",type(event['text']))    #Type of Message Received from client....... <class 'str'>
        
        
        data=json.loads(event['text'])  #convert string to python dict.(bcz we have to save the msg in databse..and database only save python dictionary.(not string values))
        print("Data...",data)           ##Data... {'msg': 'hy'}
        print("Type of Data...",type(data))    #Type of Data... <class 'dict'>
        print('Actual message',data['msg'])    #Actual message hy

        print(self.scope['user'])  #get a user (login or not).for eg:-admin

        group=Group.objects.get(name=self.group_name)  #find group object
        if self.scope['user'].is_authenticated:   #if user is login it returns true and this run the loc.

            #create a new chat object
            chat=Chat(content=data['msg'],group=group)
            chat.save()
            
            data['user']=self.scope['user'].username   
            async_to_sync(self.channel_layer.group_send)(self.group_name,{
                'type':'chat.message',
                'message':json.dumps(data)   #convert dict to string(when we send data to frontend)
            })  
        else:
            self.send({ 
                'type':'websocket.send',
                'text':json.dumps({'msg':'login required','user':'guest'})  #convert python dict to string.(bcz only string data is send to fromntend. )
            })

    def chat_message(self,event):
        print("Event....",event)    #return Event.... {'type': 'chat.message', 'message': '{"msg": "hy", "user": "admin"}'}
        print("Actual data....",event['message'])   #Actual data.... {"msg": "hy", "user": "admin"}
        print(" type of Actual data....",type(event['message']))   # type of Actual data.... <class 'str'>
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })    

    def websocket_disconnect(self, event):  
        print("websocket dissconnected.....",event)
        print("channel layer.........",self.channel_layer) 
        print("channel name.........",self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)
        
        raise StopConsumer()


#Async Web Socket.
class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):  
        print("websocket connected",event)
        print("channel layer.........",self.channel_layer)  #get default channel layer from a project.
        print("channel name.........",self.channel_name) 

        await self.channel_layer.group_add("programmers",self.channel_name) 

        await self.send({                      # this method accepts the connection from server side. 
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):  
        print("websocket Received from client.......",event)  
        print("websocket Received from client.......",event['text'])
       
        await self.channel_layer.group_send("programmers",{
            'type':'chat.message',
            'message':event['text']
        })  

    async def chat_message(self,event):
        print("Event....",event)    
        print("Actual data....",event['message'])
        print(" type of Actual data....",type(event['message']))
        await self.send({
            'type':'websocket.send',
            'text':event['message']
        })    


    async def websocket_disconnect(self, event):  
        print("websocket dissconnected.....",event)
        print("channel layer.........",self.channel_layer) 
        print("channel name.........",self.channel_name)
        await self.channel_layer.group_discard("programmers",self.channel_name)
        
        raise StopConsumer()

#  def websocket_receive(self, event):  
#         print("Message Received from client.......",event)  
#         print("Message Received from client.......",event['text'])
#         print("Type of Message Received from client.......",type(event['text']))

#         data=json.loads(event['text'])  #convert string to python dict.
#         print("Data...",data)
#         print("Type of Data...",type(data))
#         print('Actual message',data['msg'])
#         print(self.scope['user'])  #get a user (login or not).

#         group=Group.objects.get(name=self.group_name)  #find group object
#         if self.scope['user'].is_authenticated:   #if user is login it returns true and this run the loc.

#             #create a new chat object
#             chat=Chat(content=data['msg'],group=group)
#             chat.save()
            
#             async_to_sync(self.channel_layer.group_send)(self.group_name,{
#                 'type':'chat.message',
#                 'message':event['text']   #only string value is send in frontend side.
#             })  
#         else:
#             self.send({
#                 'type':'websocket.send',
#                 'text':json.dumps({'msg':'login required'})  #convert python dict to string.
#             })

#django channels documentations
from channels.generic.websocket import WebsocketConsumer

class MyConsumer(WebsocketConsumer):
    groups = ["broadcast"]

    def connect(self):
        print("websocket connected...")

        # Called on connection.
        # To accept the connection call:
        self.accept()  #accepts the connection by server.
        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']
        self.accept("subprotocol")
        # To reject the connection, call:
        self.close()

    def receive(self, text_data=None, bytes_data=None):
        print("Message Received from client.......",text_data)        
        
        # Called with either text_data or bytes_data for each frame
        # You can call:
        self.send(text_data="Hello world!")  #when server sends the data from client.
        # Or, to send a binary frame:
        self.send(bytes_data="Hello world!")
        # Want to force-close the connection? Call:
        self.close()
        # Or add a custom WebSocket error code!
        self.close(code=4123)

    def disconnect(self, close_code):
        # Called when the socket closes
        pass



class MyWebSocketConsumer(WebsocketConsumer):
    def connect(self):
        print("WebSocket Connected....")
        self.accept()  # To accept the connection call:
        # self.close()   # To reject the connection, call forcefully.

    def receive(self,text_data=None,bytes_data=None):
        print("Message received from cleint...",text_data)

        self.send(text_data='message from server to client')
        # self.send(bytes_data="Hello world!")

    def dissconnect(self,close_code):
        print("WebSocket Dissconnected...",close_code)



from channels.generic.websocket import AsyncWebsocketConsumer
class MysyncWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket Connected....")
        await self.accept()  # To accept the connection call:
        # await self.close()   # To reject the connection, call forcefully.

    async def receive(self,text_data=None,bytes_data=None):
        print("Message received from cleint...",text_data)

        await self.send(text_data='message from server to client')
        # self.send(bytes_data="Hello world!")

    async def dissconnect(self,close_code):
        print("WebSocket Dissconnected...",close_code)

        
