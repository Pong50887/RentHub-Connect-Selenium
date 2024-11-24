# RentHub-Connect
[![Run unit tests](https://github.com/Pong50887/RentHub-Connect/actions/workflows/run_unittests.yml/badge.svg)](https://github.com/Pong50887/RentHub-Connect/actions/workflows/run_unittests.yml)
[![Style - PEP8 (currently pycodestyle)](https://github.com/Pong50887/RentHub-Connect/actions/workflows/style.yml/badge.svg)](https://github.com/Pong50887/RentHub-Connect/actions/workflows/style.yml)
[![Run tests and upload coverage](https://github.com/Pong50887/RentHub-Connect/actions/workflows/test-coverage.yml/badge.svg)](https://github.com/Pong50887/RentHub-Connect/actions/workflows/test-coverage.yml)

RentHub-Connect is an application designed to streamline apartment management by integrating booking and payments. 

## Installation
### 1. Clone the repository
Run this in your terminal
```
git clone https://github.com/Pong50887/RentHub-Connect
```
### 2. Navigate to the project directory
```commandline
cd RentHub-Connect
```
### 3. Create a virtual environment
```commandline
python -m venv myenv
```
### 4. Activate the Virtual environment
For Mac/Linux
```commandline
source myenv/bin/activate
```
For Windows
```commandline
.\myenv\Scripts\activate
```
### 5. Install requirements
```
pip install -r requirements.txt
```
### 6. Create your own .env file
In the `sample.env` file, we have provided everything necessary to run the file,
So you can duplicate and rename it to `.env`
#### To create a .env file in terminal
For Mac/Linux
```commandline
cp sample.env .env
```
For windows
```commandline
copy sample.env .env
```

You'll have to create your own neon.tech Postgre database and Amazon S3 to connect with the application <br>
Follow these tutorial, you only have to get values for your .env <br>
[neon.tech Postgre database](https://www.youtube.com/watch?v=kvIK2NpuF2I) <br>
[Amazon S3 tutorial](https://www.youtube.com/watch?v=JQVQcNN0cXE) <br>


### 7. Migrate
```commandline
python manage.py migrate
```

### 8. Run tests
```commandline
python manage.py test
```

### 9. Load data
Media files 
First, download awscli
Windows
```commandline
choco install awscli
```
Mac/Linux
```commandline
brew install awscli
```
log in to your amazon cli
```
aws configure
```
input your aws configuration data

If the aws configuration data is correct, then you'd be able to load media/ into S3 with
```commandline
aws s3 sync media/ s3://<your-bucket-name> --region <your-region-name>

```

Relational files
For Windows
```commandline
for %f in (data\*.json) do python manage.py loaddata "%f"
```
For Mac/Linux
```commandline
for file in data/*.json; do
    python manage.py loaddata $file
done
```
if you ran into loaddata errors, you simply rerun those commands again until no error reports appears

## Running the Application
## 1. After you've finished the Installation Tutorial
you can run the application; run this in your terminal from the project directory
```commandline
python manage.py runserver
```
if static files did not load properly, quit previous (CTRL+C) and use this instead
```commandline
python manage.py runserver --insecure
```

## 2. Use your web browser of choice
type this in your web browser's URL bar
```url
localhost:8000
```
or
```url
127.0.0.1:8000
```
### And you should be redirected to the renthub home page
<img width="1440" alt="Screenshot 2567-11-23 at 21 45 27" src="https://github.com/user-attachments/assets/93eaa32c-bda3-479f-a916-51119e651072">

**!Caution** Some web browser may block the application due to security concerns (like Safari) <br>
Try Google Chrome or Brave.

## 3. Saving data
Your data are saved to cloud database (neon.tech Postgres, Amazon S3) up-to-date in real-time
But if you want to save your questions and choices locally
To save your data
Windows
```commandline
python manage.py dumpdata auth.user --indent 4 > data\users.json
```
Mac/Linux
- users
```commandline
python3 manage.py dumpdata auth.user --indent 4 > data/users.json
```

- app models
Windows
```commandline
for %model in (user, announcement, feature, maintenancerequest, notification, propertyowner, rental, rentalpayment, renter, room, roomimage, roomtype, transaction) do (
    python manage.py dumpdata <yourappname>.%model --indent 4 > data\%model%.json
)
```
Mac/Linux
```commandline
for model in user announcement feature maintenancerequest notification propertyowner rental rentalpayment renter room roomimage roomtype transaction; do
    python3 manage.py dumpdata <yourappname>.$model --indent 4 > data/${model}.json
done
```

To save your media files
First, download awscli
Windows
```commandline
choco install awscli
```
Mac/Linux
```commandline
brew install awscli
```
log in to your amazon cli
```
aws configure
```
input your aws configuration data

If the aws configuration data is correct, then you'd be able to load media into media/ with
```commandline
aws s3 sync s3://<your-bucket-name> --region <your-region-name> media/  
```

## 4. Terminate the running application
`Ctrl+C` to stop the running web application.
If you've accidentally pressed `Ctrl+Z` and can't run the application again,
follow these instructions
1. Type this in your terminal
For Mac/Linux <br>
**sudo is added to execute the command with superuser(root) privileges**
```commandline
sudo lsof -i :8000
//The second column of the output is the <PID>
```
Then replace <PID> in this code below and run,
```commandline
sudo kill <PID>
//or
sudo kill -9 <PID>
```
or 

Mac
Searching the PID in your Activity Moniter, right click, and press Quit.

For Windows <br>
```commandline
netstat -ano | findstr :8000
//The last column is the <PID>
```
Then replace <PID> in this code below and run,
```commandline
taskkill /PID <PID> /F
```

## 5. Exit virtual environment
run this in your virtual environment
```commandline
deactivate
```

# Existing demo users and passwords <br>
## Admin
|    Username     |    password     |
|:---------------:|:---------------:|
|     rhadmin     |   renthub1234   |

## Property
|    Username     |    password     |
|:---------------:|:---------------:|
|    renthub1     |    owner123     |

## Renters
|    Username     |    password     |
|:---------------:|:---------------:|
|      demo1      |    hackme11     |
|      demo2      |    hackme22     |
|      demo3      |    hackme33     |
|      demo4      |    hackme44     |
|      demo5      |    hackme55     |


## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](https://docs.google.com/document/d/1Wsx3GNd7tnee5MSvxD7LutaDATKzdYSilZCzCAl7u4g)
- [Requirements](../../wiki/Requirements)
- [Project Development Plan](../../wiki/Project-Development-Plan)
- [Domain Model](../../wiki/Domain-Model)
- [Task Board](https://github.com/users/Pong50887/projects/3/views/1)

## Iteration Plans
- [Iteration 1](../../wiki/Iteration-1-Plan)
- [Iteration 2](../../wiki/Iteration-2-Plan)
- [Iteration 3](../../wiki/Iteration-3-Plan)
- [Iteration 4](../../wiki/Iteration-4-Plan)
- [Iteration 5](../../wiki/Iteration-5-Plan)
- [Iteration 6](../../wiki/Iteration-6-Plan)
- [Iteration 7](../../wiki/Iteration-7-Plan)
