import cv2
import cvlib

def detect_object(image, model = "yolov4", conf = 0.65, useGPU = False):

    try:
        shp = image.shape
        if shp[2] != 3:
            return 0,0,0
        
        locations, item_names, confidences = cvlib.detect_common_objects(image, model=model, confidence=conf, enable_gpu=useGPU)
        frame = cvlib.object_detection.draw_bbox(image, locations, item_names, confidences, write_conf=True)

        return item_names, confidences, frame
    except Exception as e:
        print("ERROR:", e)
        return 0,0,e


def realtime():

    cam = cv2.VideoCapture(0)#Initialize Video Camera

    while(True):
        
        _, frame = cam.read()# Capture 1 Video frame from Video camera

        try:
            frame = cv2.resize(frame, (640, 480))#Resizing the Image
            #Lower resolution can help in Perormance
            print(frame.shape)

            #detect the objects in frame using Yolov4
            locations, item_names, confidences = cvlib.detect_common_objects(frame, model='yolov4', confidence=0.65, enable_gpu=False)
            #Get all the item names and locations

            print("Number of Items Detected: ", len(item_names))
            print(item_names)
##            print(len(locations), len(item_names), len(confidences))
##            print(locations)
            
##            print(confidences)

        except Exception as e:
            #Handle if any Error
            print(e)

        #Draw Boxes around the Detected Object and Write their Names
        frame = cvlib.object_detection.draw_bbox(frame, locations, item_names, confidences, write_conf=True)

        #Show the Output to the User
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    # finally, close the window
    cv2.destroyAllWindows()

if __name__ == '__main__':
    realtime()
