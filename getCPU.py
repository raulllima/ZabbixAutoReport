from functions.getDateInfo import getDateInfo
from functions.getDataZabbix import getDataZabbix
from functions.getDatasheet import getDatasheet
import re, ftplib
from os import environ as envs
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
ftp = ftplib.FTP()

dataInfo = [
    {
        "id":"33",
        "name":"Prioridade 1",
    },
    {
        "id":"34",
        "name":"Prioridade 2",
    },
]

zbxInstance = getDataZabbix(envs.get('ZABBIXHost'), envs.get('ZABBIXUser'), envs.get('ZABBIXPass'))

itemKeys = ['system.cpu.util']
for index, priority in enumerate(dataInfo):
    data = []
    nameFile = f"CPU Usage {dataInfo[index]['name']}.xlsx"

    hosts = zbxInstance.getHosts(priority['id'])

    excelFile = getDatasheet("/root/producao/vmware/archives/", nameFile)
    
    if excelFile.addSheet("CPU Usage"):
        excelFile.addRow(["Data Coleta","Hora Coleta","IP","Hostname","CPU Usage"], styleFill={
            "setHeadScaleColor": [
                {
                    "font": {
                        "size": 12,
                        "bold": True,
                        "color": 'FFFFFF'
                    },
                    "fill": {
                        "start_color": "434343",
                        "end_color": "434343",
                        "fill_type": "solid"
                    }
                }
            ]
        })

    excelFile.style.font({
        "name": "Calibri Light",
        "bold": True, 
        "color": "FFFFFF",
        "size": 24
    })

    for host in hosts:
        dataPerHost = []
        dataPerHost.append(getDateInfo.dateFormated())
        dataPerHost.append(getDateInfo.getHour())
        dataPerHost.append(host['interfaces'][0]['ip'])
        dataPerHost.append(host['host'])

        for itemKey in itemKeys:
            items = zbxInstance.getItems(host['hostid'], itemKey)
            
            for item in items:
                history = zbxInstance.getHistory(item['itemid'], itemKey)
                
                if (': Space utilization' in item['name']):
                    nameDisk = item['name'].replace(': Space utilization', '')

                    if (nameDisk == "/"):
                        nameDisk = "/:"
                        dataPerHost.append(f"{nameDisk} - {history[0]}")
                    
                    else:
                        match = re.search(r'\((\w:)\)', nameDisk)
                        if match:
                            disk_name = match.group(1)

                        dataPerHost.append(f"{disk_name} - {history[0]}")
                else:
                    dataPerHost.append(f"{history[0]}")

        excelFile.addRow(dataPerHost)
    excelFile.saveFile()

    try:
        ftp.connect(envs.get('FTPHost'), 21)

        if ftp.login(envs.get('FTPUser'), envs.get('FTPPass')):
            try:
                if getDateInfo.getYear() not in ftp.nlst():
                    ftp.mkd(getDateInfo.getYear())
                
                ftp.cwd(getDateInfo.getYear())

                if getDateInfo.nameMonth() not in ftp.nlst():
                    ftp.mkd(getDateInfo.nameMonth())
                
                ftp.cwd(getDateInfo.nameMonth())

                uploadFile = open(rf'./archives/{nameFile}', 'rb')
                ftp.storbinary(rf'STOR {nameFile}', uploadFile)
                uploadFile.close()
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)