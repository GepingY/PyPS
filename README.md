# PyPartitionSchemes
This program is under development to read most partitioning schemes, such as MBR, GPT, etc. <br />
## Current available function: 
`interpret MBR (Master Boot Record) and it's deviate data such as partition table and type etc......`
`interpret GPT (GUID Partition Table and it's deviate data such as partition table and type etc......)`
## How to use
This program is purely written in `Python 3`, no external libraries are required. <br />
Build in Library `struct` is used to convert edian, don't worry about it<br />

It has been tested on `Windows 11` and `Ubuntu 24.04 Noble`, and it is supposed to work on `macOS` as well, although it has never been tested on `macOS`. <br />
To use, simply run it with `Python`, e.g. <br />
On `Windows` command line, run `python Main.py` <br />
On `Linux` terminal, run `python3 Main.py` <br />
<br />
You will then be asked to input the path to the disk. For Windows, the path should be something like `\\.\PHYSICALDRIVE1`. To find the list of disk paths on Windows, run `wmic diskdrive list brief`; for Linux, the path should look like `/dev/sdX`, where X is a letter from a to b, such as `/dev/sda`. Find the list of disk paths on Linux by using `lsblk`. **DO NOT** use the path to a partition instead of the path to disk on linux, there shouldn't be a number behind the path, e.g. you should use something like `/dev/sda` instead of `/dev/sda1` <br />

Then Enter 1 to parse GPT, or enter 2 to parse MBR <br />

After that, the interpreted data will br printed out in the command line <br />
<br />
Note: CHS data is given in hex, sector numbers are given in decimal

## Example Output
```
PS C:\Users\YourUserName\Documents\Script> python MBR.py
DiskPath: \\.\PHYSICALDRIVE1
Raw MBR Bytes in Hex *************************
boot_code: fab800108ed0bc00b0b800008ed88ec0fbbe007cbf0006b90002f3a4ea21060000bebe073804750b83c61081fefe0775f3eb16b402b001bb007cb2808a74018b4c02cd13ea007c0000ebfe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
DiskSig: 69d0e8300000
Partition1: 0020210083fec2ff000800000060f624
Partition2: 00fec2ff07fec2ff0068f62400684552
Partition3: 00000000000000000000000000000000
Partition4: 00000000000000000000000000000000
Signature: 55aa
**********************************************
Partition 1 Data
Cylinder: 20
Head: 21
Sector: 00
Partition type: 83 Linux ext FS
End Cylinder: fe
End Head: c2
End Sector: ff
FirstSector: 2048
TotalSector: 620126208
LastSector: 620128256
**********************************************
Partition 2 Data
Cylinder: fe
Head: c2
Sector: ff
Partition type: 07 NTFS / HPFS / exFAT
End Cylinder: fe
End Head: c2
End Sector: ff
FirstSector: 620128256
TotalSector: 1380280320
LastSector: 2000408576
**********************************************
Empty
**********************************************
Empty
```

# In Development Function
`MBR to GPT without data loss`

# Keywords
MBR; MBR dump; Windows MBR dump; MBR structure; Python MBR Reader; Partition Scheme Dump; GPT; GUID Partition Table
