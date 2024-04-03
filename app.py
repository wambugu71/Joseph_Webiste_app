import streamlit as st 
import os 
import zipfile
from streamlit_option_menu import option_menu
from tensorflow.keras.models import load_model


from helper import get_label
from transformers import DetrImageProcessor, DetrForObjectDetection

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
<html>
<body>
Dear Veterinary and Farming Community,

I hope this email finds you well. Unfortunately, I am writing to bring to your attention a matter of utmost importance. It has come to our attention that there is a confirmed outbreak of Foot and Mouth Disease within our region.

Foot and Mouth Disease poses a significant threat to our livestock and agricultural operations. Given its highly contagious nature, it is imperative that we take immediate and decisive action to contain and mitigate the spread of this disease.

For veterinarians:

Please remain vigilant and report any suspected cases of Foot and Mouth Disease immediately to the relevant authorities.
Follow strict biosecurity measures in your clinics and when visiting farms to prevent further transmission of the disease.
Provide guidance and support to farmers on proper containment and management practices.</p>
For farmers:

Monitor your livestock closely for any signs of illness, including lameness, blisters, and excessive salivation.
Restrict movement of animals within and outside your farm premises to prevent the spread of the disease.
Implement rigorous biosecurity protocols, such as disinfection of equipment, vehicles, and personnel.
Collaboration and communication are paramount during this critical time. Let us work together swiftly and efficiently to contain this outbreak and safeguard the health and well-being of our livestock and agricultural industry.

Please do not hesitate to reach out if you require any assistance or have further questions. We will provide updates as the situation develops.

Thank you for your cooperation and commitment to the health of our community.</p>

Best regards,

Foot and  mouth disease  detection org.
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

    if images : 

        for image_ in images :

            with open('Uploaded_file.jpg' , 'wb') as img : img.write(image_.getbuffer())
            
            label = get_label(model  , bb_model , processor)

            if label == 0 : 
                st.write('The cattle in the Image have FMD')
                st.image('Uploaded_file.jpg')
                with st.spinner("Updating  farmers  and  Veterinary"):
                    for  email_add in st.session_state.user_mails:
                        send_html_email(sender_email, sender_password,  email_add, subject, body)
            elif label == 1 : 
                st.write('The cattle in the image does not have FMD')
                st.image('Uploaded_file.jpg')
            else : 
                st.write('The porvided image is not of a cattle')
                st.image('Uploaded_file.jpg')
                
def home() : st.markdown(open('text.txt').read())


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
            option = option_menu("Main Menu", ["Home", 'prediction'], 
            icons=['house', 'gear'], menu_icon="cast", default_index=1)
        if option == 'Prediction' :
            with st.sidebar:
                email_input = st.text_input("Enter  farmers  emails")
                if  email_input != '':
                    st.session_state.user_mails.append(email_input)
                    with st.container(border = True, height =100):
                        st.table({"Farmers Mails": st.session_state.user_mails})
        if option == 'Home' : home()
        elif option == 'Prediction' : prediction()
        

    else : st.write('Invalid Username or Pasword')




