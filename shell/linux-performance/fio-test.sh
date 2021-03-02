# dd: time dd if=/dev/zero of=test.file bs=10M count=100 oflag=direct


dev_name=vda

echo -e "\033[32m>>> 100%随机, 100%读, 4K...\033[0m" 
fio -filename=/dev/${dev_name} -direct=1 -iodepth 1 -thread -rw=randread -ioengine=psync -bs=4k -size=1G -numjobs=50 -runtime=10 -group_reporting -name=rand_100read_4k

echo -e "\033[32m>>> 100%随机, 100%写, 4K...\033[0m" 
fio -filename=/dev/${dev_name} -direct=1 -iodepth 1 -thread -rw=randwrite -ioengine=psync -bs=4k -size=1G -numjobs=50 -runtime=10 -group_reporting -name=rand_100write_4k

echo -e "\033[32m>>> 100%顺序, 100%读, 4K...\033[0m" 
fio -filename=/dev/${dev_name} -direct=1 -iodepth 1 -thread -rw=read -ioengine=psync -bs=4k -size=1G -numjobs=50 -runtime=10 -group_reporting -name=sqe_100read_4k

echo -e "\033[32m>>> 100%顺序, 100%写, 4K...\033[0m" 
fio -filename=/dev/${dev_name} -direct=1 -iodepth 1 -thread -rw=write -ioengine=psync -bs=4k -size=1G -numjobs=50 -runtime=10 -group_reporting -name=sqe_100write_4k

echo -e "\033[32m>>> 100%随机, 70%读30%写, 4K...\033[0m" 
fio -filename=/dev/${dev_name} -direct=1 -iodepth 1 -thread -rw=randrw -rwmixread=70 -ioengine=psync -bs=4k -size=1G -numjobs=50 -runtime=10 -group_reporting -name=randrw_70read_4k
