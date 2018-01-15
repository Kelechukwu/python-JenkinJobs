import jenkins

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()


def initializeDb():
    engine = create_engine('sqlite:///jenkins.db', echo=False)
    session = sessionmaker(bind=engine)()
    Base.metadata.create_all(engine)
    return session

#Database Model
class Job(Base):
    __tablename__ = 'Jobs'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    timeStamp = Column(DateTime)
    result = Column(String)

    def __init__(self,name,timeStamp,result):
        self.name = name
        self.timeStamp = timeStamp
        self.result = result




def connect(url,username,password):
    return jenkins.Jenkins(url,username=username, password=password)

def getJobs(server):
    return server.get_jobs()


url = 'http://localhost:8080'

print("Jenkins URL is set to %s" % url)
username = raw_input('Enter username: ')
password = raw_input('Enter password: ')


server = connect(url, username, password)


jobs = getJobs(server)

session = initializeDb()

for j in jobs:
    jobName = j['name']  # get job name
    # print jobName
    #astJobId = getLastJobId(session, jobName)  # get last locally stored job of this name
    lastBuildNumber = server.get_job_info(jobName)['lastBuild']['number']
    lastBuildDetails = server.get_build_info(jobName, lastBuildNumber)
    lastBuildResult = lastBuildDetails['result']
    lastBuildTimestamp = datetime.datetime.fromtimestamp(long(lastBuildDetails['timestamp']) * 0.001)
    session.add(Job(name=jobName,timeStamp=lastBuildTimestamp,result=lastBuildResult))
    session.commit()

print "done "