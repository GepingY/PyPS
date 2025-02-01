import struct

disk_path = input("DiskPath: ")

with open(disk_path, 'rb') as disk:
    # Read the first 512 bytes
    rawB = disk.read(512)
rawH = rawB.hex()

def type_check(B):
    partition_types = [
    ['00', 'Empty or Unused'],
    ['01', 'FAT12'],
    ['02', 'XENIX root'],
    ['03', 'XENIX usr'],
    ['04', 'FAT16 (Small)'],
    ['05', 'Extended Partition'],
    ['06', 'FAT16'],
    ['07', 'NTFS / HPFS / exFAT'],
    ['08', 'AIX bootable'],
    ['09', 'AIX data'],
    ['0A', 'OS/2 Boot Manager'],
    ['0B', 'FAT32 (CHS)'],
    ['0C', 'FAT32 (LBA)'],
    ['0E', 'FAT16 (LBA)'],
    ['0F', 'Extended Partition (LBA)'],
    ['10', 'OPUS'],
    ['11', 'Hidden FAT12'],
    ['12', 'Compaq diagnostcs'],
    ['14', 'FAT16 (LBA)'],
    ['16', 'Hidden FAT16'],
    ['17', 'Hidden NTFS'],
    ['1B', 'Hidden FAT32'],
    ['1C', 'Hidden FAT32 (LBA)'],
    ['1E', 'Hidden FAT16 (LBA)'],
    ['24', 'NEC DOS'],
    ['39', 'Plan 9'],
    ['3C', 'PartitionMagic recovery'],
    ['40', 'Venix 80286'],
    ['41', 'Linux/MINIX'],
    ['42', 'Linux Swap'],
    ['43', 'Linux Ext2/Ext3 (Old format)'],
    ['44', 'Linux Ext2/Ext3 (New format)'],
    ['83', 'Linux ext FS'],
    ['84', 'Linux swap / Solaris'],
    ['8E', 'Linux LVM'],
    ['93', 'Amoeba'],
    ['A0', 'IBM Thinkpad hidden'],
    ['A5', 'FreeBSD'],
    ['A6', 'OpenBSD'],
    ['A8', 'Mac OS X'],
    ['A9', 'NetBSD'],
    ['AF', 'Mac OS X HFS+'],
    ['B7', 'BSDI'],
    ['B8', 'Boot Manager'],
    ['BE', 'Solaris Boot Partition'],
    ['BF', 'Solaris / OpenIndiana'],
    ['C0', 'NTFS Boot Partition'],
    ['C1', 'FreeBSD boot'],
    ['C4', 'TrueCrypt volume'],
    ['C7', 'Windows 7 recovery'],
    ['D1', 'OpenBSD bootstrap'],
    ['D3', 'GParted'],
    ['D5', 'FreeBSD UFS2'],
    ['D6', 'Solaris (x86) partition'],
    ['D7', 'OpenBSD partition'],
    ['E1', 'Linux RAID'],
    ['E2', 'Linux LVM2'],
    ['E3', 'Linux EVMS'],
    ['E4', 'MS-DOS 6.0'],
    ['E5', 'OpenDOS'],
    ['E6', 'OS/2 Boot Manager'],
    ['E7', 'Non-OS/2 Boot Manager'],
    ['EB', 'FAT16 (LBA) (exFAT)'],
    ['EC', 'Windows 98 SE'],
    ['EE', 'GPT Protective'],
    ['EF', 'EFI System Partition'],
    ['F0', 'Microsoft Reserved'],
    ['F2', 'Linux Swap (used by newer Linux versions)'],
    ['F4', 'Microsoft Windows recovery partition'],
    ['F6', 'HPFS/NTFS'],
    ['F7', 'HPFS/NTFS (Boot)'],
    ['F8', 'OEM proprietary'],
    ['F9', 'BSD']
    ]
    for i in range (0, len(partition_types)):
        if B == partition_types[i][0]:
            return partition_types[i][1]
    return "Unknow"


def partition(raw):
    if raw == "00000000000000000000000000000000":
        return "Empty"
    elif len(raw) != 32:
        print("UnExpected PartitionTable Length")
        exit()

    if int(raw[:2]) == 80:
        bootable = "not bootable"
    elif int(raw[:2]) == 00:
        bootable = "not bootable"
    else:
        print("UnExpected PartitionTable Header: ", raw[:2])
        exit()
    Cylinder = raw[2:4]
    Head = raw[4:6]
    Sector = raw[6:8]
    Type_B = raw[8:10]
    Type = type_check(Type_B)
    Cylinder2 = raw[10:12]
    Head2 = raw[12:14]
    Sector2 = raw[14:16]
    FirstSector = struct.unpack('<I', bytes.fromhex(raw[16:24]))[0]
    TotalSector = struct.unpack('<I', bytes.fromhex(raw[24:32]))[0]
    LastSector = FirstSector + TotalSector
    return [Cylinder, Head, Sector, Type_B, Type, Cylinder2, Head2, Sector2, FirstSector, TotalSector, LastSector]

boot_code = rawH[:880]
DiskSig = rawH[880:892]
PartitionTable = rawH[892:1020]
Signature = rawH[-4:]
p1 = PartitionTable[:32]
p2 = PartitionTable[32:64]
p3 = PartitionTable[64:96]
p4 = PartitionTable[-32:]

print("Raw MBR Bytes in Hex *************************")
print("boot_code:", boot_code)
print("DiskSignature:", DiskSig)
print("Partition1:", p1)
print("Partition2:", p2)
print("Partition3:", p3)
print("Partition4:", p4)
print("MbrSignature:", Signature)
print("**********************************************")
part1 = partition(p1)
part2 = partition(p2)
part3 = partition(p3)
part4 = partition(p4)
if type(part1) == list:
    print("Partition 1 Data")
    print("Cylinder:", part1[0])
    print("Head:", part1[1])
    print("Sector:", part1[2])
    print("Partition type:", part1[3], part1[4])
    print("End Cylinder:", part1[5])
    print("End Head:", part1[6])
    print("End Sector:", part1[7])
    print("FirstSector:", part1[8])
    print("TotalSector:", part1[9])
    print("LastSector:", part1[10])
else:
    print(part1)

print("**********************************************")

if type(part2) == list:
    print("Partition 2 Data")
    print("Cylinder:", part2[0])
    print("Head:", part2[1])
    print("Sector:", part2[2])
    print("Partition type:", part2[3], part2[4])
    print("End Cylinder:", part2[5])
    print("End Head:", part2[6])
    print("End Sector:", part2[7])
    print("FirstSector:", part2[8])
    print("TotalSector:", part2[9])
    print("LastSector:", part2[10])
else:
    print(part2)

print("**********************************************")

if type(part3) == list:
    print("Partition 3 Data")
    print("Cylinder:", part3[0])
    print("Head:", part3[1])
    print("Sector:", part3[2])
    print("Partition type:", part3[3], part3[4])
    print("End Cylinder:", part3[5])
    print("End Head:", part3[6])
    print("End Sector:", part3[7])
    print("FirstSector:", part3[8])
    print("TotalSector:", part3[9])
    print("LastSector:", part3[10])
else:
    print(part3)

print("**********************************************")

if type(part4) == list:
    print("Partition 4 Data")
    print("Cylinder:", part4[0])
    print("Head:", part4[1])
    print("Sector:", part4[2])
    print("Partition type:", part4[3], part4[4])
    print("End Cylinder:", part4[5])
    print("End Head:", part4[6])
    print("End Sector:", part4[7])
    print("FirstSector:", part4[8])
    print("TotalSector:", part4[9])
    print("LastSector:", part4[10])
else:
    print(part4)