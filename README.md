# Picamera Websocket for Teachable Machine

## How to use

1. plug in camera
2. setup camera
    - offical [Documentation](https://www.raspberrypi.org/documentation/configuration/camera.md)
3. clone this repo to your home directory
4. install python dependencies 
    ```
    pip3 install -r requirements.txt
    ```
5. open SSH tunnel to your raspberry
    ```
    ssh pi@<raspberry-ip> -L 8080:<raspberry-ip>:8080
    ```
6. run python script
    ```
    python3 server.py
    ```
7. visit Teachable Machine 
    - to collect images via the network append the following code to the [link](https://teachablemachine.withgoogle.com/train/image?network=true)
    ```
    ?network=true
    ```
    - now three options for uploading images show up. 
        - Wecam
        - Upload
        - Network <-- **that is what you want**
    - use the configured websocket address `localhost` and the port `8080`
    - press **connect**
    - now you cann add images to the class by pressing the **record** button
