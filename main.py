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

itemKeys = ['system.cpu.util', 'vm.memory.util', 'vfs.fs.size']

for index, priority in enumerate(dataInfo):
    data = []

    hosts = zbxInstance.getHosts(priority['id'])

    excelFile = getDatasheet("./archives/", f"{dataInfo[index]['name']} - {getDateInfo.nameMonth()}.xlsx")
    excelFile.addSheet(getDateInfo.dateFormated())
    excelFile.addRow(['HOSTNAME', 'CPU USAGE', 'MEMORY USAGE', 'DISK 0 USAGE', 'DISK 1 USAGE', 'DISK 2 USAGE', 'DISK 3 USAGE', 'DISK 4 USAGE', 'DISK 5 USAGE', 'DISK 6 USAGE', 'DISK 7 USAGE'])

    excelFile.style.font({
        "name": "Calibri Light",
        "bold": True, 
        "color": "FFFFFF",
        "size": 24
    })

    for host in hosts:
        dataPerHost = []
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
        excelFile.addRow(dataPerHost, styleFill={
            "setScaleColor": [
                {
                    "name": "Normal",
                    "startFilter": 0,
                    "endFilter": 35,
                    "font": {
                        "size": 12,
                        "bold": True,
                        "color": '0080FF'
                    },
                    "fill": {
                        "start_color": "CCE5FF",
                        "end_color": "CCE5FF",
                        "fill_type": "solid"
                    }
                },
                {
                    "name": "Atention",
                    "startFilter": 35,
                    "endFilter": 65,
                    "font": {
                        "size": 12,
                        "bold": True,
                        "color": 'D4D413'
                    },
                    "fill": {
                        "start_color": "FFFFCC",
                        "end_color": "FFFFCC",
                        "fill_type": "solid"
                    }
                },
                {
                    "name": "High",
                    "startFilter": 65,
                    "endFilter": 85,
                    "font": {
                        "size": 12,
                        "bold": True,
                        "color": 'FF8000'
                    },
                    "fill": {
                        "start_color": "FFE5CC",
                        "end_color": "FFE5CC",
                        "fill_type": "solid"
                    }
                },
                {
                    "name": "Desaster",
                    "startFilter": 85,
                    "endFilter": 101,
                    "font": {
                        "size": 12,
                        "bold": True,
                        "color": 'FF0000'
                    },
                    "fill": {
                        "start_color": "FFCCCC",
                        "end_color": "FFCCCC",
                        "fill_type": "solid"
                    }
                }
            ]
        })
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

                nameFile = f"{dataInfo[index]['name']} - {getDateInfo.nameMonth()}.xlsx"
                uploadFile = open(rf'./archives/{nameFile}', 'rb')
                ftp.storbinary(rf'STOR {nameFile}', uploadFile)
                uploadFile.close()
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)