from channels.consumer import AsyncConsumer,SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync



class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):  
        print("websocket connected",event)
        print("channel layer.........",self.channel_layer)  #get default channel layer from a project.
        print("channel name.........",self.channel_name) 

        self.group_name=self.scope['url_route']['kwargs']['GroupName']
        print(self.group_name)

        async_to_sync(self.channel_layer.group_add)(self.group_name,self.channel_name) 

        self.send({                      # this method accepts the connection from server side. 
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):  
        print("websocket Received from client.......",event)  
        print("websocket Received from client.......",event['text'])
       
        async_to_sync(self.channel_layer.group_send)(self.group_name,{
            'type':'chat.message',
            'message':event['text']
        })  

    def chat_message(self,event):
        print("Event....",event)    
        print("Actual data....",event['message'])
        print(" type of Actual data....",type(event['message']))
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
