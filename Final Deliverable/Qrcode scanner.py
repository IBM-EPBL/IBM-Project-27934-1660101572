import cv2 as cv  
 import numpy as np  
 import time  
 import pyzbar.pyzbar as pyzbar  
 from ibmcloudant.cloudant_v1 import CloudantV1  
 from ibmcloudant import CouchDbSessionAuthenticator  
 from ibm_cloud_sdk_core.authenticators import BasicAuthenticator  
 import wiotp.sdk.device  
 authenticator=BasicAuthenticator('apikey-v2-2ji0x00sov1b6clf61hctelp07os2c41mauy6mk7a3ot', '6866a033c311b4968d996ca9fa217206')  
 service=CloudantV1(authenticator=authenticator)  
 service.set_service_url('https://apikey-v2-2ji0x00sov1b6clf61hctelp07os2c41mauy6mk7a3ot:6866a033c311b4968d996ca9fa217206@53e4077b-d008-4545-8ea1-1d70926b1b71-bluemix.cloudantnosqldb.appdomain.cloud')  
   
 cap = cv.VideoCapture(0)  
 font = cv.FONT_HERSHEY_PLAIN   
 if not cap.isOpened():  
     print("Cannot open camera")  
     exit()  
   
   
 myConfig = {  
     "identity" :{  
         "orgId":"u3neop",  
         "typeId":"qrcode",  
         "deviceId":"1234567"  
         },  
     "auth":{  
         "token":"1234567890"  
         }  
     }  
 def myCommandCallback(cmd):  
     print("Message received fromIBM IoT Platform: %s" % cmd.data['command'])  
     m=cmd.data['command']  
   
 client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)  
 client.connect()  
   
 def pub(data):  
     client.publishEvent(eventId = "status", msgFormat="json", data=response, qos=0, onPublish=None)  
     print("Published data Successfully: %s",response)  
     print("\n")  
   
 while True:  
     ret, frame=cap.read()  
     decodedObjects = pyzbar.decode(frame)  
     if not ret:  
         print("Can't receive frame (stream end?). Exiting ...")  
         break  
     for obj in decodedObjects:  
         a=obj.data.decode('UTF-8')  
         cv.putText(frame, "Ticket", (50,50),font,2,  
                     (255 ,0, 0),3)  
   
         try:  
             response=service.get_document(  
                 db='bookingdetails',  
                 doc_id = a  
                 ) .get_result()  
             print(response)  
             print("\n\n")  
             pub(response)  
             time.sleep(5)  
         except Exception as e:  
             response={'Error':'Not a Valid Ticket'}  
             pub(response)  
             print("Not a Valid Ticket")  
             print("\n\n")  
             time.sleep(5)  
   
     cv.imshow("Frame" ,frame)  
     if cv.waitKey(1) & 0xFF == ord('q'):  
         break  
     client.commandCallback = myCommandCallback  
 cap.release()  
 cv.destroyAllWindows()  
 client.disconnect() 
