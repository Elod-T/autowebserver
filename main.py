import os
import argparse
from ssl import create_self_signed_cert

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", help="your docker image's name")
parser.add_argument("-a", "--autostart", help="autostart after created")
parser.add_argument("-e", "--export", help="export the image after created")
parser.add_argument("-nc", "--noclean", help="clean the temporary files after successful image creation")

args = parser.parse_args()


def begins_with(str1: str, str2: str):
    if len(str1) > len(str2):
        return False
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            return False
    return True


# get default config files
print("Getting default config files...")
os.system("docker run --rm httpd:2.4 cat /usr/local/apache2/conf/httpd.conf > httpd.conf")
os.system("docker run --rm httpd:2.4 cat /usr/local/apache2/conf/extra/httpd-ssl.conf > httpd-ssl.conf")
print("Default config files successfully gotten!")

# create config for ssl server
print("Creating ssl config...")
with open("httpd.conf", "a") as config:
    config.write("LoadModule socache_shmcb_module modules/mod_socache_shmcb.so\n"
                 "LoadModule ssl_module modules/mod_ssl.so\n"
                 "Include conf/extra/httpd-ssl.conf\n")


# create ssl directory if not exists
if not os.path.isdir("./ssl"):
    os.mkdir("./ssl")

if len(os.listdir("./ssl")) == 0:
    print("No SSL certificates were found, so generating some...")
    create_self_signed_cert("./ssl/dockerizer.pem")
    print("Self signed certificates generated")

certificate, key = os.listdir("./ssl")
sslconf = ""
with open("httpd-ssl.conf", "r") as base:
    line = "."
    lastline = "."
    while True:
        secondlast = lastline
        lastline = line
        line = base.readline()
        if secondlast + lastline + line != "":
            if begins_with("SSLCertificateFile", str(line)):
                sslconf += f"""SSLCertificateFile "/usr/local/apache2/conf/{certificate}"\n"""
            elif begins_with("SSLCertificateKeyFile", str(line)):
                sslconf += f"""SSLCertificateKeyFile "/usr/local/apache2/conf/{key}"\n"""
            else:
                sslconf += line
        else:
            break
with open("httpd-ssl.conf", "w") as base:
    base.write(sslconf)
print("SSL config successfully created!")


with open("Dockerfile", "w") as Dockerfile:
    print("Creating Dockerfile...")
    # create Dockerfile
    Dockerfile.write("FROM httpd:latest\n"
                     "COPY /html /usr/local/apache2/htdocs/\n"
                     "COPY ./httpd.conf /usr/local/apache2/conf/httpd.conf\n"
                     "COPY ./httpd-ssl.conf /usr/local/apache2/conf/extra/httpd-ssl.conf\n"
                     "COPY /ssl/* /usr/local/apache2/conf/")
    print("Dockerfile successfully created!")

print("Building Docker image...")
os.system(f"docker build --tag {args.name}:latest .")
print("Image successfully built!")

if args.autostart:
    print("Starting container...")
    os.system(f"docker run -dit --rm --name {args.name}-webserver -p 2080:80 -p 2443:443 {args.name}")
    print("Container successfully started")

if args.export:
    print("Exporting image...")
    os.system(f"docker save {args.name} -o {args.name}")
    print("Image successfully exported")

if not args.noclean:
    os.system("rm httpd.conf httpd-ssl.conf Dockerfile")
