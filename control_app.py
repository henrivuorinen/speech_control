import os
import cv2
from wifi_controller import WifiController

def receive_video_stream(wifi_controller):
    try:
        # Connect to the Raspberry Pi server
        wifi_controller.connect()

        # Receive video frames from the server and display them
        while True:
            frame_bytes = wifi_controller.receive_data()  # Receive frame data
            # Convert frame bytes to OpenCV image format
            frame = cv2.imdecode(frame_bytes, cv2.IMREAD_COLOR)
            cv2.imshow("Video Stream", frame)  # Display frame
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break  # Break the loop if 'q' is pressed

    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting...")
    finally:
        wifi_controller.disconnect()

if __name__ == "__main__":
    raspberry_ip = "10.42.0.1"  # Replace this with the Raspberry Pi's IP address
    raspberry_port = 12345
    wifi_controller = WifiController(ip_address=raspberry_ip, port=raspberry_port)

    try:
        receive_video_stream(wifi_controller)
    finally:
        cv2.destroyAllWindows()  # Close OpenCV windows
