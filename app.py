import streamlit as st 
import os 
import zipfile
from streamlit_option_menu import option_menu
from tensorflow.keras.models import load_model
from streamlit_extras.grid import grid
from helper import get_label
from transformers import DetrImageProcessor, DetrForObjectDetection
st.set_page_config(layout="wide", page_title="Foot and  Mouth Detection", initial_sidebar_state="expanded", page_icon="cattle.webp")
with zipfile.ZipFile('fmd_detection_model.zip' , "r") as z:
    z.extractall(".")
import smtplib, ssl

smtp_server = "smtp-relay.brevo.com"
port = 587  # For starttls
sender_email = "kenliz1738@gmail.com"
password = os.environ["mail_pass"] 
sender_password = password
subject = "Foot  and  Mouth Disease  Alert"
import smtplib
from email.mime.text import MIMEText
body = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Foot and Mouth Disease Outbreak Alert</title>
</head>
<body>
    <p>Dear Veterinary and Farming Community,</p>

    <p>I hope this email finds you well. Unfortunately, I am writing to bring to your attention a matter of utmost importance. It has come to our attention that there is a confirmed outbreak of Foot and Mouth Disease within our region.</p>

    <p>Foot and Mouth Disease poses a significant threat to our livestock and agricultural operations. Given its highly contagious nature, it is imperative that we take immediate and decisive action to contain and mitigate the spread of this disease.</p>

    <p><strong>For veterinarians:</strong></p>
    <ul>
        <li>Please remain vigilant and report any suspected cases of Foot and Mouth Disease immediately to the relevant authorities.</li>
        <li>Follow strict biosecurity measures in your clinics and when visiting farms to prevent further transmission of the disease.</li>
        <li>Provide guidance and support to farmers on proper containment and management practices.</li>
    </ul>

    <p><strong>For farmers:</strong></p>
    <ul>
        <li>Monitor your livestock closely for any signs of illness, including lameness, blisters, and excessive salivation.</li>
        <li>Restrict movement of animals within and outside your farm premises to prevent the spread of the disease.</li>
        <li>Implement rigorous biosecurity protocols, such as disinfection of equipment, vehicles, and personnel.</li>
    </ul>

    <p>Collaboration and communication are paramount during this critical time. Let us work together swiftly and efficiently to contain this outbreak and safeguard the health and well-being of our livestock and agricultural industry.</p>

    <p>Please do not hesitate to reach out if you require any assistance or have further questions. We will provide updates as the situation develops.</p>

    <p>Thank you for your cooperation and commitment to the health of our community.</p>

    <p>Best regards,<br>Foot and Mouth Disease Detection Organization</p>
</body>
</html>

'''
def send_html_email(sender_email, sender_password, receiver_email, subject, body):
    # Set up the SMTP server
    server = smtplib.SMTP('smtp-relay.brevo.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Compose the email
    message = MIMEText(body, 'html')
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Send the email
    server.send_message(message)
    server.quit()

if  "user_mails" not  in st.session_state:
    st.session_state.user_mails  = ["andrewmodiny21@gmail.com","josekomma@gmail.com", "wambugukinyua125@gmail.com"]
    
def prediction() : 

    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
    bb_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")

    model = load_model('fmd_detection_model.h5')

    images = st.sidebar.file_uploader('Upload the Image' , type = ['jpg' , 'jpeg' , 'png' , 'webp'] , accept_multiple_files = True)
    if  images == []:
        st.components.v1.html(open('no_uploaded.html').read(), height=1000)
    if images : 

        for image_ in images :

            with open('Uploaded_file.jpg' , 'wb') as img : img.write(image_.getbuffer())
            
            label = get_label(model  , bb_model , processor)

            if label == 0 :
                with st.container(border =True):
                    my_grid = grid([0.4,0.6])
                    st.toast("Disease  detected ❗❗❗")
                    with my_grid.container():
                        st.title("Disease detected")
                        with st.container(border=True):
                            st.write('The cattle in the Image have FMD')
                    with my_grid.container():
                        st.image('Uploaded_file.jpg',caption="Foot  and  Mouth detected")
                with st.container(border = True):
                    notify_users = st.button("Notify Other  Farmers", type="primary")
                    if  notify_users:
                        with st.spinner("Updating  farmers  and  Veterinary"):
                            for  email_add in st.session_state.user_mails:
                                send_html_email(sender_email, sender_password,  email_add, subject, body)
                            st.toast("All farmers  notified.")
            elif label == 1 : 
                with st.container(border =True):
                    my_grid = grid([0.4,0.6])
                    st.toast("No disease detected")
                    with my_grid.container():
                        st.title("No Disease  detected.")
                        with st.container(border=True):
                            st.write('The cattle in the Image have No FMD')
                    with my_grid.container():
                        st.image('Uploaded_file.jpg',caption="Foot  and  Mouth not detected")
                #st.write('The cattle in the image does not have FMD')
                #st.image('Uploaded_file.jpg')
            else : 
                st.error('The porvided image is not of a cattle')
                st.image('Uploaded_file.jpg')
                
def home() : st.components.v1.html(open('home.html').read(), height=1000)


usernames = {
    'Ayush' : 'Joseph'
}


login_container = st.empty()

lc = login_container.container(border = True)
username = lc.text_input('Username') 
password = lc.text_input('Password')

if username != '' and password != '' : 

    if username in usernames.keys() and password == usernames[username] : 
        
        login_container.empty()
        with st.sidebar:
            option = option_menu("Main Menu", ["Home", 'Predict Photo'], 
            icons=['house', 'robot'], menu_icon="cast", default_index=0)
        if option == 'Predict Photo':
            with st.sidebar:
                email_input = st.text_input("Enter  farmers  emails")
                if  email_input != '':
                    st.session_state.user_mails.append(email_input)
                    with st.container(border = True, height =100):
                        st.table({"Farmers Mails": st.session_state.user_mails})
        if option == 'Home' : home()
        elif option == 'Predict Photo' : prediction()
        

    else : st.write('Invalid Username or Pasword')




