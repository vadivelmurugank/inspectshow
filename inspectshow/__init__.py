# Collect System info
#
#
#   - processes and pmap
#
#   - kernel version
#   - kernel bootline
#   - device nodes
#
#   - kernel modules
#   - kernel config
#
#   - pci list
#   - network interfaces
#
#   - loader and libs
#
#   - hardware info
#        - disk
#        - ram
#

pstree -Aa -st -l
sudo sh -c "perf record -F 99 -ag -p $(pidof switchd)"

sudo sh -c "perf report -n"
sudo sh -c "perf report -n --stdio"

#Flamegraph
# git clone https://github.com/brendangregg/FlameGraph  # or download it from github
 cd FlameGraph
sudo sh -c "perf record -F 99 -ag -- sleep 60"
perf script | ./stackcollapse-perf.pl > out.perf-folded
cat out.perf-folded | ./flamegraph.pl > perf-kernel.svg

# vlibshow
export LD_LIBRARY_PATH=$SDE/install/lib
~/bin/vlibshow ./libbf_switch.so > ~/bin/libbf_switch_symbols.txt


show_host()
{
    echo -e "\n\n Host Info"
    echo -e "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    echo -e "\n\n Hostname"
    echo -e "-----------------------------------------------"
    echo -e "\n\n#$ hostname"
    hostname
    nslookup $(hostname)


    echo -e "\n\n system"
    echo -e "-----------------------------------------------"
    echo -e "\n\n#$ dmidecode -t system\n"
    dmidecode -t system
    echo -e "\n\n #$ dmidecode -t bios \n"
    dmidecode -t bios
    dmidecode -t slot
    dmidecode -t baseboard
    dmidecode -t chassis
}


show_virtual()
{
    echo -e "\n\n Virtual Info"
    echo -e "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    echo -e "\n\n#$ lsmod | grep -i vm \n"
    lsmod | grep -E -i '(vm|vir)'

    echo -e "\n\n#$ virt-what \n"
    virt-what

    echo -e "\n\n#$ virt-host-validate \n"
    virt-host-validate

   
    echo -e "\n\n#$ virsh list --all \n"
    virsh list --all

    echo -e "\n\n#$ virsh iface-list \n"
    virsh iface-list

    echo -e "\n\n#$ virsh nodeinfo \n"
    virsh nodeinfo

    echo -e "\n\n#$ virsh version \n"
    virsh version

    echo -e "\n\n#$ virsh nwfilter-list \n"
    virsh nwfilter-list

    echo -e "\n\n#$ virsh net-list \n"
    virsh net-list


    echo -e "\n\n#$ virsh pool-list \n"
    virsh pool-list

    echo -e "\n\n#$ virsh pool-info default \n"
    virsh pool-info default

    echo -e "\n\n#$ virsh vol-list --details default \n"
    virsh vol-list --details default

    echo -e "\n\n#$ virsh nodememstats \n"
    virsh nodememstats

    echo -e "\n\n#$ virsh sysinfo \n"
    virsh sysinfo

   echo -e "\n\n#$  virsh capabilities \n"
    virsh capabilities 

    echo -e "\n\n#$ virsh nodedev-list \n"
    virsh nodedev-list

}

show_docker()
{

    echo -e "\n\n#$ docker images ls \n"
    docker images ls

    echo -e "\n\n#$ docker network ls \n"
    docker network ls

    echo -e "\n\n#$ docker version \n"
    docker version

    echo -e "\n\n#$ docker volume \n"
    docker volume

    echo -e "\n\n#$ docker info \n"
    docker info
}


show_process()
{

        ## Total number of priorities = 140
        ## Real time priority range(PR or PRI):  0 to 99 
        ## User space priority range: 100 to 139

        ## Nice value range (NI): -20 to 19
        ## PR = 20 + NI
        ## PR = 20 + (-20 to + 19)
        ## PR = 20 + -20  to 20 + 19
        ## PR = 0 to 39 which is same as 100 to 139.  

    echo -e "\n\n Process Info"
    echo -e "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    echo -e "\n\nProcesses and memory"
    echo -e "-----------------------------------------------"
    #echo -e "\n\n#$ ps auxf  | awk '{ printf("%6u MB\t", $6/1024); printf("%-6s \t\t", $1); for(i=11;i<=NF;++i) printf("%s ", $i);printf("\n")}'\n"
    #ps auxf  | awk '{ printf("%6u MB\t", $6/1024); printf("%-6s \t\t", $1); for(i=11;i<=NF;++i) printf("%s ", $i);printf("\n")}'

    # pstree $(pgrep <<process name>. )
    # pstree $(pgrep <<process name>. )
	# -A : Ascii
	# -a : args
	# -h : highlight running process
	# -t : thread names
	# -s : parents
	# -l : don't truncate long lines
	pstree -Aa -h  -st -l


# list all threads
# ps -Tef | grep vfrwd

pids=
for pid in $(ls -1 /proc | grep -E '^[0-9]+')
do
pids="$pids $pid"
Threads=$(awk -F'\t' '/^Threads/ {print $2}' /proc/$pid/status)
if [ XX$Threads != "XX" ] ; then
            if [ -d /proc/$pid/task ] ; then
                pids="$pids $(ls -1 /proc/$pid/task/ | grep -E '^[0-9]+')"
            fi
        fi
    done

    #echo $pids

    printf "========================================================================\n"
    printf "%-10s || %-10s || %10s (%5s) core:%s | vmsize=%s \n" "ThreadGroup" "Parent" "TName" "Tid"  "TCpus" "VmPeak"
    printf "========================================================================\n\n"
    for pid in $pids
    #for pid in "139726"
    do 
        NGid=$(awk -F'\t' '/^Ngid/ {print $2}' /proc/$pid/status)
        TGid=$(awk -F'\t' '/^Tgid/ {print $2}' /proc/$pid/status)
        PPid=$(awk -F'\t' '/^PPid/ {print $2}' /proc/$pid/status)

        VmPeak=$(awk -F'\t' '/^VmPeak/ {print $2}' /proc/$pid/status)
        TName=$(awk -F'\t' '/^Name/ {print $2}' /proc/$pid/status)
        TCpus=$(awk -F'\t' '/^Cpus_allowed_list/ {print $2}' /proc/$pid/status)
        Tid=$(awk -F'\t' '/^Pid/ {print $2}' /proc/$pid/status)
        Threads=$(awk -F'\t' '/^Threads/ {print $2}' /proc/$pid/status)

        NumaGroup=$(awk -F'\t' '/^Name/ {print $2}' /proc/$NGid/status 2> /dev/null)
        ThreadGroup=$(awk -F'\t' '/^Name/ {print $2}' /proc/$TGid/status 2> /dev/null)
        Parent=$(awk -F'\t' '/^Name/ {print $2}' /proc/$PPid/status 2> /dev/null)

        #Thread=$(grep 'Name\|Cpus_allowed_list\|^Pid' /proc/$pid/status | tr -d '\t' | cut -d: -f2 | xargs -L3 | awk '{print $1,$2,$3}')

        #echo -e "${ThreadGroup} -> ${Parent} ->  ${TName} :: ${Tid} : ${TCpus} - ${VmPeak}"
        printf "%-10s -> %-10s -> %10s (%5s) core:%s : vmsize=%s Threads:%s\n" "${ThreadGroup}" "${Parent}" "${TName}" "${Tid}"  "${TCpus}" "${VmPeak}" "${Threads}"
    done


    #ps -p $pid  -L -o pid,tid,cputime,args,psr,pcpu
    #ps -p $pid -L -o uname,pid,psr,pcpu,cputime,pmem,rsz,vsz,tty,s,etime,args


    echo -e "\n\nProcess Shared Memory and Semaphores"
    echo -e "-----------------------------------------------"
    echo -e "\n\n#$ ipcs -u\n"
    ipcs -u --human
    ipcs -pm
        
    echo -e "\n\n#$ ipcs\n"
    ipcs -a

    echo -e "\n\n#$ lsipc\n"
    lsipc
    echo -e "\n\n#$ lslocks\n"
    lslocks

    echo -e "\n\nProcess and Sockets"
    echo -e "-----------------------------------------------"
    echo -e "\n\n#$ netstat -tulpn\n"
    netstat -tulpn
}

show_kernel()
{
    echo -e "\n\n Kernel Info"
    echo -e "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    echo -e "\n\n Kernel Version" 
    echo -e "-----------------------------------------------"
    echo -e "\n\n#$ uname -a\n"
    uname -a
    echo -e "\n\n$# cat /proc/version\n"
    cat /proc/version
  
    echo -e "\n\n Kernel bootline"
    echo -e "-----------------------------------------------"
    echo -e "\n\n#$ cat /proc/cmdline\n"
    cat /proc/cmdline 

    #echo -e "\n\n Regenerate module dependencies"
    #echo -e "-----------------------------------------------"
    #echo -e "\n\n#$ depmod -a\n"
    #depmod -a

    # List module parameters
    # systool -vm $mod
    
    echo -e "\n\n Installed Kernel Modules"
    echo -e "-----------------------------------------------"
    echo -e "\n\n#$ for mod in `lsmod | awk '{print $1}'`; do echo -e \"$mod\", \"$(modinfo -F description $mod)\", \"$(modinfo -F filename $mod)\" , \"$(modinfo -F license $mod)\" , \"$(modinfo -F parm $mod)\" , \"$(modinfo -F depends $mod)\" , \"$(modinfo -F alias $mod)\" ; done \n" 
for mod in $(lsmod | awk '{print $1}') ; do echo -e \"$mod\", \"$(modinfo -F description $mod)\", \"$(modinfo -F filename $mod)\" , \"$(modinfo -F license $mod)\" , \"$(modinfo -F parm $mod)\" , \"$(modinfo -F depends $mod)\",
\"$(modinfo -F alias $mod)\" ; systool -vm $mod ; done 


    echo -e "\n\n Kernel module static nodes"
    echo -e "-----------------------------------------------"
    echo -e "\n\n#$ kmod static-nodes\n"
    kmod static-nodes

    echo -e "\n\n Kernel Config"
    echo -e "-----------------------------------------------"
    echo -e "\n\n#$ cat /boot/config-$(uname -r)\n "
    cat /boot/config-$(uname -r)
}

show_cpu()
{
    echo -e "\n\n CPU Info"
    echo -e "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    echo -e "\n\n#$ numactl -H \n"
    numactl -H

    echo -e "\n\n#$ lscpu \n"
    lscpu
    echo -e "\n\n#$ dmidecode -t processor \n"
    dmidecode -t processor

    echo -e "\n\n#$ cat /proc/devices \n"
    cat /proc/devices

    echo -e "\n\n#$ lshw \n"
    lshw

    #taskset -c -p <pid>
}

show_memory()
{
    echo -e "\n\n Memory Info"
    echo -e "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    echo -e "\n\n#$ dmidecode -t memory \n"
    dmidecode -t memory
    
    echo -e "\n\n#$ dmidecode -t cache \n"
    dmidecode -t cache

    echo -e "\n\n#$ cat /proc/meminfo \n"
    /proc/meminfo

    echo -e "\n\n#$ free \n"
    free

    echo -e "\n\n#$ vmstat -s \n"
    vmstat -s
}

show_pci_devices()
{
    echo -e "\n\n PCI Info"
    echo -e "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    echo -e "\n\n#$ lspci -tvv \n"
    lspci -tvv 

    echo -e "\n\n#$ lsusb \n"
    lsusb
}

show_storage()
{

    echo -e "\n\n Storage Info"
    echo -e "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    echo -e "\n\n Block Info" 
    echo -e "-----------------------------------------------"

    echo -e "\n\n#$ lsscsi \n"
    lsscsi

    echo -e "\n\n #$ blkid \n"
    blkid

    echo -e "\n\n #$ lsblk -ai \n"
    lsblk -ai

    echo -e "\n\n Parition table "
    echo -e "-----------------------------------------------"

    echo -e "\n\n #$ df -h \n"
    df -h

    echo -e "\n\n #$ fdisk -l \n"
    fdisk -l


    echo -e "\n\n Mount table "
    echo -e "-----------------------------------------------"

    echo -e "\n\n #$ mount -l \n"
    mount -l
}

show_network()
{
    echo -e "\n\n Network Info"
    echo -e "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    echo -e "\n\n Network Adapter "
    echo -e "-----------------------------------------------"

    echo -e "\n\n#$ lspci -tvv | grep -i "ethernet\|network" \n"
    lspci -tvv | grep -i "ethernet\|network"


    echo -e "\n\n Network Interfaces "
    echo -e "-----------------------------------------------"

    echo -e "\n\n#$ ifconfig -a \n"
    printf "=======================================================\n"
    printf "%-14s: %-7s | %-20s | %-20s | %-15s | %s\n" "|  intf" "    link" "    drv" "    hwaddr" "   inet" "   mask"
    printf "=======================================================\n"
    for intf in $(netstat -ia -p | sed '1,2d' | awk -F"  " '{print $1}')
    do
    #hwaddr=$(ifconfig $intf | grep -Go 'ether [a-zA-Z0-9:]\+' | awk -F'ether ' '{print $2}')
    hwaddr=$(ifconfig $intf | grep -Go 'ether [a-zA-Z0-9:]\+' | awk -F'ether ' '{print $2}')
    [ -z "$hwaddr" ] && hwaddr="----"
    link=$(ifconfig $intf | grep -Go 'Link encap:[a-zA-Z]\+' | awk -F'Link encap:' '{print $2}')
    [ -z "$link" ] && link="-"
    inet=$(ifconfig $intf | grep -Go 'inet [a-zA-Z0-9.]\+' | awk -F'inet ' '{print $2}')
    #inet=$(ifconfig $intf | grep -Go 'inet [a-zA-Z0-9.]\+' | awk -F'inet ' '{print $2}')
    [ -z "$inet" ] && inet="-"
    mask=$(ifconfig $intf | grep -Go 'netmask [a-zA-Z0-9.]\+' | awk -F'netmask ' '{print $2}')
    #mask=$(ifconfig $intf | grep -Go 'Mask:[a-zA-Z0-9.]\+' | awk -F'Mask:' '{print $2}')
    [ -z "$mask" ] && mask="-"
    drv=$(ethtool -i $intf 2> /dev/null | grep driver | awk -F'driver: ' '{print $2}')
    [ -z "$drv" ] && drv="-"
    printf "%-14s: %7s %20s %20s %15s %s\n" "$intf" "$link" "$drv" "$hwaddr" "$inet" "$mask"
    done

    echo -e "\n\n Network Link "
    echo -e "-----------------------------------------------"

    echo -e "\n\n#$ brctl show \n"
    brctl show


    #ifconfig -a
    #for intf in $(ifconfig -s | sed '1d' | awk -F"  " '{print $1}') ; do echo $intf; ethtool -S $intf | grep -i "drops: [1-9]\+" ; done

    echo -e "\n\n#$ statistics: netstat -ia -p \n"
    netstat -ia -p


    echo -e "\n\n#$ Ethernet NIC features: ethtool -? \n"
    for intf in $( netstat -ia -p | sed '1,2d' | awk -F"  " '{print $1}' ) ; do \
    echo -e "\n\n\n==========================================\n" ; \
    echo "       $intf" ;  \
    echo -e "\n==========================================\n" ; \
    echo -e "\n # Driver: \n" ; ethtool -i $intf | grep driver;  \
    echo -e "\n# Ethernet features: \n" ; ethtool -k $intf | grep ": on"; \
    echo -e "\n# get ring buffers \n" ; ethtool -g $intf ; \
    echo -e "\n# get driver \n" ;  ethtool -i $intf ; \
    echo -e "\n # Flow hash \n" ; ethtool -x $intf ; \
    echo -e "\n # Timing \n" ; ethtool -T $intf ; \
    echo -e "\n # Channel \n" ; ethtool -l $intf ; \
    done

    echo -e "\n\n Network IP Interfaces "
    echo -e "-----------------------------------------------"

    echo -e "\n\n#$ ip link show \n"
    ip link show

    echo -e "\n\n#$ tcpdump -D \n"
    tcpdump -D

    echo -e "\n\n#$ netstat -ia \n"
    netstat -ia


    echo -e "\n\n#$ ip a \n"
    ip a
    
    echo -e "\n\n#$ ip route \n"
    ip route

    echo -e "\n\n#$ ip route show table all \n"
    ip route show table all

    echo -e "\n\n#$ route -n \n"
    route -n

    echo -e "\n\n Network IP Rules "
    echo -e "-----------------------------------------------"

    echo -e "\n\n#$ iptables -L -v \n"
    iptables -L -v

    echo -e "\n\n Network Sockets "
    echo -e "-----------------------------------------------"

    echo -e "\n\n #$ ss -s \n"
    ss -s

    echo -e "\n\n#$ lsof -i \n"
    lsof -i

    echo -e "\n\n#$ ss -t -a # all tcp sockets \n"
    ss -t -ap # all tcp sockets

    echo -e "\n\n #$  ss -u -a # all udp sockets \n"
    ss -u -ap # all udp sockets

    echo -e "\n\n #$ ss -w -a # all raw sockets \n"
    ss -w -ap # all raw sockets

    echo -e "\n\n #$ ss -x -a # all unix sockets \n"
    ss -x -ap # all unix sockets
}

show_scheduler()
{

    echo -e "\n\n Scheduler Info"
    echo -e "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    echo -e "\n\n  chkconfig \n"
    chkconfig
    
    echo -e "\n\n service --status-all \n"
    service --status-all

}

show_loader_libs()
{

    echo -e "\n\n Loader Info"
    echo -e "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    echo -e "\n\n  ldd --version \n"
    ldd --version
    echo -e "\n\n  ldconfig paths \n"
    ldconfig -Nv 2> /dev/null | grep -v ^$'\t' | sed 's/\:.*/ /'

    echo -e "\n\n#$  ldconfig -p : from cache \n"
    ldconfig -p
}

show_time_sync()
{
    echo -e "\n\n Time Sync Info"
    echo -e "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    ntpstat
}

show_device_nodes()
{
    echo -e "\n\n All udev Device Nodes"
    echo -e "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    echo -e "\n\n Block Devices "
    echo -e "-----------------------------------------------"
    # block devices
    echo -e "\n\n find  /dev -type b | xargs -I{} sh -c 'echo -e "\n\n [ {} ]\n"; udevadm info --query=all --name={} ' \n"
    find  /dev -type b | xargs -I{} sh -c 'echo -e "\n\n [ {} ]\n"; udevadm info --query=all --name={} '

    # character devices
    echo -e "\n\n Character Devices "
    echo -e "-----------------------------------------------"
    echo -e "\n\n find  /dev -type c | xargs -I{} sh -c 'echo -e "\n\n [ {} ]\n"; udevadm info --query=all --name={} ' \n"
    find  /dev -type c | xargs -I{} sh -c 'echo -e "\n\n [ {} ]\n"; udevadm info --query=all --name={} '

    echo -e "\n\n All Devices "
    echo -e "-----------------------------------------------"
    # links
    echo -e "\n\n find  /sys -type l | xargs -I{} sh -c 'echo -e "\n\n [ {} ]\n"; udevadm info --query=all --name={} ' \n"
    find  /sys -type l | xargs -I{} sh -c 'echo -e "\n\n [ {} ]\n"; udevadm info --query=all --name={} '

    echo -e "\n\n find  /dev -type l | xargs -I{} sh -c 'echo -e "\n\n [ {} ]\n"; udevadm info --query=all --name={} ' \n"
    find  /dev -type l | xargs -I{} sh -c 'echo -e "\n\n [ {} ]\n"; udevadm info --query=all --name={} '
    
}


show_statistics()
{

    nstat
    netstat -i
    ip -s link

    # Socket Level statistics
    netstat -s
    ss -s

}


show_perf_counters()
{
    # top 
    top -n 1 -b

    # top respective cpu
    top -c 1 -n 1 -b

    echo -e "\n\n CPU Performance Counters"
    echo -e "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    echo -e "\n\n perf list "
    echo -e "-----------------------------------------------"

    echo -e "\n\n perf list ' \n"
    perf list

    echo -e "\n\n Cpu performance counters "
    echo -e "-----------------------------------------------"
    perf stat -a sleep 10

}


show_host
show_virtual
show_docker
show_process
show_kernel
show_cpu
show_memory
show_pci_devices
show_storage
show_network
show_scheduler
show_time_sync
show_perf_counters
show_loader_libs
show_device_nodes
