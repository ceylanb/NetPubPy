# NetPubPy

NetPubPy is a script that makes easier to publish .NET projects to FTP server. Don't make a lot of effort to transfer your files and folders to FTP server! Make your configuration at once then use it again and again! By the way, you can publish one more projects at the same time. When you run the script, NetPubPy uploads app_offline.htm to FTP Server. Therefore while the publishing process continues, maintenance screen appears to web site visitors.



**Caution:** NetPubPy removes files beginning with 'App_' in 'Bin' folder at the FTP server side then uploads new ones!

 

## Getting Started

### Prerequisites

What things you need to install: 

 * Python 3 
 * Python Colorama module 
 * Python FTPUtil module

### Installing

You have to have Python 3 to install other modules as mentioned in Prerequisites section.

Command for installation of FTPUtil:
```
python -m pip install ftputil
```

Command for installation of Colorama:
```
python -m pip install colorama
```

## Running the tests

To test the script, you need to set some parameters in **config.json** file.

```
{
  "ftps": [
    -------------- Beginning for Project 1 -------------------------
    {
      "active": "1",
      "force":"0",
      "local_path": "/Published/Project/Folder/",
      "ftp_path": "/ftp/target/folder/",
      "ftp_host": "ftp_host",
      "ftp_user": "ftp_user",
      "ftp_pass": "ftp_pass",
      "excepted_dirs": [
        "excepted_dir_1",
        "excepted_dir_3",
        "excepted_dir_2/excepted_dir_3"  
      ],
      "excepted_files": [
      	"excepted_file_1",
      	"excepted_file_2"
      ],
      "upload_files": [
        "upload_file_1",
        "excepted_dir_2/upload_file_2"
      ]
    },
    -------------- Ending for Project 1 ----------------------------
    -------------- Beginning for Project 2 -------------------------
    {
      "active": "0",
      "force":"0",
      "local_path": "/Published/Project/Folder2/",
      "ftp_path": "/ftp2/taget/foder/",
      "ftp_host": "ftp_host_2",
      "ftp_user": "ftp_user_2",
      "ftp_pass": "ftp_pass_2",
      "excepted_dirs": [ 
      ],
      "excepted_files": [
      ],
      "upload_files": [
      ]      
    }
    -------------- Ending for Project 2 ----------------------------        
  ]
}
```


After the configuration run this command:
```
python publish.py
```

## Authors

* [**Ceylan Bozogullarindan**](https://www.linkedin.com/in/ceylan-bozoğullarından-05327a102/) 

