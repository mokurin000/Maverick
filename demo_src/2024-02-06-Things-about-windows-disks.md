---
layout: post
title: Win32 盘符，设备号和硬盘型号
slug: win32-drive-letters-deviceid-harddisk-model
date: 2024-02-06 18:23
status: publish
author: Poly000
categories: 
  - Win32
tags: 
  - Win32
  - Storage_Management
---

## 原发布地址

[原Issue评论](https://github.com/JonMagon/KDiskMark/issues/87#issuecomment-1925784750)，讨论 KDiskMark Windows 支持需要的工作

## 列出设备

### 逻辑设备

[`GetLogicalDrives`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getlogicaldrives) 会返回一组位码，值为1的位的位置加上'A'就是它代表的盘符

```python
from win32api import GetLogicalDrives

# for example, `0b_1100` means there are C:/ and D:/.
def logical_drives():
   bit_mask = GetLogicalDrives()
   for offset in range(26):
      alphabet = chr(ord('A') + offset)
      if (1 << offset) & bit_mask:
          yield alphabet
```

### 卷

#### 使用 Powershell[^0]:

```powershell
Get-Volume
```

#### 使用 `mountvol.exe`

```cmd
mountvol /L
```

#### 使用 [`FindFirstVolumeW`] and [`FindNextVolumeW`]
[`FindFirstVolumeW`]: https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-findfirstvolumew
[`FindNextVolumeW`]: https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-findnextvolumew

```python
from winsys._kernel32 import FindFirstVolume, FindNextVolume
handle, first = FindFirstVolume()
volumes = [first]

while (volume := FindNextVolume(handle)) and isinstance(volume, str):
    volumes.append(volume)

print(volumes)
```

## 获取硬盘型号

### 盘符 -> 硬盘型号

#### 使用 Powershell[^1]

```powershell
Get-Disk (Get-Partition -DriveLetter 'C').DiskNumber | select -Prop FriendlyName
```

### 盘符或任意卷 -> 设备号

#### 使用 Powershell （只支持盘符）

```powershell
(Get-Partition -DriveLetter 'C').DiskNumber
```

#### 使用 [`IOCTL_STORAGE_GET_DEVICE_NUMBER`]
[`IOCTL_STORAGE_GET_DEVICE_NUMBER`]: https://learn.microsoft.com/en-US/windows/win32/api/winioctl/ni-winioctl-ioctl_storage_get_device_number

```c
#include <stdio.h>
#include <Windows.h>
#include <fileapi.h>
#include <winioctl.h>

int get_disk_number_by_drive_letter(char letter) {
    char logical_drive_path[7];
    sprintf(logical_drive_path, "\\\\.\\%c:", letter);
    // '\\?\Volume{<GUID>}' is also applicable to this
    HANDLE hDevice = CreateFileA(logical_drive_path, GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);
    if (hDevice == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "Failed to open device. Error code: %lu\n", GetLastError());
        return -1;
    }

    STORAGE_DEVICE_NUMBER device_number;
    DWORD bytes_returned;
    if (!DeviceIoControl(hDevice, IOCTL_STORAGE_GET_DEVICE_NUMBER, NULL, 0, &device_number, sizeof(device_number), &bytes_returned, NULL)) {
        fprintf(stderr, "IOCTL_STORAGE_GET_DEVICE_NUMBER failed. Error code: %lu\n", GetLastError());
        CloseHandle(hDevice);
        return -1;
    }

    CloseHandle(hDevice);
    return device_number.DeviceNumber;
}
```

### 设备号 -> 硬盘型号

#### 使用 Powershell

```powershell
Get-Disk | select -Prop Number,FriendlyName
```

#### 使用 wmic

```cmd
wmic diskdrive get index,model
```

#### 使用 wmi

```python
from win32com.client import GetObject

def get_diskdrive_info():
    wmi = GetObject(r"winmgmts:\\.\root\cimv2")
    disks = wmi.ExecQuery("SELECT * FROM Win32_DiskDrive")

    disk_info = {disk.Index: disk.Model for disk in disks}
    return disk_info

disk_info = sorted(get_diskdrive_info().items())

for index, model in disk_info:
    print(f"{index}: {model}")
```

Anyway, the most accurate way is to call `smartctl ... X:`

## 其他可能要用到的系统调用

[`QueryDosDeviceW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-querydosdevicew) 可以用来从盘符获取卷编号（也可以用来列出卷，如果传入None），即 \Device\HarddiskVolume*X* 中的 X 。

[`GetDiskFreeSpaceExA`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getdiskfreespaceexa) 可以拿到对调用用户可用的空间（详见配额），总硬盘大小和总可用空间。


```python
from win32file import GetDiskFreeSpaceEx
list(map(lambda size: size / (1024**3), GetDiskFreeSpaceEx("C:")))
# [58.516212463378906, 117.97948837280273, 58.516212463378906]
```

---------

## 尾声

感谢[^2]的 Win32 Paths 解释

[^0]: https://winreg-kb.readthedocs.io/en/latest/sources/system-keys/Mounted-devices.html#notes)
[^1]: https://superuser.com/a/1147305
[^2]: https://chrisdenton.github.io/omnipath/Overview.html