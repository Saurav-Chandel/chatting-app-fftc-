from channels.consumer import AsyncConsumer,SyncConsumer
from channels.exceptions import StopConsumer




class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):  
        print("websocket connected",event)
        print("channel layer.........",self.channel_layer)  #get default channel layer from a project.
        print("channel name.........",self.channel_name)  

        self.send({                      # this method accepts the connection from server side. 
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):  
        print("websocket Received from client.......",event)    

    def websocket_dissconnect(self, event):  
        print("websocket dissconnected.....",event)
        raise StopConsumer()
