import struct

disk_path = input("DiskPath: ")
choice = int(input("input 1 for GPT and 2 for MBR: "))

def GPT(disk_path):
    print("***********************************************")
    with open(disk_path, 'rb') as disk:
        disk.seek(512)
        raw = disk.read(512).hex()
    disk.close()

    def bytes_le_to_guid(hex_str):
        # Convert hex string to bytes
        b = bytes.fromhex(hex_str)

        # Extract fields and swap endianness where needed
        part1 = b[:4][::-1].hex()  # Little-endian (4 bytes)
        part2 = b[4:6][::-1].hex()  # Little-endian (2 bytes)
        part3 = b[6:8][::-1].hex()  # Little-endian (2 bytes)
        part4 = b[8:10].hex()       # Big-endian (2 bytes)
        part5 = b[10:].hex()        # Big-endian (6 bytes)

        # Format as standard GUID
        return f"{part1}-{part2}-{part3}-{part4}-{part5}"

    def find_partition_type(guid):
        partition_types = [
            {"GUID": "00000000-0000-0000-0000-000000000000", "Description": "Unused entry"},
            {"GUID": "024DEE41-33E7-11D3-9D69-0008C781F39F", "Description": "MBR partition scheme"},
            {"GUID": "C12A7328-F81F-11D2-BA4B-00A0C93EC93B", "Description": "EFI System partition"},
            {"GUID": "21686148-6449-6E6F-744E-656564454649", "Description": "BIOS boot partition"},
            {"GUID": "D3BFE2DE-3DAF-11DF-BA40-E3A556D89593", "Description": "Intel Fast Flash (iFFS) partition (for Intel Rapid Start technology)"},
            {"GUID": "F4019732-066E-4E12-8273-346C5641494F", "Description": "Sony boot partition"},
            {"GUID": "BFBFAFE7-A34F-448A-9A5B-6213EB736C22", "Description": "Lenovo boot partition"},
            {"GUID": "E3C9E316-0B5C-4DB8-817D-F92DF00215AE", "Description": "Microsoft Reserved Partition (MSR)"},
            {"GUID": "EBD0A0A2-B9E5-4433-87C0-68B6B72699C7", "Description": "Basic data partition"},
            {"GUID": "5808C8AA-7E8F-42E0-85D2-E1E90434CFB3", "Description": "Logical Disk Manager (LDM) metadata partition"},
            {"GUID": "AF9B60A0-1431-4F62-BC68-3311714A69AD", "Description": "Windows Storage Spaces partition"},
            {"GUID": "0FC63DAF-8483-4772-8E79-3D69D8477DE4", "Description": "Linux filesystem data"},
            {"GUID": "A19D880F-05FC-4D3B-A006-743F0F84911E", "Description": "Linux RAID partition"},
            {"GUID": "0657FD6D-A4AB-43C4-84E5-0933C84B4F4F", "Description": "Linux swap partition"},
            {"GUID": "E6D6D379-F507-44C2-A23C-238F2A3DF928", "Description": "Linux Logical Volume Manager (LVM) partition"},
            {"GUID": "933AC7E1-2EB4-4F13-B844-0E14E2AEF915", "Description": "Linux /home partition"},
            {"GUID": "3B8F8425-20E0-4F3B-907F-1A25A76F98E8", "Description": "Linux /srv (server data) partition"},
            {"GUID": "7FFEC5C9-2D00-49B7-8941-3EA10A5586B7", "Description": "Linux plain dm-crypt partition"},
            {"GUID": "CA7D7CCB-63ED-4C53-861C-1742536059CC", "Description": "Linux LUKS partition"},
            {"GUID": "8DA63339-0007-60C0-C436-083AC8230908", "Description": "Linux reserved"},
            {"GUID": "A2A0D0EB-E5B9-3344-87C0-68B6B72699C7", "Description": "FreeBSD disklabel"},
            {"GUID": "516E7CB4-6ECF-11D6-8FF8-00022D09712B", "Description": "FreeBSD boot partition"},
            {"GUID": "516E7CB5-6ECF-11D6-8FF8-00022D09712B", "Description": "FreeBSD data partition"},
            {"GUID": "516E7CB6-6ECF-11D6-8FF8-00022D09712B", "Description": "FreeBSD swap partition"},
            {"GUID": "516E7CB8-6ECF-11D6-8FF8-00022D09712B", "Description": "FreeBSD UFS partition"},
            {"GUID": "516E7CB7-6ECF-11D6-8FF8-00022D09712B", "Description": "FreeBSD ZFS partition"},
            {"GUID": "516E7CBA-6ECF-11D6-8FF8-00022D09712B", "Description": "FreeBSD Vinum volume manager partition"},
            {"GUID": "48465300-0000-11AA-AA11-00306543ECAC", "Description": "Apple HFS+ partition"},
            {"GUID": "55465300-0000-11AA-AA11-00306543ECAC", "Description": "Apple UFS partition"},
            {"GUID": "6A898CC3-1DD2-11B2-99A6-080020736631", "Description": "Apple ZFS partition"},
            {"GUID": "52414944-0000-11AA-AA11-00306543ECAC", "Description": "Apple RAID partition"},
            {"GUID": "52414944-5F4F-11AA-AA11-00306543ECAC", "Description": "Apple RAID offline partition"},
            {"GUID": "426F6F74-0000-11AA-AA11-00306543ECAC", "Description": "Apple Boot partition"},
            {"GUID": "4C616265-6C00-11AA-AA11-00306543ECAC", "Description": "Apple Label partition"},
            {"GUID": "5265636F-7665-11AA-AA11-00306543ECAC", "Description": "Apple TV Recovery partition"},
            {"GUID": "53746F72-6167-11AA-AA11-00306543ECAC", "Description": "Apple Core Storage (i.e. Lion FileVault) partition"},
            {"GUID": "6A82CB45-1DD2-11B2-99A6-080020736631", "Description": "Solaris boot partition"},
            {"GUID": "6A85CF4D-1DD2-11B2-99A6-080020736631", "Description": "Solaris root partition"},
            {"GUID": "6A87C46F-1DD2-11B2-99A6-080020736631", "Description": "Solaris /usr partition"},
            {"GUID": "6A8B642B-1DD2-11B2-99A6-080020736631", "Description": "Solaris swap partition"},
            {"GUID": "6A8D2AC7-1DD2-11B2-99A6-080020736631", "Description": "Solaris backup partition"},
            {"GUID": "6A898CC3-1DD2-11B2-99A6-080020736631", "Description": "Solaris /var partition"},
            {"GUID": "6A8EF2E9-1DD2-11B2-99A6-080020736631", "Description": "Solaris /home partition"},
            {"GUID": "6A90BA39-1DD2-11B2-99A6-080020736631", "Description": "Solaris alternate sector"},
            {"GUID": "6A9283A5-1DD2-11B2-99A6-080020736631", "Description": "Solaris reserved partition"},
            {"GUID": "6A945A3B-1DD2-11B2-99A6-080020736631", "Description": "Solaris root pool"},
            {"GUID": "6A9630D1-1DD2-11B2-99A6-080020736631", "Description": "Solaris boot pool"},
            {"GUID": "49F48D32-B10E-11DC-B99B-0019D1879648", "Description": "NetBSD swap partition"},
            {"GUID": "49F48D5A-B10E-11DC-B99B-0019D1879648", "Description": "NetBSD FFS partition"},
            {"GUID": "49F48D82-B10E-11DC-B99B-0019D1879648", "Description": "NetBSD LFS partition"},
            {"GUID": "49F48DAA-B10E-11DC-B99B-0019D1879648", "Description": "NetBSD RAID partition"},
            {"GUID": "49F48DD2-B10E-11DC-B99B-0019D1879648", "Description": "NetBSD Concatenated partition"},
            {"GUID": "2DB519C4-B10F-11DC-B99B-0019D1879648", "Description": "NetBSD encrypted partition"},
            {"GUID": "FE3A2A5D-4F32-41A7-B725-ACCC3285A309", "Description": "VMware VMFS partition"},
            {"GUID": "AA31E02A-400F-11DB-9590-000C2911D1B8", "Description": "VMware reserved partition"},
            {"GUID": "9D275380-40AD-11DB-BF97-000C2911D1B8", "Description": "VMware kcore crash partition"},
            {"GUID": "11D2F81B-FD4F-459B-9ADB-9091ED7E593F", "Description": "XenServer Linux partition"},
            {"GUID": "5B193300-FC78-40CD-8002-E86C45580B47", "Description": "Microsoft Basic Data partition"},
            {"GUID": "0376FF8D-D1A5-11E3-8E7D-001B21B9EADD", "Description": "Ceph OSD partition"},
            {"GUID": "45B0969E-9B03-4F30-B4C6-5EC00CEFF106", "Description": "Ceph disk in creation"},
            {"GUID": "4FBD7E29-9D25-41B8-AFD0-062C0CEFF05D", "Description": "Ceph journal"},
            {"GUID": "89C57F98-2FE5-4DC0-89C1-F3AD0CEFF2BE", "Description": "Ceph crypt"},
            {"GUID": "FB3AABF9-D6F9-46D8-9F9D-D6A4E56C5E36", "Description": "Ceph block"},
            {"GUID": "CAFECAFE-9B03-4F30-B4C6-5EC00CEFF106", "Description": "Ceph block DB"},
            {"GUID": "30D3B3C4-9B03-4F30-B4C6-5EC00CEFF106", "Description": "Ceph block write-ahead log"}
        ]
        for partition in partition_types:
            if partition["GUID"].lower() == guid.lower():  # Case-insensitive comparison
                return partition["Description"]
        return "Unknow: " + guid


    signature = raw[:16]
    signature_ascii = bytearray.fromhex(signature).decode()
    revision = raw[16:24]
    version = str(revision[5:6]) + "." + str(revision[6:8])
    header_size = struct.unpack('<I', bytes.fromhex(raw[24:32]))[0]
    CRC32 = raw[32:40]
    reserved = raw[40:48]
    current_lba = struct.unpack('<II', bytes.fromhex(raw[48:64]))[0]
    backup_lba = struct.unpack('<II', bytes.fromhex(raw[64:80]))[0]
    first_partition = struct.unpack('<II', bytes.fromhex(raw[80:96]))[0]
    last_lba = struct.unpack('<II', bytes.fromhex(raw[96:112]))[0]
    GUID = raw[112:144]
    partition_entry_starting_lba = struct.unpack('<II', bytes.fromhex(raw[144:160]))[0]
    partition_entry_count = struct.unpack('<I', bytes.fromhex(raw[160:168]))[0]
    partition_entry_size = struct.unpack('<I', bytes.fromhex(raw[168:176]))[0]
    partition_array_CRC32 = raw[176:184]

    print("signature:", signature)
    print("signature_ascii:", signature_ascii)
    print("revision:", revision)
    print("version:", version)
    print("header_size:", header_size)
    print("CRC32:", CRC32)
    print("reserved:", reserved)
    print("current_lba:", current_lba)
    print("backup_lba:", backup_lba)
    print("first partition starting LBA:", first_partition)
    print("last lba:", last_lba)
    print("GUID:", GUID)
    print("partition entry starting LBA:", partition_entry_starting_lba)
    print("partition entry count:", partition_entry_count)
    print("partition entry size:", partition_entry_size)
    print("partition array CRC32:", partition_array_CRC32)

    with open(disk_path, 'rb') as disk:
        disk.seek(partition_entry_starting_lba * 512)
        raw2 = disk.read(partition_entry_count * partition_entry_size).hex()
    disk.close()

    def partition_groups(hex_string, partition_entry_size, partition_entry_count):

        expected_length = partition_entry_size * partition_entry_count
        if len(hex_string) != expected_length:
            raise ValueError(f"The hex string must be of length {expected_length} (partition_entry_size * partition_entry_count).")

        groups = [hex_string[i:i+partition_entry_count] for i in range(0, len(hex_string), partition_entry_size)]

        empty_count = sum(1 for group in groups if all(c == '0' for c in group))

        non_empty_groups = [group for group in groups if not all(c == '0' for c in group)]
        
        return empty_count, non_empty_groups


    empty_count, non_empty_groups = partition_groups(raw2, partition_entry_size * 2, partition_entry_count)

    print(f"Empty Partition Entry: {empty_count}")

    #Partition Parse(PP)
    def PP(data):
        PartitionTypeGUID = find_partition_type(bytes_le_to_guid(data[:32]))
        UniquePartitionGUID = data[32:64]
        StartingLBA =  struct.unpack('<II', bytes.fromhex(data[64:80]))[0]
        EndingLBA = struct.unpack('<II', bytes.fromhex(data[80:96]))[0]
        Attributes = data[96:112]
        binary_attri = bin(int(Attributes, 16))[2:].zfill(len(Attributes) * 4)
        if binary_attri[:1] != "0":
            Required_Partition = True
        else:
            Required_Partition = False
        if binary_attri[1:2] != "0":
            No_Block_IO_Protocol = True
        else:
            No_Block_IO_Protocol = False
        if binary_attri[2:3] != "0":
            Legacy_BIOS_Bootable = True
        else:
            Legacy_BIOS_Bootable = False
        PartitionName = data[112:256]
        
        return PartitionTypeGUID, UniquePartitionGUID, StartingLBA, EndingLBA, Attributes, PartitionName, Required_Partition, No_Block_IO_Protocol, Legacy_BIOS_Bootable
    for i in range(0, partition_entry_count - empty_count):
        PartitionTypeGUID, UniquePartitionGUID, StartingLBA, EndingLBA, Attributes, PartitionName, Required_Partition, No_Block_IO_Protocol, Legacy_BIOS_Bootable = PP(non_empty_groups[i])
        print("****************************************")
        print("Partition Number: ",i)
        print("PartitionTypeGUID: ", PartitionTypeGUID)
        print("UniquePartitionGUID: ", UniquePartitionGUID)
        print("StartingLBA: ", StartingLBA)
        print("EndingLBA: ", EndingLBA)
        print(f"Attributes: {Attributes}, Required_Partition={Required_Partition}, No_Block_IO_Protocol={No_Block_IO_Protocol}, Legacy_BIOS_Bootable={Legacy_BIOS_Bootable}")
        print(f"PartitionName: {bytearray.fromhex(PartitionName).decode()}")


def MBR(disk_path):
    print("***********************************************")
    with open(disk_path, 'rb') as disk:
        # Read the first 512 bytes
        rawB = disk.read(512)
        disk.close()
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
        
if choice == 1:
    GPT(disk_path)
elif choice == 2:
    MBR(disk_path)
else:
    print("Either 1 or 2!")