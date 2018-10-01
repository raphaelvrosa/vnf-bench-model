# p2-mp

## HTTP testing

* Apache Bench
	* Time limit:
		* ab -q -c 10 -t 60 http://10.0.0.3/10kb.dat
	* Request num:
		* ab -q -c 10 -n 500 http://10.0.0.3/10kb.dat
* Web Polygraph
	* 
* Siege
	* siege -b -c 500 -r 3 http://10.0.0.3/
* HTTPerf
	* httperf --server 10.0.0.3 --num-conns 100 --rate 10 --timeout 1

### Generate random files:
* head --bytes 1024 < /dev/urandom > 1kb.dat
